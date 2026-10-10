# =============================================================================
# ARCHIVO:      paginacion.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Endpoint WSGI de paginación por Query String. Extrae limite y
#               pagina con parse_qs, valida el tipo y el rango de cada valor,
#               aplica un tope máximo y pagina con el algoritmo Offset/Limit.
# =============================================================================
import json
import math
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

# Colección simulada de 100 artículos en memoria
base_de_datos = [{"id": i, "articulo": f"Item {i}", "valor": i * 10} for i in range(1, 101)]
LIMITE_MAXIMO = 50  # hard limit: máximo de registros por página


def endpoint_inventario_paginado(environ, start_response):
    # 1. Extracción: parse_qs devuelve listas, por eso se toma el elemento [0]
    parametros = parse_qs(environ.get("QUERY_STRING", ""))

    # 2. Conversión de tipos y validación de rango (Fail-Fast)
    try:
        limite = int(parametros.get("limite", ["10"])[0])
        pagina = int(parametros.get("pagina", ["1"])[0])
        if limite < 1 or pagina < 1:
            raise ValueError("valores menores que 1")
    except ValueError:
        estado = "400 Bad Request"
        cuerpo = {"error": "Paginación exige numéricos enteros positivos"}
    else:
        # 3. Tope máximo y algoritmo Offset/Limit mediante slicing
        limite = min(limite, LIMITE_MAXIMO)
        desplazamiento = (pagina - 1) * limite
        estado = "200 OK"
        cuerpo = {
            "meta": {
                "pagina": pagina,
                "limite_real": limite,
                "total_items": len(base_de_datos),
                "total_paginas": math.ceil(len(base_de_datos) / limite),
            },
            "registros": base_de_datos[desplazamiento:desplazamiento + limite],
        }

    # 4. Respuesta JSON con Content-Length exacto
    payload = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
    start_response(estado, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(payload))),
    ])
    return [payload]


if __name__ == "__main__":
    servidor = make_server("127.0.0.1", 8080, endpoint_inventario_paginado)
    print("Paginación en http://127.0.0.1:8080/?limite=15&pagina=2  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
