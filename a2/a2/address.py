import requests
import json

# Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# URL de la API de VTEX
url = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/dataentities/AD/search"

# Cabeceras para autenticación
headers = {
    'Accept': "application/vnd.vtex.ds.v10+json",
    'Content-Type': "application/json",
    'X-VTEX-API-AppKey': APP_KEY,
    'X-VTEX-API-AppToken': APP_TOKEN
}

# Función para obtener direcciones
def get_addresses():
    page = 1
    page_size = 100  # Tamaño de la página
    all_addresses = []

    while True:
        full_url = f"{url}?_page={page}&_pageSize={page_size}"

        # Realizar la solicitud GET a la API usando requests
        response = requests.get(full_url, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code != 200:
            print(f"❌ Error al conectar con la API: {response.status_code}")
            print(f"🛑 Mensaje de error: {response.text}")
            break

        data = response.json()
        if not data:
            print("✅ Todos los datos han sido recuperados.")
            break

        all_addresses.extend(data)

        # Verificar si la respuesta contiene menos de 'page_size' elementos
        # Esto indica que hemos llegado al final de los datos
        if len(data) < page_size:
            print(f"✅ Se han recuperado todos los registros.")
            break

        page += 1  # Incrementar el número de página para la siguiente solicitud

    return all_addresses

# Obtener direcciones y guardar en un archivo JSON
def main():
    addresses = get_addresses()
    if addresses:
        print(f"Se han recuperado {len(addresses)} direcciones.")
        with open('addresses.json', 'w', encoding='utf-8') as file:
            json.dump(addresses, file, indent=4, ensure_ascii=False)
        print("Direcciones guardadas en 'addresses.json'")
    else:
        print("⚠️ No se encontraron direcciones.")

if __name__ == "__main__":
    main()
