import os
import tensorflow.compat.v1 as tf
from magenta.models.music_vae import configs, trained_model
import numpy as np
import time
import random
from pythonosc import udp_client

# --- INSERISCI I PERCORSI NEGLI SPAZI MANCANTI ---
BASE_DIR = ""
DRUMS_CKPT = os.path.join(BASE_DIR, "")
GUITAR_CKPT = os.path.join(BASE_DIR, "")
BASS_CKPT = os.path.join(BASE_DIR, "")

client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

# Dizionario Accordi (One-hot per med_chords)
CHORD_MAP = {
    'C': 1, 'C#': 2, 'D': 3, 'Eb': 4, 'E': 5, 'F': 6, 'F#': 7, 'G': 8, 'Ab': 9, 'A': 10, 'Bb': 11, 'B': 12,
    'Cm': 13, 'C#m': 14, 'Dm': 15, 'Ebm': 16, 'Em': 17, 'Fm': 18, 'F#m': 19, 'Gm': 20, 'Abm': 21, 'Am': 22, 'Bbm': 23, 'Bm': 24
}

def get_chord_cond(chord_name):
    cond = np.zeros((1, 49), dtype=np.float32)
    idx = CHORD_MAP.get(chord_name, 17) # Default Em
    cond[0, idx] = 1.0
    return cond

def generate_full_metal_chaos():
    print("--- METAL CORE IA ---")
    tf.disable_v2_behavior()
    np.random.seed(int(time.time()))

    m_drums = trained_model.TrainedModel(configs.CONFIG_MAP['cat-drums_2bar_small'], batch_size=1, checkpoint_dir_or_path=DRUMS_CKPT)
    m_guitar = trained_model.TrainedModel(configs.CONFIG_MAP['cat-mel_2bar_big'], batch_size=1, checkpoint_dir_or_path=GUITAR_CKPT)
    m_bass = trained_model.TrainedModel(configs.CONFIG_MAP['cat-mel_2bar_med_chords'], batch_size=1, checkpoint_dir_or_path=BASS_CKPT)

    progressions = [     
        ['Em', 'Fm', 'Em', 'Bb'],   
        ['Em', 'D', 'C', 'B'],       
        ['Em', 'F#m', 'G', 'A'],     
        ['Em', 'Bb', 'A', 'Ab'],     
        ['Em', 'G', 'F', 'Em'],      
        ['Em', 'A', 'C', 'B'],
        ['Em', 'G', 'F', 'Em']
        ['Em', 'G', 'D', 'A'],       
        ['Em', 'C', 'G', 'D'] 
    ]

    root_notes = {
        'Em': 40, 'Fm': 41, 'F#m': 42, 'G': 43, 'Ab': 44, 'A': 45, 
        'Bb': 46, 'B': 47, 'C': 36, 'C#': 37, 'D': 38, 'Eb': 39
    }
    
    TEMPO = 155.0
    step_dur = (60.0 / TEMPO) * 0.5 

    z_g = np.random.normal(size=[1, 512]).astype(np.float32)
    z_d = np.random.normal(size=[1, 256]).astype(np.float32)
    z_b = np.random.normal(size=[1, 256]).astype(np.float32)

    while True:
        # Scegli una progressione a caso ad ogni ciclo
        current_prog = random.choice(progressions)
        print(f"Playing Progression: {current_prog}")

        for bar_idx, chord in enumerate(current_prog * 2):
            root_pitch = root_notes.get(chord, 40)
            chord_cond = get_chord_cond(chord)
            
            d_notes = m_drums.decode(z=z_d, length=32, temperature=1.2)[0].notes
            g_notes = m_guitar.decode(z=z_g, length=32, temperature=1.1)[0].notes
            b_notes = m_bass.decode(z=z_b, length=32, temperature=0.8, c_input=chord_cond)[0].notes

            # Crash all'inizio di ogni nuova progressione
            if bar_idx == 0:
                client.send_message("/instrument/drums/crash", 127.0)

            for s in range(16):
                t_start = time.time()
                current_step_time = s * step_dur
                
                # --- DRUMS INCALZANTE ---
                has_kick = False
                has_snare = False
                for n in d_notes:
                    if abs(n.start_time - current_step_time) < 0.05:
                        if n.pitch == 36: has_kick = True
                        if n.pitch == 38: has_snare = True

                if s % 2 == 0: has_kick = True # Double kick drive
                if s == 4 or s == 12: has_snare = True # Snare solid

                if has_kick: client.send_message("/instrument/drums/kick", random.uniform(115, 127))
                if has_snare: client.send_message("/instrument/drums/snare", random.uniform(120, 127))
                
                # Hi-Hat incalzante
                if s % 2 == 0 or random.random() < 0.3:
                    client.send_message("/instrument/drums/hihat", random.uniform(70, 100))

                # --- GUITAR & BASS ---
                g_pitch = root_pitch
                for n in g_notes:
                    if abs(n.start_time - current_step_time) < 0.05:
                        g_pitch = (n.pitch % 12) + (root_pitch // 12 * 12)
                        break
                client.send_message("/instrument/guitar", [float(g_pitch), 105.0])
                client.send_message("/instrument/guitar", [float(g_pitch + 7), 95.0])

                b_pitch = root_pitch - 12
                for n in b_notes:
                    if abs(n.start_time - current_step_time) < 0.05:
                        b_pitch = (n.pitch % 12) + ((root_pitch - 12) // 12 * 12)
                        break
                if b_pitch < 38: b_pitch += 12 
                client.send_message("/instrument/bass", [float(b_pitch), 90.0])

                elapsed = time.time() - t_start
                time.sleep(max(0, step_dur - elapsed))

            # Evoluzione per non essere ripetitivi
            z_d += np.random.normal(size=[1, 256], scale=0.04).astype(np.float32)
            z_g += np.random.normal(size=[1, 512], scale=0.03).astype(np.float32)
            z_b += np.random.normal(size=[1, 256], scale=0.02).astype(np.float32)

if __name__ == "__main__":
    generate_full_metal_chaos()
