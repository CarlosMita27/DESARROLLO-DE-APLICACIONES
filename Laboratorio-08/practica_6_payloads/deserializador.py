# =============================================================================
# ARCHIVO:      deserializador.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Endpoint WSGI de ingesta polimórfica. Acepta cargas JSON o
#               URL-encoded, lee el cuerpo de forma acotada con CONTENT_LENGTH
#               y valida el esquema (Fail-Fast) antes de la lógica de negocio.
# =============================================================================
import sys
import json
import socket
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server, WSGIRequestHandler

LLAVES_OBLIGATORIAS = {"identificador", "token_operacion", "comando"}
TAMANO_MAXIMO = 1_048_576  # tope del cuerpo de una petición (1 MB)


def responder(start_response, estado, datos, cabeceras_extra=(), exc_info=None):
    # Respuesta JSON uniforme con Content-Type y Content-Length exactos
    cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
    start_response(estado, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(cuerpo))),
        *cabeceras_extra,
    ], exc_info)
    return [cuerpo]


def endpoint_recepcion_estricta(environ, start_response):
    # 1. Control perimetral de verbos: solo POST y PUT transportan cargas útiles
    if environ.get("REQUEST_METHOD") not in ("POST", "PUT"):
        return responder(start_response, "405 Method Not Allowed",
                         {"error": "Método transaccional bloqueado"}, [("Allow", "POST, PUT")])

    # 2. Control de I/O: CONTENT_LENGTH debe ser un entero entre 1 y el tope
    try:
        tamano = int(environ.get("CONTENT_LENGTH") or "0")
        if tamano < 0:
            raise ValueError("longitud negativa")
    except ValueError:
        return responder(start_response, "400 Bad Request",
                         {"error": "Content-Length inválido"})
    if tamano == 0:
        return responder(start_response, "400 Bad Request",
                         {"error": "Rechazo: Payload vacío (Zero Bytes)"})
    if tamano > TAMANO_MAXIMO:
        return responder(start_response, "413 Content Too Large",
                         {"error": "El payload supera el tamaño máximo de 1 MB"})

    # 3. Lectura acotada del flujo binario: nunca más bytes de los declarados
    try:
        cuerpo_bytes = environ["wsgi.input"].read(tamano)
    except socket.timeout:
        return responder(start_response, "408 Request Timeout",
                         {"error": "Tiempo de espera agotado al leer el payload"})
    if len(cuerpo_bytes) < tamano:
        return responder(start_response, "400 Bad Request", {"error": "Payload incompleto"})

    # 4. Ingesta polimórfica: la estrategia de deserialización depende de CONTENT_TYPE
    formato = environ.get("CONTENT_TYPE", "")
    try:
        if "application/json" in formato:
            dto = json.loads(cuerpo_bytes.decode("utf-8"))
        elif "application/x-www-form-urlencoded" in formato:
            listas = parse_qs(cuerpo_bytes.decode("utf-8"))
            dto = {clave: valores[0] for clave, valores in listas.items()}
        else:
            return responder(start_response, "415 Unsupported Media Type",
                             {"error": "El servidor exige formatos JSON o URL-Encoded"})
    except ValueError:
        # JSONDecodeError y UnicodeDecodeError heredan de ValueError
        return responder(start_response, "400 Bad Request",
                         {"error": "Corrupción detectada en el formato de transferencia"})

    # 5. Validación del contrato (Fail-Fast): objeto con todas las llaves obligatorias
    if not isinstance(dto, dict):
        return responder(start_response, "400 Bad Request",
                         {"error": "El payload debe ser un objeto de pares clave-valor"})
    faltantes = sorted(LLAVES_OBLIGATORIAS - dto.keys())
    if faltantes:
        return responder(start_response, "400 Bad Request",
                         {"error": f"Violación del esquema. Faltan propiedades: {faltantes}"})

    # 6. Payload estandarizado y listo para la lógica de negocio
    return responder(start_response, "200 OK",
                     {"estado": "Payload estandarizado y auditado exitosamente", "datos": dto})


def con_manejo_de_errores(aplicacion):
    # Envoltura WSGI de manejo global: un fallo no previsto se responde con 500 en JSON
    def aplicacion_protegida(environ, start_response):
        try:
            return aplicacion(environ, start_response)
        except Exception as error:
            print(f"[Manejo global] -> {type(error).__name__}: {error}", flush=True)
            # exc_info informa al servidor de la excepción, como indica el PEP 3333
            return responder(start_response, "500 Internal Server Error",
                             {"error": "Error interno del servidor"}, exc_info=sys.exc_info())
    return aplicacion_protegida


class ManejadorConTiempoLimite(WSGIRequestHandler):
    # Tiempo límite del socket: un cliente que no envía datos no bloquea el hilo
    timeout = 10


aplicacion = con_manejo_de_errores(endpoint_recepcion_estricta)


if __name__ == "__main__":
    servidor = make_server("127.0.0.1", 8080, aplicacion,
                           handler_class=ManejadorConTiempoLimite)
    print("Receptor de payloads en http://127.0.0.1:8080  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
