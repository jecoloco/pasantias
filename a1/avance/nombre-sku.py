import json
import requests

# Credenciales VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Cabeceras para la API de VTEX
HEADERS = {
    "X-VTEX-API-AppKey": APP_KEY,
    "X-VTEX-API-AppToken": APP_TOKEN,
    "Content-Type": "application/json"
}

# Ruta de la API para obtener los SKUs por ProductID
BASE_URL = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/catalog_system/pvt/sku/stockkeepingunitByProductId/"

# Leer archivo 290.json
with open("290.json", "r", encoding="utf-8") as file:
    productos = file.readlines()

resultado = []

for linea in productos:
    if "Producto encontrado:" in linea:
        partes = linea.split(", ")
        product_id = partes[0].split(": ")[1]  # Extraer el ID del producto
        product_name = partes[1]  # Extraer el nombre del producto

        # Llamar a la API de VTEX para obtener los SKUs
        url = BASE_URL + product_id
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            skus = response.json()
            for sku in skus:
                resultado.append({
                    "Id": sku["Id"],  # ID del SKU
                    "ProductID": product_id,  # ID del producto
                    "name": sku["Name"],  # Nombre del SKU
                    "ProductName": product_name,  # Nombre del producto
                    "IsActive": sku["IsActive"]  # Estado de activación del SKU
                })
        else:
            print(f"⚠️ No se pudo obtener SKUs para el producto {product_id}")

# Guardar los datos en nombre-sku.json
with open("nombre-sku.json", "w", encoding="utf-8") as outfile:
    json.dump(resultado, outfile, ensure_ascii=False, indent=4)

print("✅ Archivo nombre-sku.json generado correctamente.")
