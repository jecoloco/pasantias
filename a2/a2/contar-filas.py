import json

# Ruta del archivo JSON
archivo_json = r"C:\simon\a2\multicenter_AD.json"

# Cargar el archivo JSON y contar los objetos
try:
    with open(archivo_json, "r", encoding="utf-8") as file:
        data = json.load(file)  # Cargar el JSON como lista de diccionarios
    
    cantidad_objetos = len(data)  # Contar elementos en la lista
    print(f"El archivo JSON contiene {cantidad_objetos} objetos.")
except Exception as e:
    print(f"Error al leer el archivo JSON: {e}")
