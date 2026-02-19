import os
import time
import tensorflow.compat.v1 as tf
from magenta.models.music_vae import configs
from magenta.models.music_vae import trained_model
import note_seq
import numpy as np

# --- CONFIGURAZIONE --- INSERISCI I PERCORSI RELATIVI ALLE CARTELLE CONTENENTI LE CARTELLE DEI TRAIN E COME ULTIMA QUELAL DOVE FINSICONO LE GENERAZIONI
BASE_DIR = ""
DRUMS_CKPT = os.path.join(BASE_DIR, "")
GUITAR_CKPT = os.path.join(BASE_DIR, "")
BASS_CKPT = os.path.join(BASE_DIR, "")
GEN_DIR = ""

def generate_creative_track(track_index):
    seed = int(time.time() * 1000) % 2**32
    np.random.seed(seed)
    tf.set_random_seed(seed)
    
    current_bpm = float(np.random.randint(135, 185))
    creative_temp = np.random.uniform(0.9, 1.3)
    
    # Libreria semplificata senza nomi
    metal_library = [
        ['Em', 'F', 'G', 'F', 'Bb', 'Ab', 'Em', 'B'],
        ['Em', 'C', 'A', 'B', 'Em', 'G', 'D', 'A'],
        ['Em', 'Eb', 'Em', 'Eb', 'F', 'Gb', 'G', 'B']
    ]
    
    progression = metal_library[np.random.randint(0, len(metal_library))]
    root_notes = {'Em': 40, 'F': 41, 'G': 43, 'A': 45, 'B': 47, 'C': 36, 'D': 38, 'Eb': 39, 'Ab': 44, 'Gb': 42, 'Bb': 46}

    os.makedirs(GEN_DIR, exist_ok=True)
    tf.disable_v2_behavior()

    m_drums = trained_model.TrainedModel(configs.CONFIG_MAP['cat-drums_2bar_small'], batch_size=1, checkpoint_dir_or_path=DRUMS_CKPT)
    m_guitar = trained_model.TrainedModel(configs.CONFIG_MAP['cat-mel_2bar_big'], batch_size=1, checkpoint_dir_or_path=GUITAR_CKPT)
    m_bass = trained_model.TrainedModel(configs.CONFIG_MAP['cat-mel_2bar_med_chords'], batch_size=1, checkpoint_dir_or_path=BASS_CKPT)

    final_ns = note_seq.NoteSequence()
    final_ns.tempos.add(qpm=current_bpm)

    step_dur = (60.0 / current_bpm) / 4 
    sec_per_block = 32 * step_dur

    print(f"\n--- GENERAZIONE {track_index} ---")
    print(f"BPM: {current_bpm} | Temp IA: {creative_temp:.2f}")

    for i, chord in enumerate(progression):
        block_start = i * sec_per_block
        root_pitch = root_notes.get(chord, 40)
        
        z_d = np.random.normal(size=[1, 256]).astype(np.float32)
        z_g = np.random.normal(size=[1, 512]).astype(np.float32)
        z_b = np.random.normal(size=[1, 256]).astype(np.float32)
        
        d_idea = m_drums.decode(z=z_d, length=32, temperature=creative_temp)[0]
        g_idea = m_guitar.decode(z=z_g, length=32, temperature=1.1)[0]
        try: 
            b_idea = m_bass.decode(z=z_b, length=32, temperature=1.0)[0]
        except: 
            b_idea = g_idea

        recorded_notes = set()

        # LOGICA BATTERIA
        for n in d_idea.notes:
            quantized_step = round(n.start_time / step_dur)
            t_curr = block_start + (quantized_step * step_dur)
            note_key = (quantized_step, n.pitch)
            if note_key not in recorded_notes:
                dn = final_ns.notes.add()
                dn.pitch, dn.start_time, dn.end_time = n.pitch, t_curr, t_curr + 0.1
                dn.is_drum, dn.instrument = True, 9
                if n.pitch in [36, 38]:
                    dn.velocity = np.random.randint(110, 127)
                else:
                    dn.velocity = np.random.randint(70, 95)
                recorded_notes.add(note_key)

        # LOGICA CHITARRA E BASSO
        for s in range(32):
            if s % 2 == 0: 
                t_curr = block_start + (s * step_dur)
                curr_g = root_pitch
                for n in g_idea.notes:
                    if abs(n.start_time - (s * step_dur)) < 0.1:
                        curr_g = (n.pitch % 12) + (root_pitch // 12 * 12)
                        break
                for interval in [0, 7]:
                    gn = final_ns.notes.add()
                    gn.pitch, gn.start_time, gn.end_time = curr_g + interval, t_curr, t_curr + step_dur
                    gn.instrument, gn.program, gn.velocity = 1, 30, 100
                
                curr_b = root_pitch - 12
                for n in b_idea.notes:
                    if abs(n.start_time - (s * step_dur)) < 0.1:
                        curr_b = (n.pitch % 12) + 24
                        break
                bn = final_ns.notes.add()
                bn.pitch, bn.start_time, bn.end_time = curr_b, t_curr, t_curr + step_dur
                bn.instrument, bn.program, bn.velocity = 0, 34, 110

    # Nome file semplificato: generazione_X.mid
    file_name = f"generazione_{track_index}.mid"
    output_path = os.path.join(GEN_DIR, file_name)
    note_seq.sequence_proto_to_midi_file(final_ns, output_path)
    print(f"File salvato: {output_path}")

if __name__ == "__main__":
    # Genera 10 tracce numerate
    for i in range(1, 11):
        generate_creative_track(i)
        time.sleep(0.1)
