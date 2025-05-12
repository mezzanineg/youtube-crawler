import subprocess
import os

# Cartella contenente gli audio da trascrivere
audio_folder = "audio/1980"
output_folder = "trascrizioni/1980"

os.makedirs(output_folder, exist_ok=True)

def transcribe_audio(file_path):
    try:
        # Nome del file senza estensione (per creare il nome del file di output)
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}.txt")

        # Esegui whisper per trascrivere l'audio in italiano
        subprocess.run([
            "whisper", file_path,
            "--language", "Italian", 
            "--model", "medium",  # Puoi scegliere il modello, small, medium, large
            "--output_dir", output_folder
        ], check=True)

        print(f"✅ Trascrizione completata per: {file_name}.txt")

    except subprocess.CalledProcessError as e:
        print(f"❌ Errore durante la trascrizione di {file_path}: {e}")

def process_audio_files():
    # Trova tutti i file .mp3 nella cartella audio
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

    if not audio_files:
        print("❌ Nessun file audio trovato.")
        return

    print(f"🔊 Inizio trascrizione per {len(audio_files)} file audio...")

    for audio_file in audio_files:
        audio_path = os.path.join(audio_folder, audio_file)
        transcribe_audio(audio_path)

    print("✅ Trascrizione completata per tutti i file audio.")

if __name__ == "__main__":
    process_audio_files()