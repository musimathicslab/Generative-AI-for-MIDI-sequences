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
            # Crescita graduale della memoria GPU
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
    'music_vae': {'steps': 25000, 'batch_size': 4}
}

# --- INSERISCI PERCORSI --- 
TF_DATA_PATH = ""
RUN_BASE_DIR = ''


def create_music_vae_fix_script(use_gpu=True):
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_path, 'music_vae_train_fix.py')
    
    fix_script = '''# -*- coding: utf-8 -*-
import os, sys
import tensorflow.compat.v1 as tf
from magenta.models.music_vae import music_vae_train, configs

# DISABILITA GPU - OBBLIGATORIO SU WINDOWS/COLAB INSTABILE
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
    if config_name not in configs.CONFIG_MAP:
        print(f"ERRORE: Configurazione {config_name} non trovata!")
        print("Configurazioni disponibili:", list(configs.CONFIG_MAP.keys()))
        sys.exit(1)
    
    config = configs.CONFIG_MAP[config_name]
    
    # 2. RIDUCI BATCH SIZE AL MINIMO PER STABILITÀ
    config.hparams.batch_size = 2
    config.hparams.max_seq_len = 32  # Per 2 battute (16*2)
    
    # 3. IMPOSTA DIRECTORY DI OUTPUT
    run_dir = tf.app.flags.FLAGS.run_dir
    if not os.path.exists(run_dir):
        os.makedirs(run_dir)
    
    print(f"=== CONFIGURAZIONE MUSIC VAE ===")
    print(f"Config: {config_name}")
    print(f"Batch size: {config.hparams.batch_size}")
    print(f"TFRecord: {tf.app.flags.FLAGS.examples_path}")
    print(f"Run dir: {run_dir}")
    print("=" * 40)
    
    # 4. AVVIA TRAINING UFFICIALE
    try:
        music_vae_train.run(config)
    except Exception as e:
        print(f"\\n!!! ERRORE DURANTE IL TRAINING: {e}")
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
    print("\n AVVIO TRAINING STABILE")

    # Percorsi TFRecord
    GUITAR_TFRECORD = os.path.join(TF_DATA_PATH, 'xxx.tfrecord') //inserisci nome file
    GUITAR_RUN_DIR = os.path.join(RUN_BASE_DIR, '') //inserisci directory

    def run_command(cmd, description):
        full_command = ' '.join(cmd)
        # Forza la cartella di lavoro su quella dello script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        print(f"\n {description}")
        print(f"Comando shell: {full_command}")
        
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
            return process.returncode == 0
        except Exception as e:
            print(f" Errore di esecuzione: {e}")
            return False
          
    # --- TRAIN MUSICVAE CHITARRA ---
    os.makedirs(GUITAR_RUN_DIR, exist_ok=True)
    fix_script = create_music_vae_fix_script(use_gpu=USE_GPU)
    cmd = [
        'python', fix_script,
        '--config=cat-mel_2bar_big',
        f'--run_dir={GUITAR_RUN_DIR}',
        f'--examples_path={GUITAR_TFRECORD}',
        '--hparams=batch_size=4',
        '--num_steps=25000'
    ]
    run_command(cmd, "MusicVAE Chitarra")

    if os.path.exists(fix_script):
        os.remove(fix_script)

if __name__ == '__main__':
    run_training()
