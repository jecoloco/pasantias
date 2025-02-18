import http.client
import json

# Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Rango de precios
PRICE_FROM = 100
PRICE_TO = 110

# Configuración de conexión
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br")

# Encabezados de la solicitud
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-VTEX-API-AppKey": APP_KEY,
    "X-VTEX-API-AppToken": APP_TOKEN
}

# Función para extraer el precio de un producto
def extract_price(product):
    try:
        if "items" in product and product["items"]:
            first_item = product["items"][0]  # Tomar el primer ítem del producto
            if "sellers" in first_item and first_item["sellers"]:
                seller = first_item["sellers"][0]  # Tomar el primer vendedor
                if "commertialOffer" in seller and "Price" in seller["commertialOffer"]:
                    return seller["commertialOffer"]["Price"]
    except Exception as e:
        print(f"Error al extraer precio de {product.get('productName', 'Desconocido')}: {e}")

    return "N/A"  # Si no se encuentra el precio, devolver "N/A"

# Función para obtener productos por rango de precio
def get_products_by_price_range():
    page = 1
    all_products = []

    while True:
        # Endpoint con parámetros de paginación
        endpoint = f"/api/catalog_system/pub/products/search?_from={(page-1)*20}&_to={page*20}"

        # Realizar la solicitud GET
        conn.request("GET", endpoint, headers=headers)

        # Obtener la respuesta
        res = conn.getresponse()
        data = res.read()

        # Convertir la respuesta a JSON
        try:
            products = json.loads(data.decode("utf-8"))
            if isinstance(products, str):
                print("La respuesta no es JSON:", products)
                break
        except json.JSONDecodeError:
            print("Error al convertir la respuesta a JSON.")
            break

        # Si no hay productos, salir del bucle
        if not products:
            break

        # Filtrar los productos con el precio correcto
        filtered_products = []
        for product in products:
            price = extract_price(product)
            if PRICE_FROM <= price <= PRICE_TO:
                filtered_products.append({
                    "productId": product["productId"],
                    "productName": product["productName"],
                    "value": price
                })

        # Agregar a la lista de productos filtrados
        all_products.extend(filtered_products)

        # Verificar si se llegó al límite de VTEX (2500)
        if (page * 20) >= 2500:
            print("⚠️ Límite de 2500 productos alcanzado en VTEX.")
            break

        # Incrementar el número de página
        page += 1

    return all_products

# Obtener los productos filtrados
products = get_products_by_price_range()

# Guardar la respuesta filtrada en un archivo JSON
file_name = "productos_por_rango_de_precio.json"
with open(file_name, "w", encoding="utf-8") as file:
    json.dump(products, file, indent=2, ensure_ascii=False)

print(f"✅ Los productos filtrados por precio se han guardado en '{file_name}' correctamente.")
