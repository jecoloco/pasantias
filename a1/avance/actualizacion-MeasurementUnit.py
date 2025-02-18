import http.client
import json
import ssl

# Configuración de las credenciales y URL
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Crear la conexión HTTPS con el host de VTEX
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

# Obtener todos los SKUs
conn.request("GET", "/api/catalog_system/pvt/sku/stockkeepingunitids", headers={
    'X-VTEX-API-AppKey': APP_KEY,
    'X-VTEX-API-AppToken': APP_TOKEN
})
res = conn.getresponse()
sku_ids = json.loads(res.read().decode("utf-8"))

# Recorrer cada SKU
for sku_id in sku_ids:
    # Obtener detalles del producto
    conn.request("GET", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", headers={
        'X-VTEX-API-AppKey': APP_KEY,
        'X-VTEX-API-AppToken': APP_TOKEN
    })
    res = conn.getresponse()
    product_data = json.loads(res.read().decode("utf-8"))

    # Verificar si el producto tiene los atributos necesarios
    if all(k in product_data for k in ['MeasurementUnit', 'ProductId', 'Name', 'IsActive']):
        measurement_unit = product_data['MeasurementUnit']
        
        # Filtrar productos con unidad "Metro Cubico" o "Metro Cuadrado"
        if measurement_unit in ["Metro Cubico", "Metro Cuadrado"]:
            product_id = product_data['ProductId']
            product_name = product_data['Name']
            is_active = product_data['IsActive']

            print(f"✅ Actualizando SKU {sku_id} - {product_name} ({measurement_unit})")

            # Crear payload manteniendo el estado de "IsActive"
            payload = json.dumps({
                "MeasurementUnit": "un",  # Nuevo valor
                "ProductId": product_id,
                "Name": product_name,
                "IsActive": is_active  # Se mantiene igual
            })

            # Realizar la solicitud PUT para actualizar el SKU
            conn.request("PUT", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", payload, headers={
                'Content-Type': "application/json",
                'X-VTEX-API-AppKey': APP_KEY,
                'X-VTEX-API-AppToken': APP_TOKEN
            })

            # Obtener la respuesta del servidor
            res = conn.getresponse()
            print(f"🔄 Respuesta: {res.status} {res.reason}")
    else:
        print(f"⚠️ No se pudieron obtener los datos del SKU {sku_id}")

# Cerrar conexión
conn.close()
