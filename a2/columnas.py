import pandas as pd

# Ruta del archivo
archivo = r'C:\simon\pasantia\a2\DIRECCIONES DE vTEX.xlsx'

# Lee el archivo .xlsx
df = pd.read_excel(archivo)

# Muestra las columnas
print(df.columns)
