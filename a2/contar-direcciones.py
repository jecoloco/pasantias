import requests

# Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

def obtener_total_direcciones():
    url = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/dataentities/AD/search"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-VTEX-API-AppKey": APP_KEY,
        "X-VTEX-API-AppToken": APP_TOKEN
    }
    params = {
        "_fields": "id",
        "_page": 1,
        "_pageSize": 1  # Solicitamos solo un registro
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        # Obtenemos el encabezado 'REST-Content-Range'
        content_range = response.headers.get("REST-Content-Range")
        if content_range:
            # El formato es 'resources X-Y/Z', por ejemplo 'resources 0-0/131520'
            total_count = int(content_range.split('/')[-1])
            print(f"Total de direcciones registradas: {total_count}")
        else:
            print("No se pudo obtener el total de direcciones. El encabezado 'REST-Content-Range' no está presente.")
    else:
        print(f"Error al realizar la solicitud: {response.status_code} - {response.text}")

obtener_total_direcciones()
