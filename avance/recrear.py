import http.client
import json
import ssl

# Configuración
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# IDs del producto
sku_id = "44852"  # ID del SKU
product_id = "44995"  # ID del producto
product_name = "Termo QUENCHER Flowstate H2.0 1,18 litros Peony Stanley"

# Crear la conexión HTTPS con VTEX
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

# 🔎 1️⃣ Verificar si el SKU existe en VTEX
conn.request("GET", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", headers={
    'X-VTEX-API-AppKey': APP_KEY,
    'X-VTEX-API-AppToken': APP_TOKEN
})

res = conn.getresponse()
data = res.read()

try:
    product_data = json.loads(data.decode("utf-8"))

    if 'ProductId' in product_data:
        print(f"✅ SKU encontrado: {sku_id} - {product_name}")
        
        # 🔄 2️⃣ Intentar restaurar el producto activándolo
        payload = json.dumps({
            "IsActive": True,  # Reactivar el SKU
            "ProductId": product_id,
            "Name": product_name,
            "MeasurementUnit": "un"
        })

        conn.request("PUT", f"/api/catalog/pvt/stockkeepingunit/{sku_id}", payload, headers={
            'Content-Type': "application/json",
            'X-VTEX-API-AppKey': APP_KEY,
            'X-VTEX-API-AppToken': APP_TOKEN
        })

        res = conn.getresponse()
        response_data = res.read()
        print("🔄 Intentando restaurar el producto:", response_data.decode("utf-8"))

    else:
        print("❌ El SKU existe, pero no tiene un ProductId válido.")

except json.JSONDecodeError:
    print("❌ El SKU no existe en VTEX. Es posible que haya sido eliminado.")

conn.close()
