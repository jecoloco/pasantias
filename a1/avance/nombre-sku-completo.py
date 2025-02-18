import json
import pandas as pd

# Cargar el archivo JSON
with open("nombre-sku.json", "r", encoding="utf-8") as file:
    productos_json = json.load(file)

# Cargar el archivo Excel
excel_data = pd.read_excel("Unidad de Medida Cambios.xlsx")

# Crear un diccionario para acceder fácilmente a los valores de la columna B usando el "Id" de la columna A
excel_dict = dict(zip(excel_data['A'], excel_data['B']))

# Recorrer los productos en el JSON y actualizar el nombre
for producto in productos_json:
    producto_id = int(producto['Id'])  # Asegurarse de que el "Id" sea un entero
    if producto_id in excel_dict:
        producto['name'] = excel_dict[producto_id]  # Actualizar solo el atributo "name"

# Guardar el resultado en un nuevo archivo JSON
with open("sku-completo.json", "w", encoding="utf-8") as outfile:
    json.dump(productos_json, outfile, ensure_ascii=False, indent=4)

print("✅ El archivo sku-completo.json ha sido generado correctamente.")
