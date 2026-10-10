# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas de la Práctica 3: variables CGI, cabeceras
#               normalizadas con el prefijo HTTP_, claves wsgi.* y omisión de
#               las variables del sistema operativo.
# =============================================================================
import json
import threading
import http.client
from wsgiref.simple_server import make_server, WSGIRequestHandler
from inspector_wsgi import inspector_entorno_wsgi


class Silencioso(WSGIRequestHandler):
    # Se desactiva el registro de peticiones para mostrar solo los resultados
    def log_message(self, *args):
        pass


# Servidor de prueba en un hilo aparte y en un puerto libre
servidor = make_server("127.0.0.1", 0, inspector_entorno_wsgi, handler_class=Silencioso)
puerto = servidor.server_address[1]
threading.Thread(target=servidor.serve_forever, daemon=True).start()

# Petición con cadena de consulta y cabeceras personalizadas
cabeceras = {"Authorization": "Bearer demo", "X-Personalizada": "valor",
             "User-Agent": "Pruebas"}
conexion = http.client.HTTPConnection("127.0.0.1", puerto)
conexion.request("GET", "/diagnostico?curso=python&seccion=web", headers=cabeceras)
respuesta = conexion.getresponse()
datos = json.loads(respuesta.read())
cgi, http_, wsgi = datos["variables_cgi"], datos["cabeceras_http"], datos["claves_wsgi"]


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:38s} -> {resultado}")


assert respuesta.status == 200
mostrar("Código de estado", respuesta.status)
assert cgi["REQUEST_METHOD"] == "GET" and cgi["PATH_INFO"] == "/diagnostico"
assert cgi["QUERY_STRING"] == "curso=python&seccion=web"
mostrar("Variables CGI", f"{cgi['REQUEST_METHOD']} {cgi['PATH_INFO']} {cgi['QUERY_STRING']}")
assert http_["HTTP_AUTHORIZATION"] == "Bearer demo"
assert http_["HTTP_X_PERSONALIZADA"] == "valor"
assert http_["HTTP_USER_AGENT"] == "Pruebas" and "HTTP_HOST" in http_
mostrar("Cabeceras normalizadas con HTTP_", ", ".join(sorted(http_)))
assert wsgi["wsgi.url_scheme"] == "http" and "BufferedReader" in wsgi["wsgi.input"]
mostrar("Claves wsgi.* (wsgi.input es un flujo)", wsgi["wsgi.input"])
assert datos["variables_del_sistema_omitidas"] > 0 and "PATH" not in cgi
mostrar("Variables del sistema omitidas", datos["variables_del_sistema_omitidas"])

servidor.shutdown()
print("Todas las pruebas de la Práctica 3 fueron superadas.")
