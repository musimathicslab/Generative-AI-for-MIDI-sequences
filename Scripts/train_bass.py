# --- CONFIGURAZIONE GPU / CPU STABILE WINDOWS ---
import os
import sys
import platform
import types
import tensorflow as tf
import subprocess
import numpy as np 

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# --- FORZA GROWTH GPU PRIMA DI TUTTO ---
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
USE_GPU = False
if USE_GPU:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("GPU attiva e configurata con growth")
        except RuntimeError as e:
            print(f"Errore configurazione GPU: {e}")
    else:
        print("Nessuna GPU trovata, useremo CPU")
        USE_GPU = False

if not USE_GPU:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    print(" Modalita CPU attiva")

# --- FIX WINDOWS resource ---
if platform.system() == "Windows":
    fake_resource = types.ModuleType("resource")
    fake_resource.RLIMIT_NOFILE = 1024
    fake_resource.getrlimit = lambda *a, **kw: (1024, 1024)
    fake_resource.setrlimit = lambda *a, **kw: None
    sys.modules["resource"] = fake_resource

# --- FIX NUMPY DEPRECATION ---
if not hasattr(np, 'bool'):
    np.bool = bool

# --- CONFIG TRAINING ---
TRAINING_CONFIG = {
    'drums_rnn': {'steps': 25000, 'batch_size': 8, 'rnn_layers': [128, 128]},
    'music_vae': {'steps': 25000, 'batch_size': 4}
}

#--- INSERISCI PERCORSI ---
TF_DATA_PATH = ""
RUN_BASE_DIR = ''

# ============== FUNZIONE DI VERIFICA DATI (NUOVA) ==============
def check_tfrecord(filepath):
    """Controlla se il TFRecord contiene dati validi"""
    import tensorflow as tf
    from magenta.protobuf import music_pb2
    
    count = 0
    try:
        print(f"\n[VERIFICA] Analisi file: {filepath}")
        for record in tf.compat.v1.python_io.tf_record_iterator(filepath):
            sequence = music_pb2.NoteSequence.FromString(record)
            if len(sequence.notes) > 0:
                count += 1
                if count == 1:  # Mostra info prima sequenza
                    print(f"  Prima sequenza valida:")
                    print(f"    - Note: {len(sequence.notes)}")
                    print(f"    - Durata: {sequence.total_time:.2f} secondi")
                    print(f"    - BPM: {sequence.tempos[0].qpm if sequence.tempos else 'N/A'}")
            if count >= 3:  # Controlla solo prime 3
                break
        print(f"  Trovate {count} sequenze valide (prime 3 controllate)")
        return count > 0
    except Exception as e:
        print(f"  ERRORE nella lettura: {e}")
        return False
# ===============================================================

def create_music_vae_fix_script(use_gpu=True):
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_path, 'music_vae_train_fix.py')
    
    fix_script = '''# -*- coding: utf-8 -*-
import os, sys
import tensorflow.compat.v1 as tf
from magenta.models.music_vae import music_vae_train, configs

# DISABILITA GPU - OBBLIGATORIO SU WINDOWS/COLAB INSTABILE
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def main(unused_argv):
    # 1. PRIMA VERIFICA LE CONFIGURAZIONI DISPONIBILI
    print("\\n=== CONFIGURAZIONI DISPONIBILI ===")
    available_configs = list(configs.CONFIG_MAP.keys())
    for i, cfg in enumerate(available_configs):
        print(f"{i+1}. {cfg}")
    
    # 2. CERCA CONFIGURAZIONI COMPATIBILI PER BASSO (2 battute, melodiche)
    compatible_configs = []
    for cfg_name in available_configs:
        cfg_lower = cfg_name.lower()
        # Cerca configurazioni per melodie di 2 battute (ignora drums)
        if ('2bar' in cfg_lower or '1bar' in cfg_lower) and 'drum' not in cfg_lower:
            compatible_configs.append(cfg_name)
    
    print("\\n=== CONFIGURAZIONI COMPATIBILI (2 battute, non batteria) ===")
    for cfg in compatible_configs:
        print(f"  - {cfg}")
    
    # 3. SCEGLI LA CONFIGURAZIONE - PRIORITÀ A QUELLE PER MELODIE/MONOFONICHE
    config_name = None
    # Prima prova con 'cat-mel_2bar_med_chords' (supporta accordi leggeri)
    if 'cat-mel_2bar_med_chords' in compatible_configs:
        config_name = 'cat-mel_2bar_med_chords'
    # Poi prova con 'cat-mel_2bar_big'
    elif 'cat-mel_2bar_big' in compatible_configs:
        config_name = 'cat-mel_2bar_big'
    # Infine la prima disponibile
    elif compatible_configs:
        config_name = compatible_configs[0]
    
    if not config_name:
        print("\\n ERRORE: Nessuna configurazione compatibile trovata!")
        sys.exit(1)
    
    print(f"\\n Configurazione selezionata: {config_name}")
    
    # IMPOSTA IL FLAG CONFIG (ESSENZIALE PER LA VALIDAZIONE INTERNA)
    tf.app.flags.FLAGS.config = config_name
    
    # 4. RIDUCI BATCH SIZE E IMPOSTA PARAMETRI PER STABILITÀ
    config = configs.CONFIG_MAP[config_name]
    config.hparams.batch_size = 2  # MINIMO ASSOLUTO
    # Se la configurazione ha un parametro 'max_seq_len', impostalo a 32 (2 battute)
    if hasattr(config.hparams, 'max_seq_len'):
        config.hparams.max_seq_len = 32
    print(f"Batch size impostato a: {config.hparams.batch_size}")
    
    # 5. IMPOSTA DIRECTORY DI OUTPUT
    run_dir = tf.app.flags.FLAGS.run_dir
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
    
    print(f"\\n=== AVVIO TRAINING ===")
    print(f"Config: {config_name}")
    print(f"TFRecord: {tf.app.flags.FLAGS.examples_path}")
    print(f"Run dir: {run_dir}")
    print(f"Steps: {tf.app.flags.FLAGS.num_steps}")
    print("=" * 40 + "\\n")
    
    # 6. AVVIA TRAINING UFFICIALE - PASSANDO L'INTERO DIZIONARIO DI CONFIGURAZIONI
    try:
        music_vae_train.run(configs.CONFIG_MAP)
        print("\\n TRAINING COMPLETATO CON SUCCESSO!")
    except Exception as e:
        print(f"\\n ERRORE DURANTE IL TRAINING: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    tf.disable_v2_behavior()
    tf.app.run(main)
'''
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fix_script)
    return path

