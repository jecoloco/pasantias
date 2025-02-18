import pandas as pd

# Cargar el archivo Excel
import os

file_path = "C:/simon/pasantia/a2/DIRECCIONES DE vTEX.xlsx"  # O usa las barras invertidas
if os.path.exists(file_path):
    print("El archivo existe")
else:
    print("El archivo no se encuentra en la ruta especificada")
 # Ajusta la ruta correcta  # Cambia la ruta al archivo real
df = pd.read_excel(file_path)

# Mostrar las primeras filas para inspección
print("Primeras filas del archivo:")
print(df.head())

# Filtrar las filas con valores erróneos (nulos o vacíos) en cualquier columna
errores = df[df.isnull().any(axis=1)]

# Mostrar todas las filas erradas
print("\nDirecciones filtradas (con errores):")
print(errores)

# Mostrar estadísticas básicas de las filas filtradas
print(df_filtradas.describe())

