import subprocess
import os
import sys
from pathlib import Path
import re

def check_yt_dlp():
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Errore: yt-dlp non è installato. Installalo con:\npip install -U yt-dlp")
        sys.exit(1)

def convert_vtt_to_txt(vtt_path, txt_path):
    lines = []
    last_line = ""

    with open(vtt_path, "r", encoding="utf-8") as vtt_file:
        for line in vtt_file:
            line = line.strip()

            # Salta intestazioni, timestamp e markup
            if (
                not line
                or line.startswith("WEBVTT")
                or re.match(r"\d{2}:\d{2}:\d{2}\.\d{3}", line)
                or "-->" in line
                or re.match(r"<[0-9:.]+><c>", line)
            ):
                continue

            # Rimuove markup inline come <...>
            clean_line = re.sub(r"<[^>]+>", "", line)

            # Evita duplicati consecutivi
            if clean_line != last_line:
                lines.append(clean_line)
                last_line = clean_line

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write("\n".join(lines))

def download_filtered_content(year):
    channel_url = "https://www.youtube.com/@spot80tv"
    title_filter = rf"\({year}\)"

    video_folder = Path(f"video/{year}")
    audio_folder = Path(f"audio/{year}")
    subs_folder = Path(f"trascrizioni/{year}")

    video_folder.mkdir(parents=True, exist_ok=True)
    audio_folder.mkdir(parents=True, exist_ok=True)
    subs_folder.mkdir(parents=True, exist_ok=True)

    print(f"📼 Scarico video con titolo che contiene '({year})'...")

    subprocess.run([
        "yt-dlp",
        "-f", "worst[ext=mp4]",
        "--match-title", title_filter,
        "--max-downloads", "500",
        "-o", f"{video_folder}/%(title).50s.%(ext)s",
        channel_url
    ])

    print(f"🔊 Scarico audio dei video con titolo '({year})'...")

    subprocess.run([
        "yt-dlp",
        "-f", "bestaudio",
        "-x", "--audio-format", "mp3",
        "--match-title", title_filter,
        "--max-downloads", "500",
        "-o", f"{audio_folder}/%(title).50s.%(ext)s",
        channel_url
    ])

    print(f"💬 Scarico sottotitoli auto-generati (se disponibili)...")

    subprocess.run([
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", "it",
        "--skip-download",
        "--convert-subs", "vtt",
        "--match-title", title_filter,
        "--max-downloads", "500",
        "-o", f"{subs_folder}/%(title).50s.%(ext)s",
        channel_url
    ])

    # Conversione da .vtt a .txt
    for file in subs_folder.glob("*.vtt"):
        txt_path = file.with_suffix(".txt")
        convert_vtt_to_txt(file, txt_path)

    print(f"✅ Download completato per l'anno {year}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Errore: devi specificare un anno come argomento. Esempio:\n  python crawler.py 1978")
        sys.exit(1)

    year = sys.argv[1]
    check_yt_dlp()
    download_filtered_content(year)
