import requests

# Credenciales de VTEX (asegúrate de mantenerlas seguras)
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

def obtener_pagina(numero_pagina):
    url = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/dataentities/AD/search"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-VTEX-API-AppKey": APP_KEY,
        "X-VTEX-API-AppToken": APP_TOKEN
    }
    params = {
        "_fields": "id,createdIn",
        "_pageSize": 100,
        "_page": numero_pagina,
        "_sort": "createdIn ASC,id ASC"  # Ordenar por 'createdIn' y luego por 'id'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error al obtener datos en la página {numero_pagina}: {response.status_code}")
        print(f"Detalles del error: {response.text}")
        return []
    data = response.json()
    return data

# Inicializar el conjunto de IDs procesados
ids_procesados = set()

# Procesar páginas
page = 1
while True:
    registros_pagina = obtener_pagina(page)
    if not registros_pagina:
        print(f"No hay más registros en la página {page}.")
        break
    nuevos_ids = 0
    for registro in registros_pagina:
        id_registro = registro['id']
        if id_registro not in ids_procesados:
            ids_procesados.add(id_registro)
            nuevos_ids += 1
            # Aquí puedes procesar el registro según necesites

    print(f"Páginas procesadas: {page}, Nuevos IDs en esta página: {nuevos_ids}, Total de IDs únicos: {len(ids_procesados)}")

    page += 1

print(f"Total de IDs únicos obtenidos: {len(ids_procesados)}")
