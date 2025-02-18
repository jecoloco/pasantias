import requests
import json

# 🔑 Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# URL del endpoint para obtener categorías
URL = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/catalog_system/pub/category/tree/10"

# Encabezados con autenticación
HEADERS = {
    "X-VTEX-API-AppKey": APP_KEY,
    "X-VTEX-API-AppToken": APP_TOKEN,
    "Accept": "application/json"
}

# Realizar la solicitud GET
response = requests.get(URL, headers=HEADERS)

# Verificar si la respuesta es correcta
if response.status_code == 200:
    categorias = response.json()
    
    # Guardar en un archivo JSON
    with open("categorias.json", "w", encoding="utf-8") as json_file:
        json.dump(categorias, json_file, ensure_ascii=False, indent=4)
    
    print("Categorías guardadas en 'categorias.json'")
else:
    print(f"Error {response.status_code}: {response.text}")
