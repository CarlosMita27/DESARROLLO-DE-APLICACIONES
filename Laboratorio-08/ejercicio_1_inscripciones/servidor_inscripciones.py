# =============================================================================
# ARCHIVO:      servidor_inscripciones.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Punto de arranque del micro-servicio. Compone la arquitectura en
#               capas (manejo de errores -> seguridad por token -> aplicación) y
#               la ejecuta sobre el servidor de referencia wsgiref.
# =============================================================================
from wsgiref.simple_server import make_server, WSGIRequestHandler
from aplicacion_inscripciones import aplicacion_inscripciones
from middleware_seguridad import MiddlewareTokenSeguridad, MiddlewareErrores


class ManejadorConTiempoLimite(WSGIRequestHandler):
    # Tiempo límite del socket: un cliente que no envía datos no bloquea el servidor
    timeout = 10


# Cadena de Responsabilidad: cada capa envuelve a la siguiente
aplicacion = MiddlewareErrores(MiddlewareTokenSeguridad(aplicacion_inscripciones))


if __name__ == "__main__":
    servidor = make_server("127.0.0.1", 8080, aplicacion,
                           handler_class=ManejadorConTiempoLimite)
    print("Servicio de inscripciones en http://127.0.0.1:8080/api/inscripciones")
    print("Cabecera requerida: Authorization: Bearer TOKEN_SECRETO_2026")
    print("Presione Ctrl + C para detener.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
