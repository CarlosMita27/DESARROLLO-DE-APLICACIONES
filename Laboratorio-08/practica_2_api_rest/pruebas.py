# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas de la Práctica 2: verbos GET y POST, errores
#               de formato, verbos no permitidos y valores anómalos de
#               Content-Length (negativo, excesivo y mayor que el cuerpo real).
# =============================================================================
import json
import socket
import threading
import http.client
from http.server import HTTPServer
from enrutador_api import EnrutadorAPI


class EnrutadorDePrueba(EnrutadorAPI):
    # Tiempo límite de 1 s para comprobar el código 408 sin esperar 10 s
    timeout = 1

    def log_message(self, *args):
        pass


# Servidor de prueba en un hilo aparte y en un puerto libre
servidor = HTTPServer(("127.0.0.1", 0), EnrutadorDePrueba)
puerto = servidor.server_address[1]
threading.Thread(target=servidor.serve_forever, daemon=True).start()


def llamar(metodo, ruta, cuerpo=None):
    # Petición con http.client: devuelve código, cabeceras y JSON de respuesta
    conexion = http.client.HTTPConnection("127.0.0.1", puerto)
    cabeceras = {"Content-Type": "application/json"} if cuerpo is not None else {}
    conexion.request(metodo, ruta, body=cuerpo, headers=cabeceras)
    respuesta = conexion.getresponse()
    return respuesta.status, dict(respuesta.getheaders()), json.loads(respuesta.read())


def enviar_crudo(content_length, cuerpo):
    # Petición escrita a mano para declarar un Content-Length anómalo
    peticion = ("POST /api/usuarios HTTP/1.1\r\nHost: localhost\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {content_length}\r\n\r\n{cuerpo}")
    with socket.create_connection(("127.0.0.1", puerto), timeout=5) as conexion:
        conexion.sendall(peticion.encode())
        datos = b""
        while bloque := conexion.recv(4096):
            datos += bloque
    return datos.split(b"\r\n")[0].decode("latin-1")


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:37s} -> {resultado}")


# 1. Consulta, creación y consulta posterior de la colección
estado, _, datos = llamar("GET", "/api/usuarios")
assert estado == 200 and datos["total"] == 1
mostrar("GET /api/usuarios", f"{estado} | total = {datos['total']}")

estado, _, datos = llamar("GET", "/api/usuarios?orden=id")
assert estado == 200
mostrar("GET /api/usuarios?orden=id", estado)

nuevo = json.dumps({"nombre": "Ada Lovelace", "perfil": "Developer"})
estado, _, datos = llamar("POST", "/api/usuarios", nuevo)
assert estado == 201 and datos["datos"]["id"] == 101
mostrar("POST con JSON válido", f"{estado} | id = {datos['datos']['id']}")

estado, _, datos = llamar("GET", "/api/usuarios")
assert datos["total"] == 2
mostrar("GET después del POST", f"{estado} | total = {datos['total']}")

# 2. Errores de formato y de enrutamiento
estado, _, _ = llamar("POST", "/api/usuarios", "{no es json")
assert estado == 400
mostrar("POST con JSON mal formado", estado)

estado, _, _ = llamar("POST", "/api/usuarios", "[1, 2]")
assert estado == 400
mostrar("POST con JSON que no es objeto", estado)

estado, _, _ = llamar("GET", "/api/productos")
assert estado == 404
mostrar("GET a una ruta no mapeada", estado)

estado, cabeceras, _ = llamar("PUT", "/api/usuarios", "{}")
assert estado == 405 and cabeceras["Allow"] == "GET, POST"
mostrar("PUT /api/usuarios", f"{estado} | Allow: {cabeceras['Allow']}")

# 3. Control de I/O sobre Content-Length (el cuerpo real siempre mide 2 bytes)
for valor, codigo in [("-1", "400"), ("abc", "400"), ("5000000", "413"), ("100", "408")]:
    linea_estado = enviar_crudo(valor, "{}")
    assert codigo in linea_estado, (valor, linea_estado)
    mostrar(f"Content-Length: {valor} (2 bytes)", linea_estado)

servidor.shutdown()
print("Todas las pruebas de la Práctica 2 fueron superadas.")
