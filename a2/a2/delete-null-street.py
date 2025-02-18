import http.client
import json
import ssl

# Credenciales de VTEX
VTEX_ACCOUNT = "multicenter"
VTEX_ENVIRONMENT = "vtexcommercestable"
APP_KEY = "vtexappkey-multicenter-DZFRCZ"
APP_TOKEN = "BALGNUFXPZGOZKIWPHVFMZPDAQPGZEGQLEBXMHVFAAXMIGKLZEHKNBHAXBMONMDYMMWFKHPMRXCZBQFNNTKGVBTXFOSWNVXQRBLABNQPSDVSUADDWJDKZQSQGYBFKZZE"

# Ruta del archivo JSON con direcciones a eliminar
archivo_json = r"C:\simon\pasantia\a2\a2\filtro-street-null.json"

# Leer el archivo JSON
try:
    with open(archivo_json, "r", encoding="utf-8") as file:
        direcciones = json.load(file)

    # Tomar las primeras 13 direcciones
    direcciones_a_eliminar = direcciones[:10]

    if not direcciones_a_eliminar:
        print("No hay direcciones para eliminar.")
        exit()

    # Crear contexto SSL para omitir verificación del certificado
    context = ssl._create_unverified_context()

    # Conexión con VTEX
    conn = http.client.HTTPSConnection(f"{VTEX_ACCOUNT}.{VTEX_ENVIRONMENT}.com.br", context=context)

    # Encabezados
    headers = {
        'Accept': "application/vnd.vtex.ds.v10+json",
        'Content-Type': "application/json",
        'X-VTEX-API-AppKey': APP_KEY,
        'X-VTEX-API-AppToken': APP_TOKEN
    }

    # Eliminar direcciones en VTEX
    for direccion in direcciones_a_eliminar:
        direccion_id = direccion.get("id")  # Se usa el ID del documento

        if not direccion_id:
            print("❌ ID no encontrado en una dirección, omitiendo...")
            continue

        url = f"/api/dataentities/AD/documents/{direccion_id}"

        try:
            conn.request("DELETE", url, headers=headers)
            res = conn.getresponse()
            response_data = res.read().decode("utf-8")

            if res.status == 200 or res.status == 204:
                print(f"✅ Dirección {direccion_id} eliminada correctamente.")
            else:
                print(f"⚠️ Error al eliminar {direccion_id}: {response_data}")

        except Exception as e:
            print(f"❌ Error al eliminar {direccion_id}: {e}")

    conn.close()

except Exception as e:
    print(f"❌ Error al procesar el archivo o eliminar direcciones: {e}")
