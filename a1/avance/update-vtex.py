import requests
import json

# Datos de autenticación
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Producto ID
PRODUCT_ID = "44995"

# Headers de autenticación
headers = {
    "X-VTEX-API-AppKey": APP_KEY,
    "X-VTEX-API-AppToken": APP_TOKEN,
    "Content-Type": "application/json"
}

# Paso 1: Obtener los SKUs asociados al PRODUCT_ID
def get_skus(product_id):
    url = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/catalog_system/pvt/sku/stockkeepingunitbyproductid/{product_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Imprimir la respuesta completa para inspeccionarla
        print("Respuesta de la API:", json.dumps(response.json(), indent=4))
        return response.json()  # Retorna la lista de SKUs
    else:
        print(f"Error al obtener SKUs: {response.status_code}")
        return None

# Paso 2: Actualizar un atributo del SKU
def update_sku_attribute(sku_id, product_id, sku_name):
    url = f"https://{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br/api/catalog/pvt/stockkeepingunit/{sku_id}"
    
    # Ejemplo de atributo que se quiere actualizar (en este caso la unidad de medida)
    data = {
        "MeasurementUnit": "un",  # Cambia esto según el atributo que quieras actualizar
        "ProductId": product_id,  # Asegurarse de incluir el ProductId
        "Name": sku_name  # Asegurarse de incluir el Name
    }
    
    print(f"Enviando actualización para SKU {sku_id}: {json.dumps(data, indent=4)}")  # Imprimir el cuerpo de la solicitud
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"SKU {sku_id} actualizado correctamente.")
    else:
        print(f"Error al actualizar SKU {sku_id}: {response.status_code}")
        print(f"Detalle del error: {response.text}")  # Mostrar detalles del error

# Main: Obtener los SKUs y luego actualizar el atributo de cada SKU
def main():
    skus = get_skus(PRODUCT_ID)
    
    if skus:
        # Si obtuvimos SKUs, los actualizamos uno por uno
        for sku in skus:
            # Imprimir cada SKU para ver su estructura
            print("SKU obtenido:", json.dumps(sku, indent=4))
            sku_id = sku.get('Id')  # Cambiar 'SkuId' por 'Id'
            product_id = sku.get('ProductId')  # Obtener el ProductId
            sku_name = sku.get('Name')  # Obtener el nombre del SKU
            if sku_id and product_id and sku_name:
                update_sku_attribute(sku_id, product_id, sku_name)
            else:
                print("No se encontró 'Id', 'ProductId' o 'Name' para este SKU.")

if __name__ == "__main__":
    main()
