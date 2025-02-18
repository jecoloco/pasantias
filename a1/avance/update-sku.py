import http.client
import json
import ssl

# Configuración
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Leer el archivo sku-completo.json
with open("sku-completo.json", "r", encoding="utf-8") as file:
    productos = json.load(file)

# Conexión HTTPS
context = ssl._create_unverified_context()

# Cabeceras para la API de VTEX
headers = {
    'X-VTEX-API-AppKey': APP_KEY,
    'X-VTEX-API-AppToken': APP_TOKEN,
    'Content-Type': 'application/json'
}

# Limitar a los primeros 5 productos para las pruebas
productos_prueba = productos[:290]

# Actualizar los SKUs
for producto in productos_prueba:
    sku_id = producto["Id"]
    sku_name = producto["name"]
    product_id = producto["ProductID"]  # Usar ProductID correctamente

    # Datos para actualizar el SKU (activar)
    data = {
        "Id": sku_id,
        "ProductId": product_id,  # Incluir el ProductId correctamente
        "IsActive": True,  # ACTIVAR EL SKU
        "Name": sku_name  # ACTUALIZAR EL NOMBRE
    }

    # Conexión HTTPS para cada SKU
    conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

    # Enviar la solicitud PUT
    conn.request("PUT", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", body=json.dumps(data), headers=headers)

    # Respuesta
    res = conn.getresponse()
    response_data = res.read().decode()

    if res.status == 200:
        print(f"✅ SKU {sku_id} actualizado correctamente.")
    else:
        print(f"❌ Error al actualizar SKU {sku_id}: {response_data}")

    conn.close()

print("✅ Proceso de actualización de los primeros 5 productos completado.")
