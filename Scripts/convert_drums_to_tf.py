import os
import subprocess

# --- INSERISCI PERCORSI ---
MIDI_INPUT_DIR = ""
TFRECORD_OUTPUT = ""

def create_new_tfrecord():
    print("--- GENERAZIONE NUOVO TFRECORD DAI MIDI ---")
    
    if not os.path.exists(MIDI_INPUT_DIR):
        print(f"ERRORE: La cartella MIDI non esiste: {MIDI_INPUT_DIR}")
        return

    # Comando Magenta per convertire i MIDI in NoteSequences
    # Usiamo direttamente il modulo note_seq che è più moderno
    cmd = [
        'convert_dir_to_note_sequences',
        f'--input_dir={MIDI_INPUT_DIR}',
        f'--output_file={TFRECORD_OUTPUT}',
        '--recursive'
    ]
    
    print(f"Eseguo: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"\n[SUCCESSO] Creato nuovo file: {TFRECORD_OUTPUT}")
        print("Ora puoi avviare il training usando questo file.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRORE] Durante la conversione: {e}")

if __name__ == "__main__":
    create_new_tfrecord()
