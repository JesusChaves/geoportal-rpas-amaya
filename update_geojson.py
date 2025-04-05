import pandas as pd

SHEET_ID = '1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

df = pd.read_csv(CSV_URL)

# Imprime claramente las columnas del CSV y fuerza una salida de error inmediata
print("\n--- COLUMNAS EXACTAS DEL CSV ---")
for col in df.columns:
    print(f"'{col}'")

# Provoca un error a propósito para detener aquí
raise Exception("Detenido a propósito para ver columnas")
