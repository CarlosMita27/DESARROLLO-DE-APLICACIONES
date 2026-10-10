# =============================================================================
# ARCHIVO:      middleware_seguridad.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Middlewares WSGI del micro-servicio de inscripciones. El
#               middleware de seguridad valida el token Bearer y cortocircuita
#               la cadena con 401; el de errores captura cualquier fallo no
#               previsto y responde 500 en JSON.
# =============================================================================
import sys
import hmac
from utilidades_http import respuesta_json

TOKEN_ESPERADO = "Bearer TOKEN_SECRETO_2026"


class MiddlewareTokenSeguridad:
    # Eslabón de seguridad: intercepta todas las peticiones antes de la aplicación
    def __init__(self, aplicacion_interior, token_esperado=TOKEN_ESPERADO):
        self.aplicacion_interior = aplicacion_interior
        self.token_esperado = token_esperado

    def __call__(self, environ, start_response):
        # 1. La cabecera Authorization llega normalizada como HTTP_AUTHORIZATION
        token = environ.get("HTTP_AUTHORIZATION", "")

        # 2. compare_digest compara en tiempo constante (evita ataques de temporización)
        if not hmac.compare_digest(token.encode("utf-8"), self.token_esperado.encode("utf-8")):
            # Cortocircuito: la cadena se detiene y se responde 401 de inmediato
            return respuesta_json(start_response, "401 Unauthorized",
                                  {"error": "Token ausente o inválido. Acceso no autorizado."},
                                  [("WWW-Authenticate", 'Bearer realm="inscripciones"')])

        # 3. Delegación: el token es válido y la petición continúa hacia la aplicación
        return self.aplicacion_interior(environ, start_response)


class MiddlewareErrores:
    # Manejo global de errores: última barrera ante cualquier excepción no prevista
    def __init__(self, aplicacion_interior):
        self.aplicacion_interior = aplicacion_interior

    def __call__(self, environ, start_response):
        try:
            return self.aplicacion_interior(environ, start_response)
        except Exception as error:
            print(f"[Manejo global] -> {type(error).__name__}: {error}", flush=True)
            # exc_info informa al servidor de la excepción, como indica el PEP 3333
            return respuesta_json(start_response, "500 Internal Server Error",
                                  {"error": "Error interno del servidor."},
                                  exc_info=sys.exc_info())