def run_training():
    print("\n" + "="*60)
    print("AVVIO TRAINING STABILE - METALLICA BASS AI")
    print("="*60)

    # Percorsi TFRecord
    DRUMS_TFRECORD = os.path.join(TF_DATA_PATH, 'drums_rnn_sequences', 'training_drum_tracks.tfrecord')
    BASS_TFRECORD = os.path.join(TF_DATA_PATH, 'bass_ultimate.tfrecord')
    GUITAR_TFRECORD = os.path.join(TF_DATA_PATH, 'metal_guitar_sequences.tfrecord')

    DRUMS_RUN_DIR = os.path.join(RUN_BASE_DIR, 'drums_rnn_train')
    BASS_RUN_DIR = os.path.join(RUN_BASE_DIR, 'bass_vae_train')
    GUITAR_RUN_DIR = os.path.join(RUN_BASE_DIR, 'guitar_vae_train')

    # ============== VERIFICA DATI PRIMA DEL TRAINING ==============
    '''print("\n" + "="*60)
    print("FASE 1: VERIFICA DATI TFRecord")
    print("="*60)
    
    if not os.path.exists(BASS_TFRECORD):
        print(f"\n ERRORE CRITICO: File non trovato!")
        print(f"Percorso: {BASS_TFRECORD}")
        print("\nSoluzione:")
        print("1. Controlla che il file esista")
        print("2. Se non esiste, rigeneralo con:")
        print("   convert_dir_to_note_sequences --input_dir=midi_bass --output_file=bass_ultimate.tfrecord")
        return
    
    if not check_tfrecord(BASS_TFRECORD):
        print("\n DATI NON VALIDI: Il training non può partire.")
        print("   Rigenera il TFRecord con dati MIDI puliti.")
        return
    
    print("\n VERIFICA DATI COMPLETATA CON SUCCESSO!")'''
    # ===============================================================

    def run_command(cmd, description):
        full_command = ' '.join(cmd)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        print(f"\n{'='*60}")
        print(f"{description}")
        print(f"{'='*60}")
        print(f"Comando: {full_command}")
        
        try:
            process = subprocess.Popen(full_command, 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.STDOUT, 
                                       universal_newlines=True,
                                       shell=True,
                                       cwd=base_dir)
            for line in process.stdout:
                print(line, end='')
            process.wait()
            
            if process.returncode == 0:
                print(f"\n {description} COMPLETATO!")
            else:
                print(f"\n {description} FALLITO (codice: {process.returncode})")
            return process.returncode == 0
        except Exception as e:
            print(f"\n Errore di esecuzione: {e}")
            return False

    # --- TRAIN MUSICVAE BASSO (SOLO QUESTO PER ORA) ---
    os.makedirs(BASS_RUN_DIR, exist_ok=True)
    fix_script = create_music_vae_fix_script(use_gpu=USE_GPU)
    
    # COMANDO CORRETTO: rimuovi --config perché ora lo sceglie automaticamente
    cmd = [
        'python', fix_script,
        f'--run_dir={BASS_RUN_DIR}',
        f'--examples_path={BASS_TFRECORD}',
        '--num_steps=15000'  # RIDOTTO PER TEST INIZIALE
    ]
    
    success = run_command(cmd, "MusicVAE BASS TRAINING")
    
    if os.path.exists(fix_script):
        os.remove(fix_script)
    
    if success:
        print("\n" + "="*60)
        print(" TRAINING BASSO METALLICA COMPLETATO!")
        print("="*60)
        print(f"Checkpoint salvati in: {BASS_RUN_DIR}")
        print("\nProssimi passi:")
        print("1. Usa 'music_vae_generate' per creare nuovi riff")
        print("2. Aumenta --num_steps a 10000+ per training completo")
        print("3. Prova con altri configurazioni")
    else:
        print("\n" + "="*60)
        print(" TRAINING FALLITO")
        print("="*60)
        print("Condividi l'errore completo per debug.")

if __name__ == '__main__':
    run_training()
