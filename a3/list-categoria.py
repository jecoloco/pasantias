import http.client
import json

# Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# ID de la categoría que quieres buscar
CATEGORY_ID = "8"  # Reemplaza con el ID real de la categoría en VTEX

# Configuración de conexión
conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br")

# Encabezados de la solicitud
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-VTEX-API-AppKey": APP_KEY,
    "X-VTEX-API-AppToken": APP_TOKEN
}

# Función para obtener productos con paginación
def get_products():
    page = 1
    all_products = []

    while True:
        # Endpoint con parámetros de paginación
        endpoint = f"/api/catalog_system/pub/products/search?fq=C:{CATEGORY_ID}&_from={(page-1)*20}&_to={page*20}"

        # Realizar la solicitud GET
        conn.request("GET", endpoint, headers=headers)

        # Obtener la respuesta
        res = conn.getresponse()
        data = res.read()

        # Verificamos el contenido de la respuesta
        print("Respuesta completa de la API:", data.decode("utf-8"))  # Depuración

        try:
            # Convertir la respuesta a JSON
            products = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("Error al convertir la respuesta a JSON.")
            break

        # Si no hay productos, salimos del bucle
        if not products:
            break

        # Filtrar solo los atributos "productId" y "productName"
        filtered_products = [{"productId": product["productId"], "productName": product["productName"]} for product in products]

        # Agregar los productos a la lista de todos los productos
        all_products.extend(filtered_products)

        # Incrementar el número de página
        page += 1

    return all_products

# Obtener todos los productos
products = get_products()

# Guardar la respuesta filtrada en un archivo JSON
file_name = "productos_categoria.json"
with open(file_name, "w", encoding="utf-8") as file:
    json.dump(products, file, indent=2, ensure_ascii=False)

print(f"✅ Los productos filtrados se han guardado en '{file_name}' correctamente.")
