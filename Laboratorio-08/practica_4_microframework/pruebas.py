# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas de la Práctica 4: rutas registradas con el
#               decorador, respuesta en streaming, ruta inexistente, manejo
#               global de errores y mensajes del middleware de auditoría.
# =============================================================================
import io
import threading
import http.client
from contextlib import redirect_stdout
from wsgiref.simple_server import make_server, WSGIRequestHandler
from microframework import aplicacion_fortificada


class Silencioso(WSGIRequestHandler):
    # Se desactiva el registro de wsgiref para conservar solo los mensajes propios
    def log_message(self, *args):
        pass


# Servidor de prueba en un hilo aparte y en un puerto libre
servidor = make_server("127.0.0.1", 0, aplicacion_fortificada, handler_class=Silencioso)
puerto = servidor.server_address[1]
threading.Thread(target=servidor.serve_forever, daemon=True).start()


def pedir(ruta):
    # Devuelve código de estado, cabeceras y cuerpo decodificado
    conexion = http.client.HTTPConnection("127.0.0.1", puerto)
    conexion.request("GET", ruta)
    respuesta = conexion.getresponse()
    return respuesta.status, dict(respuesta.getheaders()), respuesta.read().decode("utf-8")


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:16s} -> {resultado}")


# Se captura la consola para verificar los mensajes de los middlewares
consola = io.StringIO()
with redirect_stdout(consola):
    saludo = pedir("/saludo")
    hora = pedir("/hora")
    exportar = pedir("/exportar")
    inexistente = pedir("/inexistente")
    fallo = pedir("/fallo")
registro = consola.getvalue()

assert saludo[0] == 200 and "Micro-Framework" in saludo[2]
mostrar("GET /saludo", f"{saludo[0]} | {saludo[2]}")
assert hora[0] == 200 and hora[2].startswith("Hora del servidor")
mostrar("GET /hora", f"{hora[0]} | {hora[2]}")
lineas = exportar[2].splitlines()
assert exportar[0] == 200 and len(lineas) == 1000 and "Content-Length" not in exportar[1]
mostrar("GET /exportar",
        f"{exportar[0]} | {len(lineas)} líneas en streaming, sin Content-Length")
assert inexistente[0] == 404
mostrar("GET /inexistente", f"{inexistente[0]} | {inexistente[2]}")
assert fallo[0] == 500 and "[Manejo global] -> ZeroDivisionError" in registro
mostrar("GET /fallo", f"{fallo[0]} | excepción capturada por MiddlewareErrores")
peticiones = registro.count("[Capa de Seguridad]")
assert peticiones == 5
mostrar("Auditoría", f"{peticiones} peticiones registradas por el middleware")

servidor.shutdown()
print("Todas las pruebas de la Práctica 4 fueron superadas.")
