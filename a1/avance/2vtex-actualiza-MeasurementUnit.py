import http.client
import json
import ssl
import time

# Configuración de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Leer productos desde el archivo JSON
with open("productos_metro_filtrados.json", "r", encoding="utf-8") as file:
    productos = json.load(file)

# Limitar a los primeros 5 productos
productos_a_actualizar = productos[:150]

# Crear conexión HTTPS con VTEX
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

# Recorrer los primeros 5 productos filtrados y actualizar VTEX
for producto in productos_a_actualizar:
    sku_id = producto.get("idsku")  # Cambiar 'idSKU' por 'idsku'
    product_id = producto.get("id")  # Cambiar 'ProductId' por 'id'
    product_name = producto.get("nombre")  # Cambiar 'Name' por 'nombre'
    is_active = producto.get("IsActive", True)  # Mantener el estado actual, asignando un valor por defecto

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

    # Esperar a que el servidor responda adecuadamente
    try:
        # Obtener la respuesta del servidor
        res = conn.getresponse()
        # Leer el cuerpo de la respuesta
        response_body = res.read()

        print(f"🔄 Respuesta: {res.status} {res.reason}")
        print(f"Respuesta: {response_body.decode()}")  # Mostrar cuerpo de la respuesta (si es necesario)

    except Exception as e:
        print(f"⚠️ Error al obtener respuesta para SKU {sku_id}: {e}")
        time.sleep(2)  # Intentar después de un pequeño retraso

# Cerrar conexión
conn.close()


#tomar en cuenta que tiene un error, y es que modifica el "name"(nombreSKU) por el nombre del producto cosa que son atributos independientes
#tomalos datos el archivo productos_metro_filtrados.json el cual es generado por el scritpt 1filtramcuadrado-mcubico.py
