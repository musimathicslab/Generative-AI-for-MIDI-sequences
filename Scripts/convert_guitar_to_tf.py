import os
import tensorflow as tf
from magenta.music.protobuf import music_pb2
from magenta.music import midi_io
import pretty_midi

# --- INSERISCI PERCORSO ---
TF_OUTPUT_DIR = ""

# Le cartelle che contengono i tuoi file MIDI separati - INSERISCI NOME CARTELLA
INPUT_DIRS = {
    'guitar': ''
}

# I percorsi dove salvare i file TFRecord per il training
OUTPUT_FILES = {
    'guitar': os.path.join(TF_OUTPUT_DIR, 'metal_guitar.tfrecord')
}

# --- Funzioni ---

def convert_dir_to_tfrecord(input_dir, output_file):
    """
    Legge tutti i file MIDI in input_dir, li converte in NoteSequence
    e scrive un singolo file TFRecord.
    """
    print(f"\n Avvio conversione per la directory: {input_dir}")
    
    # Inizializza il TFRecordWriter
    # Nota: su Windows, '/tmp/' potrebbe dover essere cambiato in una cartella locale sicura
    writer = tf.io.TFRecordWriter(output_file)
    
    num_converted = 0
    num_skipped = 0
    
    # Itera su tutti i file MIDI
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.mid', '.midi')):
            full_path = os.path.join(input_dir, filename)
            
            try:
                # 1. Carica il file MIDI con pretty_midi
                midi_data = pretty_midi.PrettyMIDI(full_path)
                
                # 2. Converte in NoteSequence di Magenta
                note_sequence = midi_io.midi_to_note_sequence(midi_data)
                
                # 3. Serializza e Scrivi nel TFRecord
                writer.write(note_sequence.SerializeToString())
                num_converted += 1
                
            except Exception as e:
                print(f"    Errore processando {filename}: {e}")
                num_skipped += 1
                continue

    writer.close()
    print(f" Conversione completata per {input_dir}.")
    print(f"   Totale convertiti: {num_converted}, Saltati: {num_skipped}")

# --- Esecuzione Principale ---
if __name__ == "__main__":
    
    # Verifica la directory /tmp/ se non esiste su Windows (cambia se necessario)
    temp_dir = os.path.dirname(OUTPUT_FILES['drums'])
    if temp_dir and not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)
        
    for track_type, input_dir in INPUT_DIRS.items():
        output_file = OUTPUT_FILES[track_type]
        convert_dir_to_tfrecord(input_dir, output_file)
        
    print("\nTutte le conversioni in TFRecord sono terminate con successo.")
