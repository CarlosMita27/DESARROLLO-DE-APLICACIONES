# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas de la Práctica 6: ingesta JSON y URL-encoded,
#               errores de verbo, formato y esquema, control de Content-Length y
#               manejo global de errores.
# =============================================================================
import io
import json
import socket
import threading
import http.client
from contextlib import redirect_stdout
from wsgiref.simple_server import make_server
from deserializador import aplicacion, con_manejo_de_errores, ManejadorConTiempoLimite

JSON, FORM = "application/json", "application/x-www-form-urlencoded"


class ManejadorDePrueba(ManejadorConTiempoLimite):
    # Tiempo límite de 1 s para comprobar el código 408 sin esperar 10 s
    timeout = 1

    def log_message(self, *args):
        pass


def iniciar(app):
    # Servidor de prueba en un hilo aparte y en un puerto libre
    servidor = make_server("127.0.0.1", 0, app, handler_class=ManejadorDePrueba)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


servidor = iniciar(aplicacion)
puerto = servidor.server_address[1]


def enviar(metodo, cuerpo, tipo, destino=None):
    # Devuelve código de estado, cabeceras y JSON de la respuesta
    conexion = http.client.HTTPConnection("127.0.0.1", destino or puerto)
    conexion.request(metodo, "/", body=cuerpo, headers={"Content-Type": tipo} if tipo else {})
    respuesta = conexion.getresponse()
    return respuesta.status, dict(respuesta.getheaders()), json.loads(respuesta.read())


def enviar_crudo(content_length, cuerpo):
    # Petición escrita a mano para declarar un Content-Length anómalo
    peticion = (f"POST / HTTP/1.1\r\nHost: localhost\r\nContent-Type: {JSON}\r\n"
                f"Content-Length: {content_length}\r\n\r\n{cuerpo}")
    with socket.create_connection(("127.0.0.1", puerto), timeout=5) as conexion:
        conexion.sendall(peticion.encode())
        datos = b""
        while bloque := conexion.recv(4096):
            datos += bloque
    return datos.split(b"\r\n")[0].decode("latin-1")


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:34s} -> {resultado}")


# 1. Ingesta polimórfica y validación del esquema
valido = {"identificador": 7, "token_operacion": "abc123", "comando": "sincronizar"}
formulario = "identificador=7&token_operacion=abc123&comando=sincronizar"
casos = [
    ("POST JSON válido", "POST", json.dumps(valido), JSON, 200),
    ("POST URL-encoded válido", "POST", formulario, FORM, 200),
    ("PUT URL-encoded válido", "PUT", formulario, FORM, 200),
    ("GET (verbo no permitido)", "GET", None, None, 405),
    ("POST sin cuerpo", "POST", "", JSON, 400),
    ("POST JSON corrupto", "POST", "{roto", JSON, 400),
    ("POST texto plano", "POST", "texto", "text/plain", 415),
    ("POST con llaves faltantes", "POST", json.dumps({"identificador": 7}), JSON, 400),
    ("POST JSON que no es objeto", "POST", "[1, 2, 3]", JSON, 400),
]
for descripcion, metodo, cuerpo, tipo, esperado in casos:
    estado, cabeceras, datos = enviar(metodo, cuerpo, tipo)
    assert estado == esperado, (descripcion, estado, datos)
    mostrar(descripcion, f"{estado} | {datos.get('error') or datos.get('estado')}")

# 2. Cabecera Allow en la respuesta 405 y tipos de dato según el formato
_, cabeceras, _ = enviar("GET", None, None)
assert cabeceras["Allow"] == "POST, PUT"
mostrar("Cabecera Allow en el 405", f"Allow: {cabeceras['Allow']}")
_, _, desde_json = enviar("POST", json.dumps(valido), JSON)
_, _, desde_formulario = enviar("POST", formulario, FORM)
assert desde_json["datos"]["identificador"] == 7
assert desde_formulario["datos"]["identificador"] == "7"
mostrar("Tipo de identificador", "JSON: int | formulario: str")

# 3. Control de I/O sobre CONTENT_LENGTH
for valor, cuerpo, codigo in [("-1", "{}", "400"), ("5000000", "{}", "413"),
                              ("100", '{"a": 1}', "408")]:
    linea_estado = enviar_crudo(valor, cuerpo)
    assert codigo in linea_estado, (valor, linea_estado)
    mostrar(f"Content-Length: {valor}", linea_estado)

# 4. Manejo global de errores con una aplicación que falla a propósito
consola = io.StringIO()
servidor_fallido = iniciar(con_manejo_de_errores(lambda environ, start_response: 1 / 0))
with redirect_stdout(consola):
    estado, _, datos = enviar("POST", "{}", JSON, servidor_fallido.server_address[1])
assert estado == 500 and "ZeroDivisionError" in consola.getvalue()
mostrar("Excepción no prevista", f"{estado} | {datos['error']}")

servidor_fallido.shutdown()
servidor.shutdown()
print("Todas las pruebas de la Práctica 6 fueron superadas.")
