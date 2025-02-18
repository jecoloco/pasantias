import http.client
import json
import ssl

# Configuración de las credenciales y URL
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"
sku_id = "44449"  # El SKU que deseas actualizar

# Crear la conexión HTTPS con el host de VTEX
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

# Hacer una solicitud GET para obtener el estado actual del SKU
conn.request("GET", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", headers={
    'X-VTEX-API-AppKey': APP_KEY,
    'X-VTEX-API-AppToken': APP_TOKEN
})

res = conn.getresponse()
data = res.read()

# Convertir la respuesta a JSON
product_data = json.loads(data.decode("utf-8"))

# Verificar si recibimos correctamente los datos necesarios
if 'ProductId' in product_data and 'Name' in product_data and 'IsActive' in product_data:
    product_id = product_data['ProductId']
    product_name = product_data['Name']
    is_active = product_data['IsActive']  # Obtener el estado actual

    print(f"ProductId: {product_id}")
    print(f"Product Name: {product_name}")
    print(f"IsActive actual: {is_active}")

    # Ahora, hacer la solicitud PUT para actualizar el SKU manteniendo IsActive
    payload = json.dumps({
        "MeasurementUnit": "un",  # Modificamos solo este atributo
        "ProductId": product_id,
        "Name": product_name,
        "IsActive": is_active  # Mantiene el valor actual de IsActive
    })

    # Realizar la solicitud PUT para actualizar el SKU
    conn.request("PUT", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", payload, headers={
        'Content-Type': "application/json",
        'X-VTEX-API-AppKey': APP_KEY,
        'X-VTEX-API-AppToken': APP_TOKEN
    })

    # Obtener la respuesta del servidor
    res = conn.getresponse()
    data = res.read()

    # Mostrar la respuesta del servidor
    print(data.decode("utf-8"))
else:
    print("❌ No se pudo obtener ProductId, Nombre o IsActive del producto.")
