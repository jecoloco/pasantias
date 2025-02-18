import json

# Rutas de los archivos
archivo_json = r"C:\simon\a2\multicenter_AD.json"
archivo_filtrado = r"C:\simon\a2\filtro-street-null.json"

# Lista de valores inválidos para "street"
valores_invalidos = {"null", "nulo"}

try:
    with open(archivo_json, "r", encoding="utf-8") as file:
        data = json.load(file)  # Cargar JSON como lista de diccionarios

    # Filtrar objetos con "street" inválido
    objetos_filtrados = [
        obj for obj in data if str(obj.get("street", "")).strip().lower() in valores_invalidos
    ]

    # Exportar a JSON
    with open(archivo_filtrado, "w", encoding="utf-8") as file:
        json.dump(objetos_filtrados, file, indent=4, ensure_ascii=False)

    print(f"Archivo filtrado exportado correctamente en: {archivo_filtrado}")

except Exception as e:
    print(f"Error al procesar el archivo JSON: {e}")
