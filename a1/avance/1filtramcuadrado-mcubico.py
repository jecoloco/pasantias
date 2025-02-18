import requests
import json
import os
import time

# Credenciales
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Función para obtener todos los productos y filtrar por 'measurementUnit' == 'Metro Cubico' o 'Metro Cuadrado'
def get_products_by_measurement_unit():
    all_products = []
    step = 50  
    start = 0  

    while True:
        # Endpoint
        API_URL = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/catalog_system/pub/products/search?_from={start}&_to={start + step - 1}"
        print(f"🔄 Consultando productos {start} - {start + step - 1}...")

        try:
            response = requests.get(API_URL, headers={
                'X-VTEX-API-AppKey': APP_KEY,
                'X-VTEX-API-AppToken': APP_TOKEN
            }, timeout=10)
            
            response.raise_for_status()  
            products_data = response.json()

            # Si la respuesta está vacía, terminamos la iteración
            if not products_data:
                print("✅ No hay más productos para consultar.")
                break

            for product_data in products_data:
                product_id = product_data.get('productId', 'No disponible')
                product_name = product_data.get('productName', 'No disponible')

                # Revisamos si el producto tiene variantes (SKUs)
                items = product_data.get('items', [])
                for item in items:
                    measurement_unit = item.get('measurementUnit', 'No disponible')
                    id_sku = item.get('itemId', 'No disponible')

                    if measurement_unit in ['Metro Cubico', 'Metro Cuadrado']:
                        all_products.append({
                            "idsku": id_sku,
                            "id": product_id,
                            "nombre": product_name,
                            "unidad_de_medida": measurement_unit
                        })
                        print(f"✅ Producto encontrado: {id_sku}, {product_id}, {product_name}, {measurement_unit}")

            start += step
            time.sleep(1)  # Evita sobrecargar la API con muchas solicitudes seguidas

        except requests.exceptions.RequestException as e:
            print(f"❌ Error al obtener los productos: {e}")
            break
        except json.JSONDecodeError:
            print("❌ Error al procesar la respuesta JSON de la API.")
            break
        except Exception as e:
            print(f"❌ Ocurrió un error: {e}")
            break

    # Guardar en un archivo JSON
    file_path = os.path.join(os.getcwd(), "productos_metro_filtrados.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(all_products, json_file, indent=4, ensure_ascii=False)

    print(f"\n✅ Archivo guardado correctamente en: {file_path}")
    print(f"📦 Total de productos encontrados: {len(all_products)}")

# Llamada a la función
get_products_by_measurement_unit()


#mejorar lo acdecuado seria que muestre los atributos idsku, productid, nombre del producto, nombre del sku, unidad de medida