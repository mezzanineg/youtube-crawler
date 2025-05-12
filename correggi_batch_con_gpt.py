import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

# Carica le variabili d'ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("⚠️ OPENAI_API_KEY non trovata. Aggiungila nel file .env")

# Inizializza il client
client = OpenAI(api_key=api_key)

# Cartelle input/output
trascrizioni_dir = Path("trascrizioni/1980/txt")
output_dir = Path("trascrizioni/1980/corretti")
output_dir.mkdir(parents=True, exist_ok=True)

# Prompt per migliorare la trascrizione
PROMPT_BASE = """
Correggi il seguente testo trascritto automaticamente da un file audio in italiano.
Migliora la punteggiatura e correggi eventuali errori grammaticali e ortografici.
Mantieni il tono del parlato originale e NON aggiungere nulla di inventato.

Testo da correggere:
\"\"\"
{testo}
\"\"\"
"""

# Ciclo sui file di trascrizione
for file in tqdm(sorted(trascrizioni_dir.glob("*.txt")), desc="🔍 Elaborazione trascrizioni"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            testo = f.read().strip()

        prompt = PROMPT_BASE.format(testo=testo)

        response = client.chat.completions.create(
            model="gpt-4-turbo",  # cambia in "gpt-4-turbo" se hai accesso
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        testo_corretto = response.choices[0].message.content.strip()

        # Salva il testo corretto
        output_file = output_dir / file.name
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(testo_corretto)

    except Exception as e:
        print(f"❌ Errore su {file.name}: {e}")
