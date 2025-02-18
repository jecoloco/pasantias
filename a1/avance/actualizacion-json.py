import http.client
import json
import ssl

# Configuración de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Leer productos desde el archivo JSON
with open("productos_metro_filtrados.json", "r", encoding="utf-8") as file:
    productos = json.load(file)

# Crear conexión HTTPS con VTEX
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

# Recorrer productos filtrados y actualizar VTEX
for producto in productos:
    sku_id = producto.get("idSKU")
    product_id = producto.get("ProductId")
    product_name = producto.get("Name")
    is_active = producto.get("IsActive")  # Mantener el estado actual

    if not sku_id or not product_id or not product_name:
        print(f"⚠️ Producto sin datos completos: {producto}")
        continue

    print(f"✅ Actualizando SKU {sku_id} - {product_name}")

    # Crear payload para actualizar VTEX
    payload = json.dumps({
        "MeasurementUnit": "un",  # Nuevo valor
        "ProductId": product_id,
        "Name": product_name,
        "IsActive": is_active  # Se mantiene igual
    })

    # Hacer la solicitud PUT para actualizar en VTEX
    conn.request("PUT", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", payload, headers={
        'Content-Type': "application/json",
        'X-VTEX-API-AppKey': APP_KEY,
        'X-VTEX-API-AppToken': APP_TOKEN
    })

    # Obtener la respuesta del servidor
    res = conn.getresponse()
    print(f"🔄 Respuesta: {res.status} {res.reason}")

# Cerrar conexión
conn.close()
