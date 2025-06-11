import os
import pandas as pd

# Cartella principale
base_dir = 'audio'

# Lista per i dati
data = []

# Esplora le sottocartelle
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.mp3'):
            anno = os.path.basename(root)
            data.append({
                'Anno': int(anno),
                'Nome file': file
            })

# Crea DataFrame
df = pd.DataFrame(data)

# Ordina per anno (crescente) e nome file (alfabetico)
df.sort_values(by=['Anno', 'Nome file'], inplace=True)

# Salva in Excel
df.to_excel('elenco_file_audio.xlsx', index=False)

print("File Excel creato con successo: elenco_file_audio.xlsx")
