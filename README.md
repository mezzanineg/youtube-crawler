# YouTube Crawler e Trascrizione Audio

Questo progetto è un **crawler YouTube** che estrae i video da un canale e scarica i file audio e video. Inoltre, esegue la **trascrizione automatica** dei file audio in formato `.txt` utilizzando **Whisper di OpenAI**.

## 📝 Funzionalità

1. **Scaricamento Video e Audio**: scarica i video e audio da un canale YouTube specificato.
2. **Filtraggio per Titolo**: è possibile scaricare solo i video che contengono una determinata stringa nel titolo (es. `(1978)`).
3. **Trascrizione Audio**: trascrive automaticamente i file audio `.mp3` in formato testo utilizzando il modello Whisper di OpenAI.

## ⚙️ Requisiti

- Python 3.7 o superiore
- `yt-dlp` per il download dei video e audio
- `whisper` per la trascrizione dei file audio

## 📦 Installazione

1. Clona questo repository:

   ```bash
   git clone https://github.com/mezzanineg/youtube-crawler.git
   cd youtube-crawler
