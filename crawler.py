import subprocess
import os
import sys

def check_yt_dlp():
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Errore: yt-dlp non è installato. Installalo con:\npip install -U yt-dlp")
        sys.exit(1)

def download_filtered_content(year):
    channel_url = "https://www.youtube.com/@spot80tv"
    video_folder = f"video/{year}"
    audio_folder = f"audio/{year}/"

    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)

    title_filter = rf"\({year}\)"  # Esempio: \(1978\)

    print(f"📼 Scarico video con titolo che contiene '({year})'...")

    subprocess.run([
        "yt-dlp",
        "-f", "worst[ext=mp4]",
        "--match-title", title_filter,
        "--max-downloads", "10",
        "-o", f"{video_folder}/%(title).50s.%(ext)s",
        channel_url
    ])

    print(f"🔊 Scarico audio dei video con titolo '({year})'...")

    subprocess.run([
        "yt-dlp",
        "-f", "bestaudio",
        "-x", "--audio-format", "mp3",
        "--match-title", title_filter,
        "--max-downloads", "10",
        "-o", f"{audio_folder}/%(title).50s.%(ext)s",
        channel_url
    ])

    print(f"✅ Download completato per l'anno {year}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Errore: devi specificare un anno come argomento. Esempio:\n  python crawler.py 1978")
        sys.exit(1)

    year = sys.argv[1]
    check_yt_dlp()
    download_filtered_content(year)
