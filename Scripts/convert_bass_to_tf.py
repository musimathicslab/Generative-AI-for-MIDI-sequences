import os
import tensorflow as tf
from magenta.models.music_vae.data import OneHotMelodyConverter
import note_seq

# ==================== MODIFICA QUESTI PERCORSI ====================
your_bass_midi_folder = ""
# ==================================================================
OUTPUT_TFRECORD = ""

def convert_midi_to_musicvae_tfrecord(midi_dir, output_path):
    """Converte MIDI di basso in TFRecord per MusicVAE."""
    # 1. CONFIGURA IL CONVERTER PER MELODIE DI 2 BATTUTE
    converter = OneHotMelodyConverter(
        slice_bars=2,                     # SEGMENTA in blocchi di 2 battute
        gap_bars=1.0,                     # Impostazione predefinita
        max_tensors_per_notesequence=8,   # Massimo segmenti per brano
        min_pitch=28,                     # Pitch minimo per basso (E1)
        max_pitch=67,                     # Pitch massimo per basso (~G4)
        valid_programs=[32, 33, 34, 35, 36, 37, 38, 39],  # Programmi per basso
        steps_per_quarter=4,
        quarters_per_bar=4,
        skip_polyphony=False              # IMPORTANTE: mantieni le doppie corde
    )
    
    # 2. CREA LO SCRITTORE TFRecord
    with tf.io.TFRecordWriter(output_path) as writer:
        midi_files = [f for f in os.listdir(midi_dir) if f.lower().endswith('.mid')]
        print(f"Trovati {len(midi_files)} file MIDI di basso.")
        
        total_examples = 0
        for midi_file in midi_files:
            full_path = os.path.join(midi_dir, midi_file)
            try:
               # 3. LEGGI IL MIDI
               ns = note_seq.midi_file_to_note_sequence(full_path)
               # --- INIZIO MODIFICA: PULIZIA CAMPI TESTO ---
               import hashlib
               # Genera un ID univoco e sicuro (stringa esadecimale ASCII)
               ns.id = hashlib.md5(ns.SerializeToString()).hexdigest()
               # Pulisci il campo filename (imposta a stringa vuota)
               ns.filename = ''
               # --- FINE MODIFICA ---
               
               # 4. PULIZIA CRITICA: assegna tutte le note al programma BASSO
               for note in ns.notes:
                note.program = 34  # Bass Electric (PGM 34 General MIDI)
                note.instrument = 0  # Strumento unificato
                    # Opzionale: trasponi note troppo basse (sotto E1)
                    # if note.pitch < 28:
                    #     note.pitch += 12
                
                # 5. CONVERTI IN TENSORI (segmenti)
                tensors = converter.to_tensors(ns)
                
                if not tensors.inputs:
                    print(f" Saltato: {midi_file} (nessun segmento valido)")
                    continue
                
                # 6. SCRIVI OGNI SEGMENTO NEL TFRecord
                segment_count = len(tensors.inputs)
                for i in range(segment_count):
                    example = tf.train.Example(
                        features=tf.train.Features(feature={
                            'inputs': tf.train.Feature(
                                float_list=tf.train.FloatList(value=tensors.inputs[i].flatten())
                            ),
                            'lengths': tf.train.Feature(
                                int64_list=tf.train.Int64List(value=[tensors.lengths[i]])
                            )
                        })
                    )
                    writer.write(example.SerializeToString())
                
                total_examples += segment_count
                print(f"   {midi_file}: creati {segment_count} segmenti")
                
            except Exception as e:
                print(f"   Errore in {midi_file}: {e}")
                continue
    
    print(f"\n CONVERSIONE BASSO COMPLETATA!")
    print(f"   Segmenti totali creati: {total_examples}")
    print(f"   File salvato in: {output_path}")
    
    # STIMA DELLA DIMENSIONE
    if total_examples > 0:
        avg_per_song = total_examples / len(midi_files)
        print(f"   Media: {avg_per_song:.1f} segmenti per brano")
        if total_examples < 500:
            print("  Dataset piccolo. Considera aggiungere più brani.")
        else:
            print(" Dataset di buone dimensioni per il training.")

if __name__ == "__main__":
    if os.path.exists(your_bass_midi_folder):
        convert_midi_to_musicvae_tfrecord(your_bass_midi_folder, OUTPUT_TFRECORD)
    else:
        print(f"Cartella non trovata: {your_bass_midi_folder}")
        print("   Modifica la variabile 'your_bass_midi_folder' nello script.")
