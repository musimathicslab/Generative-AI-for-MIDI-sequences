# --- CONFIGURAZIONE GPU / CPU STABILE WINDOWS ---
import os
import sys
import platform
import types
import tensorflow as tf
import subprocess
import numpy as np 

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

if platform.system() == "Windows":
    fake_resource = types.ModuleType("resource")
    fake_resource.RLIMIT_NOFILE = 1024
    fake_resource.getrlimit = lambda *a, **kw: (1024, 1024)
    fake_resource.setrlimit = lambda *a, **kw: None
    sys.modules["resource"] = fake_resource

if not hasattr(np, 'bool'):
    np.bool = bool

# --- INSERISCI PERCORSI PROGETTO ---
TF_DATA_PATH = ""
RUN_BASE_DIR = ''

def create_drums_vae_fix_script():
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_path, 'drums_vae_train_fix.py')
    
    fix_script = '''# -*- coding: utf-8 -*-
import os, sys
import tensorflow.compat.v1 as tf
from magenta.models.music_vae import music_vae_train, configs

def main(unused_argv):
    # Modello SMALL: Stabile, leggero e veloce
    config_name = 'cat-drums_2bar_small' 
    
    if config_name not in configs.CONFIG_MAP:
        sys.exit(1)
        
    tf.app.flags.FLAGS.config = config_name
    config = configs.CONFIG_MAP[config_name]
    
    # Configurazione ottimale per modello small
    config.hparams.batch_size = 16 

    print(f"\\n[OK] Avvio Training Standard (Modello SMALL).")
    print(f"[INFO] Spazio su disco monitorato: i checkpoint saranno leggeri.")
    print("-" * 40)

    try:
        # Avviamo senza patch esterne per evitare errori di variabili
        music_vae_train.run(configs.CONFIG_MAP)
    except Exception as e:
        print(f"\\n ERRORE: {e}")
        sys.exit(1)

if __name__ == "__main__":
    tf.disable_v2_behavior()
    tf.app.run(main)
'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fix_script)
    return path
def run_drums_training():
    print("\n" + "="*60)
    print("AVVIO TRAINING BATTERIA METALLICA (RISPARMIO DISCO)")
    print("="*60)

    # Nota: Assicurati di usare il file TFRecord rigenerato/pulito
    DRUMS_TFRECORD = os.path.join(TF_DATA_PATH, 'drums_ultimate.tfrecord')
    DRUMS_RUN_DIR = os.path.join(RUN_BASE_DIR, 'drums_vae_train')

    if not os.path.exists(DRUMS_TFRECORD):
        print(f"ERRORE: File {DRUMS_TFRECORD} non trovato!")
        return

    os.makedirs(DRUMS_RUN_DIR, exist_ok=True)
    fix_script = create_drums_vae_fix_script()
    
    cmd = [
        'python', fix_script,
        f'--run_dir={DRUMS_RUN_DIR}',
        f'--examples_path={DRUMS_TFRECORD}',
        '--num_steps=20000' 
    ]
    
    full_command = ' '.join(cmd)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
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
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == '__main__':
    run_drums_training()
