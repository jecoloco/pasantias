import pandas as pd

# Ruta del archivo CSV y JSON
archivo_csv = r"C:\simon\a2\multicenter_AD.csv"
archivo_json = r"C:\simon\a2\multicenter_AD.json"  # Cambié el nombre para reflejar que ya no está filtrado

# Intentar detectar automáticamente el delimitador
try:
    df = pd.read_csv(archivo_csv, dtype=str, sep=None, engine='python', encoding="utf-8")  # Detecta el delimitador automáticamente
    print("Archivo CSV cargado correctamente.")
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
    exit()

# Exportar TODAS las filas a un archivo JSON
df.to_json(archivo_json, orient="records", indent=4, force_ascii=False)

print(f"Archivo JSON exportado correctamente en: {archivo_json}")
