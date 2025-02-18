import requests
import json

# Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# URL de la API de VTEX
base_url = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/dataentities/AD/search"

# Parámetros de la solicitud
params = {
    "_page": 1,
    "_pageSize": 100
}

# Encabezados para la autenticación
headers = {
    "X-VTEX-API-AppKey": APP_KEY,
    "X-VTEX-API-AppToken": APP_TOKEN,
    "User-Agent": "Mozilla/5.0"  # Puede ser cualquier cadena válida
}

# Nombre del archivo donde se guardarán las direcciones
output_file = "addresses.json"

# Función para realizar la solicitud y procesar los datos
def fetch_addresses():
    addresses = []
    page = 1

    while True:
        print(f"Solicitando datos de: {base_url}?_page={page}&_pageSize=100")

        # Realizar la solicitud GET
        response = requests.get(base_url, headers=headers, params={**params, "_page": page})

        if response.status_code == 200:
            data = response.json()
            if not data:
                print("No se encontraron más direcciones.")
                break
            addresses.extend(data)  # Agregar los datos obtenidos a la lista de direcciones
            print(f"Se han encontrado {len(data)} direcciones en la página {page}.")
            page += 1  # Incrementar el número de página para la siguiente solicitud
        else:
            print(f"Error al solicitar datos en la página {page}. Código de estado: {response.status_code}")
            print(f"Respuesta completa: {response.text}")
            break

    # Guardar las direcciones en un archivo JSON
    if addresses:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(addresses, file, ensure_ascii=False, indent=4)
        print(f"Se han guardado {len(addresses)} direcciones en el archivo '{output_file}'.")
    else:
        print("No se encontraron direcciones.")

# Llamar a la función para obtener las direcciones
fetch_addresses()
