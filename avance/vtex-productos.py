import http.client
import json
import ssl

# Configuración
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"
sku_id = "44853"  # Cambia por el ID del SKU a verificar

# Función para hacer solicitudes a la API de VTEX
def vtex_request(endpoint):
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)
    
    conn.request("GET", endpoint, headers={
        'X-VTEX-API-AppKey': APP_KEY,
        'X-VTEX-API-AppToken': APP_TOKEN
    })
    
    res = conn.getresponse()
    data = res.read()
    conn.close()
    
    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        return None

# 1️⃣ Consultar el SKU
sku_data = vtex_request(f"/api/catalog/pvt/stockkeepingunit/{sku_id}")

if sku_data:
    product_id = sku_data.get("ProductId")
    measurement_unit = sku_data.get("MeasurementUnit")

    # 2️⃣ Consultar el Producto para obtener el nombre
    product_name = None
    if product_id:
        product_data = vtex_request(f"/api/catalog/pvt/product/{product_id}")
        product_name = product_data.get("Name") if product_data else "Desconocido"

    # 3️⃣ Mostrar la respuesta con ProductName y MeasurementUnit
    sku_data["ProductName"] = product_name
    sku_data["MeasurementUnit"] = measurement_unit

    print("✅ SKU encontrado:", json.dumps(sku_data, indent=4, ensure_ascii=False))
else:
    print("❌ El SKU no existe en VTEX.")
