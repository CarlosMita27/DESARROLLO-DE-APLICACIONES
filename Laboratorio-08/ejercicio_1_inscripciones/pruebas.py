# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas del Ejercicio 1: seguridad por token,
#               ingesta JSON y URL-encoded, validación del esquema, control de
#               verbos y rutas, control de Content-Length y manejo de errores.
# =============================================================================
import io
import json
import socket
import threading
import http.client
from contextlib import redirect_stdout
from wsgiref.simple_server import make_server
from servidor_inscripciones import aplicacion, ManejadorConTiempoLimite
from middleware_seguridad import MiddlewareErrores

TOKEN = "Bearer TOKEN_SECRETO_2026"
JSON, FORM = "application/json", "application/x-www-form-urlencoded"
RUTA = "/api/inscripciones"


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


def enviar(metodo, ruta, cuerpo=None, tipo=None, token=None, destino=None):
    # Devuelve código de estado, cabeceras y JSON de la respuesta
    cabeceras = {}
    if tipo:
        cabeceras["Content-Type"] = tipo
    if token:
        cabeceras["Authorization"] = token
    conexion = http.client.HTTPConnection("127.0.0.1", destino or puerto)
    conexion.request(metodo, ruta, body=cuerpo, headers=cabeceras)
    respuesta = conexion.getresponse()
    return respuesta.status, dict(respuesta.getheaders()), json.loads(respuesta.read())


def enviar_crudo(content_length, cuerpo):
    # Petición escrita a mano para declarar un Content-Length anómalo
    peticion = (f"POST {RUTA} HTTP/1.1\r\nHost: localhost\r\nAuthorization: {TOKEN}\r\n"
                f"Content-Type: {JSON}\r\nContent-Length: {content_length}\r\n\r\n{cuerpo}")
    with socket.create_connection(("127.0.0.1", puerto), timeout=5) as conexion:
        conexion.sendall(peticion.encode())
        datos = b""
        while bloque := conexion.recv(4096):
            datos += bloque
    return datos.split(b"\r\n")[0].decode("latin-1")


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:32s} -> {resultado}")


aspirante = {"dni": "70123456", "correo_electronico": "aspirante@correo.com",
             "programa_academico": "Ingeniería de Sistemas"}
formulario = ("dni=70654321&correo_electronico=postulante%40correo.com"
              "&programa_academico=Ingenier%C3%ADa+de+Sistemas")
dni_invalido = json.dumps({**aspirante, "dni": "12AB"})
correo_invalido = json.dumps({**aspirante, "correo_electronico": "sin-arroba"})

# 1. Seguridad, ingesta, validación, verbos y rutas
casos = [
    ("Sin cabecera Authorization", "POST", RUTA, json.dumps(aspirante), JSON, None, 401),
    ("Token inválido", "POST", RUTA, json.dumps(aspirante), JSON, "Bearer TOKEN_FALSO", 401),
    ("JSON válido con token", "POST", RUTA, json.dumps(aspirante), JSON, TOKEN, 201),
    ("URL-encoded válido con token", "POST", RUTA, formulario, FORM, TOKEN, 201),
    ("Campos obligatorios faltantes", "POST", RUTA, '{"dni": "70123456"}', JSON, TOKEN, 400),
    ("DNI con formato inválido", "POST", RUTA, dni_invalido, JSON, TOKEN, 400),
    ("Correo con formato inválido", "POST", RUTA, correo_invalido, JSON, TOKEN, 400),
    ("JSON corrupto", "POST", RUTA, "{dni: 7012", JSON, TOKEN, 400),
    ("JSON que no es objeto", "POST", RUTA, "[1, 2, 3]", JSON, TOKEN, 400),
    ("Formato no soportado", "POST", RUTA, "dni 70123456", "text/plain", TOKEN, 415),
    ("Cuerpo vacío", "POST", RUTA, "", JSON, TOKEN, 400),
    ("GET con token", "GET", RUTA, None, None, TOKEN, 405),
    ("Ruta inexistente con token", "POST", "/api/otra", "{}", JSON, TOKEN, 404),
    ("Ruta inexistente sin token", "POST", "/api/otra", "{}", JSON, None, 401),
]
respuestas = {}
for descripcion, metodo, destino, cuerpo, tipo, token, esperado in casos:
    estado, cabeceras, datos = enviar(metodo, destino, cuerpo, tipo, token)
    assert estado == esperado, (descripcion, estado, datos)
    respuestas[descripcion] = (cabeceras, datos)
    mostrar(descripcion, f"{estado} | {datos.get('error') or datos.get('estado')}")

# 2. Cabeceras exigidas por el RFC 9110 y detalle del campo faltante
autenticacion = respuestas["Sin cabecera Authorization"][0]["WWW-Authenticate"]
assert autenticacion.startswith("Bearer")
mostrar("Cabecera WWW-Authenticate (401)", autenticacion)
assert respuestas["GET con token"][0]["Allow"] == "POST"
mostrar("Cabecera Allow (405)", respuestas["GET con token"][0]["Allow"])
faltantes = respuestas["Campos obligatorios faltantes"][1]["campos_faltantes"]
assert faltantes == ["correo_electronico", "programa_academico"]
mostrar("Detalle de campos faltantes", faltantes)

# 3. Control de I/O sobre CONTENT_LENGTH
for valor, cuerpo, codigo in [("-1", "{}", "400"), ("5000000", "{}", "413"),
                              ("100", '{"dni": "1"}', "408")]:
    linea_estado = enviar_crudo(valor, cuerpo)
    assert codigo in linea_estado, (valor, linea_estado)
    mostrar(f"Content-Length: {valor}", linea_estado)

# 4. Manejo global de errores con una aplicación que falla a propósito
consola = io.StringIO()
servidor_fallido = iniciar(MiddlewareErrores(lambda environ, start_response: 1 / 0))
puerto_fallido = servidor_fallido.server_address[1]
with redirect_stdout(consola):
    estado, _, datos = enviar("POST", RUTA, "{}", JSON, TOKEN, puerto_fallido)
assert estado == 500 and "ZeroDivisionError" in consola.getvalue()
mostrar("Excepción no prevista", f"{estado} | {datos['error']}")

servidor_fallido.shutdown()
servidor.shutdown()
print("Todas las pruebas del Ejercicio 1 fueron superadas.")
