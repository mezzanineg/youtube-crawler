import subprocess
import os
import argparse

def transcribe_audio(file_path, txt_folder, high_quality):
    try:
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        base_command = [
            "whisper", file_path,
            "--language", "Italian",
            "--model", "large",
            "--task", "transcribe",
            "--fp16", "False"
        ]

        if high_quality:
            base_command += [
                "--temperature", "0.2",
                "--beam_size", "5",
                "--best_of", "5"
            ]

        # Genera file .txt
        txt_command = base_command + ["--output_format", "txt", "--output_dir", txt_folder]
        subprocess.run(txt_command, check=True)

        # Genera file .vtt
       # vtt_command = base_command + ["--output_format", "vtt", "--output_dir", vtt_folder]
        #subprocess.run(vtt_command, check=True)

        print(f"✅ Trascrizione completata per: {file_name}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Errore durante la trascrizione di {file_path}: {e}")

def process_audio_files(anno, high_quality):
    audio_folder = f"audio/{anno}"
    txt_folder = f"trascrizioni/{anno}/txt"
   # vtt_folder = f"trascrizioni/{anno}/vtt"

    os.makedirs(txt_folder, exist_ok=True)
   # os.makedirs(vtt_folder, exist_ok=True)

    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

    if not audio_files:
        print("❌ Nessun file audio trovato.")
        return

    print(f"🎙️ Inizio trascrizione ({'alta qualità' if high_quality else 'standard'}) per {len(audio_files)} file...")

    for audio_file in audio_files:
        audio_path = os.path.join(audio_folder, audio_file)
        transcribe_audio(audio_path, txt_folder, high_quality)

    print("✅ Tutte le trascrizioni completate.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trascrizione audio con Whisper")
    parser.add_argument("anno", help="Anno della cartella (es. 1980)")
    parser.add_argument("--hq", action="store_true", help="Attiva la modalità alta qualità")

    args = parser.parse_args()
    process_audio_files(args.anno, args.hq)
