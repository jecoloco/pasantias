import http.client
import json
import ssl

# Configuración
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"
sku_id = "44853"  # ID del SKU

# Conexión HTTPS
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

# Datos para actualizar el SKU (activar)
data = {
    "Id": 44853,
    "ProductId": 44996,
    "IsActive": True,  # ACTIVAR EL SKU
    "Name": "ST-1010827819"  # AGREGAR EL NOMBRE
}

headers = {
    'X-VTEX-API-AppKey': APP_KEY,
    'X-VTEX-API-AppToken': APP_TOKEN,
    'Content-Type': 'application/json'
}

# Enviar la solicitud PUT
conn.request("PUT", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", body=json.dumps(data), headers=headers)

# Respuesta
res = conn.getresponse()
print(res.status, res.read().decode())
