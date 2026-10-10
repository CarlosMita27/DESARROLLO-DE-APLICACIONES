# =============================================================================
# ARCHIVO:      paginacion_guia.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Versión original de la guía, usada solo para comparar. Convierte
#               los parámetros a entero, pero no valida que sean mayores que
#               cero: los valores negativos producen resultados indebidos.
# =============================================================================
import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

base_de_datos = [{"id": i, "articulo": f"Item {i}", "valor": i * 10} for i in range(1, 101)]


def endpoint_inventario_paginado(environ, start_response):
    # Extracción y conversión de los parámetros de la cadena de consulta
    parametros_url = parse_qs(environ.get("QUERY_STRING", ""))
    try:
        limite_elementos = int(parametros_url.get("limite", ["10"])[0])
        pagina_actual = int(parametros_url.get("pagina", ["1"])[0])
    except ValueError:
        estado, cuerpo = "400 Bad Request", {"error": "Paginación exige numéricos"}
    else:
        # Solo se controla el tope superior; no hay validación de valores negativos
        if limite_elementos > 50:
            limite_elementos = 50
        indice_desplazamiento = (pagina_actual - 1) * limite_elementos
        indice_corte = indice_desplazamiento + limite_elementos
        estado = "200 OK"
        cuerpo = {
            "meta": {"pagina": pagina_actual, "limite_real": limite_elementos,
                     "total_items": len(base_de_datos)},
            "registros": base_de_datos[indice_desplazamiento:indice_corte],
        }

    payload = json.dumps(cuerpo).encode("utf-8")
    start_response(estado, [("Content-Type", "application/json"),
                            ("Content-Length", str(len(payload)))])
    return [payload]


if __name__ == "__main__":
    servidor = make_server("127.0.0.1", 8080, endpoint_inventario_paginado)
    print("Versión de la guía en http://127.0.0.1:8080  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
