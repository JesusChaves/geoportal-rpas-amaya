import pandas as pd

SHEET_ID = '1Vy5PuzBZwBlg4r4mIK98eX0_NfDpTTRVkxvXL_tVGuw'
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

df = pd.read_csv(CSV_URL)

# Imprime las columnas exactas del CSV
print("COLUMNAS ENCONTRADAS:", df.columns.tolist())
