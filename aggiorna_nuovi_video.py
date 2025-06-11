import subprocess
import os
import sys
from pathlib import Path

def check_yt_dlp():
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Errore: yt-dlp non è installato. Installalo con:\npip install -U yt-dlp")
        sys.exit(1)

def convert_vtt_to_txt(vtt_path, txt_path):
    with open(vtt_path, "r", encoding="utf-8") as vtt_file, open(txt_path, "w", encoding="utf-8") as txt_file:
        for line in vtt_file:
            line = line.strip()
            if not line or "-->" in line or line.isdigit() or line.startswith("WEBVTT"):
                continue
            if line.startswith("♪") and line.endswith("♪"):
                continue  # esclude eventuali note musicali
            txt_file.write(line + "\n")

def aggiorna_nuovi_video():
    channel_url = "https://www.youtube.com/@spot80tv"
    archive_file = "scaricati.txt"

    video_folder = Path("video/nuovi")
    audio_folder = Path("audio/nuovi")
    subs_folder = Path("trascrizioni/nuovi")

    video_folder.mkdir(parents=True, exist_ok=True)
    audio_folder.mkdir(parents=True, exist_ok=True)
    subs_folder.mkdir(parents=True, exist_ok=True)

    print("📼 Scarico nuovi video (bassa qualità)...")
    subprocess.run([
        "yt-dlp",
        "-f", "worst[ext=mp4]",
        "--download-archive", archive_file,
        "-o", f"{video_folder}/%(upload_date)s - %(title).50s.%(ext)s",
        channel_url
    ])

    print("🔊 Scarico audio dei nuovi video...")
    subprocess.run([
        "yt-dlp",
        "-f", "bestaudio",
        "-x", "--audio-format", "mp3",
        "--download-archive", archive_file,
        "-o", f"{audio_folder}/%(upload_date)s - %(title).50s.%(ext)s",
        channel_url
    ])

    print("💬 Scarico sottotitoli auto-generati (se disponibili)...")
    subprocess.run([
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "it",
        "--skip-download",
        "--convert-subs", "vtt",
        "--download-archive", archive_file,
        "-o", f"{subs_folder}/%(upload_date)s - %(title).50s.%(ext)s",
        channel_url
    ])

    for file in subs_folder.glob("*.vtt"):
        txt_path = file.with_suffix(".txt")
        convert_vtt_to_txt(file, txt_path)

    print("✅ Aggiornamento completato.")

if __name__ == "__main__":
    check_yt_dlp()
    aggiorna_nuovi_video()
