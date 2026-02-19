import pretty_midi
import os

# --- Configurazione ---
RAW_MIDI_DIR = 'raw_midi'
OUTPUT_DIRS = {
    'drums': 'metal_drums_midi',
    'bass': 'metal_bass_midi',
    'guitar': 'metal_guitar_midi'
}

# Range approssimativi dei Programmi MIDI per Basso e Chitarra
# (Standard MIDI General - GS/GM)
BASS_PROGRAM_RANGE = range(33, 41)  # Basso Acustico, Elettrico, Fretless, ecc.
GUITAR_PROGRAM_RANGE = range(25, 33) # Chitarra Acustica, Elettrica, Overdriven, Distorted.

# --- Funzioni di Utility ---

def setup_directories(output_dirs):
    """Crea le cartelle di output se non esistono."""
    for dirname in output_dirs.values():
        os.makedirs(dirname, exist_ok=True)
    print("Cartelle di output pronte.")

def extract_and_save_track(original_midi, track_instrument, output_path):
    """Crea un nuovo oggetto MIDI contenente solo lo strumento specificato."""
    new_midi = pretty_midi.PrettyMIDI(initial_tempo=original_midi.estimate_tempo())
    new_midi.instruments.append(track_instrument)
    new_midi.write(output_path)

def analyze_and_split_midi(midi_path):
    """Analizza un file MIDI e salva le tracce separate."""
    try:
        midi = pretty_midi.PrettyMIDI(midi_path)
    except Exception as e:
        print(f"Errore nella lettura di {midi_path}: {e}")
        return

    # Contenitori per le tracce separate per questo brano
    separated_tracks = {key: [] for key in OUTPUT_DIRS.keys()}
    
    # 1. Analisi Strumenti
    for instrument in midi.instruments:
        
        # A. Traccia Batteria (MIDI Channel 10)
        if instrument.is_drum:
            separated_tracks['drums'].append(instrument)
            
        # B. Traccia Basso
        elif instrument.program in BASS_PROGRAM_RANGE:
            separated_tracks['bass'].append(instrument)
            
        # C. Traccia Chitarra
        elif instrument.program in GUITAR_PROGRAM_RANGE:
            separated_tracks['guitar'].append(instrument)
            
    # 2. Salvataggio
    base_name = os.path.basename(midi_path)

    for track_type, instruments in separated_tracks.items():
        if instruments:
            # Crea un singolo file MIDI per ogni tipo di strumento
            
            # Se ci sono più strumenti dello stesso tipo (es. 2 chitarre), li uniamo
            # In MMM, questo sarebbe stato gestito, qui li salviamo come polifonici
            
            output_dir = OUTPUT_DIRS[track_type]
            output_path = os.path.join(output_dir, f"{track_type}_{base_name}")
            
            # Crea un nuovo oggetto MIDI per il salvataggio
            new_midi = pretty_midi.PrettyMIDI(initial_tempo=midi.estimate_tempo())
            for inst in instruments:
                new_midi.instruments.append(inst)

            try:
                new_midi.write(output_path)
                print(f"  -> Salvato traccia {track_type} in {output_path}")
            except Exception as e:
                print(f"  -> ERRORE di scrittura per {track_type} su {base_name}: {e}")


# --- Esecuzione Principale ---
if __name__ == "__main__":
    setup_directories(OUTPUT_DIRS)
    
    # Itera su tutti i file MIDI nella cartella raw_midi
    for filename in os.listdir(RAW_MIDI_DIR):
        if filename.endswith(('.mid', '.midi')):
            full_path = os.path.join(RAW_MIDI_DIR, filename)
            print(f"Processo: {filename}")
            analyze_and_split_midi(full_path)
            
    print("\n Processo di separazione completato.")
