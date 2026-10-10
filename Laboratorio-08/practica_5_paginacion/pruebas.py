# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas de la Práctica 5: valores por defecto,
#               desplazamiento, tope máximo y rechazo de valores no numéricos,
#               negativos o iguales a cero.
# =============================================================================
import json
import threading
import http.client
from wsgiref.simple_server import make_server, WSGIRequestHandler
from paginacion import endpoint_inventario_paginado


class Silencioso(WSGIRequestHandler):
    # Se desactiva el registro de peticiones para mostrar solo los resultados
    def log_message(self, *args):
        pass


# Servidor de prueba en un hilo aparte y en un puerto libre
servidor = make_server("127.0.0.1", 0, endpoint_inventario_paginado, handler_class=Silencioso)
puerto = servidor.server_address[1]
threading.Thread(target=servidor.serve_forever, daemon=True).start()


def pedir(consulta):
    # Devuelve el código de estado y el JSON de la respuesta
    conexion = http.client.HTTPConnection("127.0.0.1", puerto)
    conexion.request("GET", "/api/inventario" + consulta)
    respuesta = conexion.getresponse()
    return respuesta.status, json.loads(respuesta.read())


def ids(datos):
    # Rango de identificadores devuelto, para mostrarlo en la consola
    registros = datos["registros"]
    return f"ids {registros[0]['id']}-{registros[-1]['id']}" if registros else "lista vacía"


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:28s} -> {resultado}")


estado, datos = pedir("")
assert estado == 200 and len(datos["registros"]) == 10 and datos["registros"][0]["id"] == 1
mostrar("Sin parámetros", f"{estado} | {ids(datos)}")

estado, datos = pedir("?limite=15&pagina=2")
assert estado == 200 and datos["registros"][0]["id"] == 16 and len(datos["registros"]) == 15
mostrar("limite=15&pagina=2",
        f"{estado} | {ids(datos)} | total_paginas = {datos['meta']['total_paginas']}")

estado, datos = pedir("?limite=500")
assert estado == 200 and datos["meta"]["limite_real"] == 50 and len(datos["registros"]) == 50
mostrar("limite=500", f"{estado} | limite_real = {datos['meta']['limite_real']}")

estado, datos = pedir("?pagina=11")
assert estado == 200 and datos["registros"] == []
mostrar("pagina=11 (fuera de rango)", f"{estado} | {ids(datos)}")

for consulta in ["pagina=tres", "pagina=-1", "limite=-5", "limite=0", "pagina=0"]:
    estado, datos = pedir("?" + consulta)
    assert estado == 400, consulta
    mostrar(consulta, f"{estado} | {datos['error']}")

servidor.shutdown()
print("Todas las pruebas de la Práctica 5 fueron superadas.")
