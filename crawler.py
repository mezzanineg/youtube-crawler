from pytube import Channel, YouTube
import os

# Imposta qui il link al canale
channel_url = "https://www.youtube.com/@spot80tv"

# Cartelle per video e audio
video_path = "./video_bassa_qualita/video"
audio_path = "./video_bassa_qualita/audio"

os.makedirs(video_path, exist_ok=True)
os.makedirs(audio_path, exist_ok=True)

channel = Channel(channel_url)
print(f"Scarico {len(channel.video_urls)} video dal canale: {channel.channel_name}")

for url in channel.video_urls:
    try:
        yt = YouTube(url)
        safe_title = "".join(c if c.isalnum() else "_" for c in yt.title)[:50]
        print(f"Scaricando: {yt.title}")

        # Video solo video
        video_stream = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').first()
        if video_stream:
            video_stream.download(output_path=video_path, filename=f"{safe_title}_video.mp4")

        # Solo audio
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio_stream:
            audio_stream.download(output_path=audio_path, filename=f"{safe_title}_audio.mp4")

    except Exception as e:
        print(f"Errore con {url}: {e}")