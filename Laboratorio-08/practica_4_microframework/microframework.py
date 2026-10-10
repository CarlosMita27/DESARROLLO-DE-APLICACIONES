# =============================================================================
# ARCHIVO:      microframework.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Micro-framework WSGI orientado a objetos. Registra rutas con
#               decoradores, admite respuestas en streaming con generadores
#               (yield) y se protege con una cadena de middlewares: auditoría
#               y manejo global de errores.
# =============================================================================
import sys
from datetime import datetime
from wsgiref.simple_server import make_server


class NucleoWSGI:
    def __init__(self):
        # Tabla hash ruta -> función controladora (búsqueda en tiempo O(1))
        self.mapa_enrutamiento = {}

    def registrar_endpoint(self, ruta_esperada):
        # Fábrica de decoradores: registra la vista al definirla y la devuelve sin cambios
        def envoltura(funcion_controlador):
            self.mapa_enrutamiento[ruta_esperada] = funcion_controlador
            return funcion_controlador
        return envoltura

    def __call__(self, environ, start_response):
        # 1. Despacho: se busca el controlador asociado a PATH_INFO
        controlador = self.mapa_enrutamiento.get(environ.get("PATH_INFO", "/"))
        if controlador is None:
            return self.responder_texto(start_response, "404 Not Found",
                                        "Error 404: Endpoint huérfano o no implementado.")

        # 2. Ejecución de la vista
        resultado = controlador(environ)

        # 3a. Respuesta completa: texto codificado con Content-Length exacto
        if isinstance(resultado, str):
            return self.responder_texto(start_response, "200 OK", resultado)

        # 3b. Respuesta en streaming: el generador entrega cada bloque bajo demanda
        start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
        return (fragmento.encode("utf-8") for fragmento in resultado)

    @staticmethod
    def responder_texto(start_response, estado, texto):
        # Contrato WSGI: estado y cabeceras con start_response, cuerpo como lista de bytes
        payload = texto.encode("utf-8")
        start_response(estado, [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(payload))),
        ])
        return [payload]


class MiddlewareAuditoria:
    # Eslabón de la Cadena de Responsabilidad: registra la petición y la delega
    def __init__(self, aplicacion_interior):
        self.aplicacion_interior = aplicacion_interior

    def __call__(self, environ, start_response):
        verbo = environ.get("REQUEST_METHOD")
        uri = environ.get("PATH_INFO")
        print(f"[Capa de Seguridad] -> Intento de acceso: {verbo} a la ruta {uri}", flush=True)
        return self.aplicacion_interior(environ, start_response)


class MiddlewareErrores:
    # Manejo global de errores: ninguna excepción de las capas internas llega al cliente
    def __init__(self, aplicacion_interior):
        self.aplicacion_interior = aplicacion_interior

    def __call__(self, environ, start_response):
        try:
            return self.aplicacion_interior(environ, start_response)
        except Exception as error:
            print(f"[Manejo global] -> {type(error).__name__}: {error}", flush=True)
            payload = "Error 500: fallo interno controlado por el middleware.".encode("utf-8")
            start_response("500 Internal Server Error", [
                ("Content-Type", "text/plain; charset=utf-8"),
                ("Content-Length", str(len(payload))),
            ], sys.exc_info())
            return [payload]


app = NucleoWSGI()


# Vistas registradas de forma declarativa con el decorador
@app.registrar_endpoint("/saludo")
def vista_saludo(environ):
    return "Micro-Framework funcionando mediante abstracción declarativa."


@app.registrar_endpoint("/hora")
def vista_hora(environ):
    return f"Hora del servidor: {datetime.now():%H:%M:%S}"


@app.registrar_endpoint("/exportar")
def vista_exportar(environ):
    # Generador: las 1000 líneas se producen una a una, nunca todas juntas en memoria
    for numero in range(1, 1001):
        yield f"Registro {numero:04d}: acceso auditado\n"


@app.registrar_endpoint("/fallo")
def vista_fallo(environ):
    # Ruta de prueba: provoca una excepción para comprobar el manejo global de errores
    return f"Resultado: {1 / 0}"


# Cadena de Responsabilidad: Auditoría -> Manejo de errores -> Framework
aplicacion_fortificada = MiddlewareAuditoria(MiddlewareErrores(app))


if __name__ == "__main__":
    servidor = make_server("127.0.0.1", 8080, aplicacion_fortificada)
    print("Micro-framework en http://127.0.0.1:8080/saludo  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
