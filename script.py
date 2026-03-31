import pandas as pd
import json

# Leer archivo Excel
archivo = "provee.xlsx"

header_df = pd.read_excel(archivo, sheet_name="HEADER")
lines_df = pd.read_excel(archivo, sheet_name="LINES")

# Tomar la única fila de cabecera
h = header_df.iloc[0]

asiento = {
    "ReferenceDate": str(h["RefDate"])[:10],
    "DueDate": str(h["DueDate"])[:10],
    "TaxDate": str(h["TaxDate"])[:10],
    "Memo": h["Memo"],
    "Reference1": h["Ref1"],
    "JournalEntryLines": []
}

# Recorrer líneas
for _, row in lines_df.iterrows():
    linea = {
        "LineMemo": row.get("LineMemo", "")
    }

    # Cuenta o BP
    if pd.notna(row.get("ShortName")):
        linea["ShortName"] = row["ShortName"]
    else:
        linea["AccountCode"] = row["AccountCode"]

    # Importes
    if row.get("Debit", 0) > 0:
        linea["Debit"] = float(row["Debit"])

    if row.get("Credit", 0) > 0:
        linea["Credit"] = float(row["Credit"])

    asiento["JournalEntryLines"].append(linea)

# Guardar JSON
with open("asiento.json", "w") as f:
    json.dump(asiento, f, indent=4)

print("JSON listo para Service Layer 🚀")
