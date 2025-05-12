# YouTube Crawler e Trascrizione Audio

# 🎞️ YouTube Spot Crawler & Transcriber

Un progetto Python per:
- 🕵️‍♀️ Scaricare video da un canale YouTube specifico
- 🔉 Estrarre tracce audio
- 🧠 Trascrivere con Whisper (in italiano)
- ✍️ Correggere e migliorare automaticamente le trascrizioni con GPT-4

---

## 📝 Funzionalità

1. **Scaricamento Video e Audio**: scarica i video e audio da un canale YouTube specificato.
2. **Filtraggio per Titolo**: è possibile scaricare solo i video che contengono una determinata stringa nel titolo (es. `(1978)`).
3. **Trascrizione Audio**: trascrive automaticamente i file audio `.mp3` in formato testo utilizzando il modello Whisper di OpenAI.
4. **Miglioramento delle trascrizioni**: Rivede il testo trascritto e prova a correggere eventuali errori

## 📦 Requisiti

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) installato nel sistema
- Una chiave API OpenAI (per la correzione)

---

## ⚙️ Installazione

Clona il repository e crea un ambiente virtuale:

```bash
git clone https://github.com/tuo-utente/youtube-crawler.git
cd youtube-crawler
python3 -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate su Windows
pip install -r requirements.txt