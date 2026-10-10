# =============================================================================
# ARCHIVO:      enrutador_api.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  API REST con http.server sobre una colección de usuarios en
#               memoria. GET consulta y POST crea registros (201 Created). La
#               lectura del cuerpo se limita a Content-Length, con tope y tiempo
#               límite, para evitar bloqueos del hilo (Thread Starvation).
# =============================================================================
import json
import socket
import functools
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# Base de datos volátil: la lista vive en memoria mientras el servidor esté activo
coleccion_usuarios = [
    {"id": 100, "nombre": "Linus Torvalds", "perfil": "SysAdmin"}
]
TAMANO_MAXIMO = 1_048_576  # tope del cuerpo de una petición (1 MB)


def con_manejo_de_errores(metodo):
    # Decorador de manejo global: un fallo no previsto se responde con 500 en JSON
    @functools.wraps(metodo)
    def envoltura(self):
        try:
            metodo(self)
        except Exception as error:
            self.log_error("Error interno: %r", error)
            self.emitir_json(500, {"error": "Error interno del servidor."})
    return envoltura


class EnrutadorAPI(BaseHTTPRequestHandler):
    # Tiempo límite del socket: un cliente que no envía datos no bloquea el hilo
    timeout = 10

    def emitir_json(self, codigo_http, datos, cabeceras_extra=()):
        # Serialización centralizada: diccionario -> JSON -> bytes UTF-8
        payload = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo_http)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for nombre, valor in cabeceras_extra:
            self.send_header(nombre, valor)
        self.end_headers()
        self.wfile.write(payload)

    @con_manejo_de_errores
    def do_GET(self):
        # Consulta de la colección; la query string no altera el enrutamiento
        if urlparse(self.path).path == "/api/usuarios":
            self.emitir_json(200, {"estado": "ok", "total": len(coleccion_usuarios),
                                   "datos": coleccion_usuarios})
        else:
            self.emitir_json(404, {"error": "Endpoint no mapeado en la API"})

    @con_manejo_de_errores
    def do_POST(self):
        # 1. Enrutamiento: solo /api/usuarios admite la creación de registros
        if urlparse(self.path).path != "/api/usuarios":
            self.emitir_json(404, {"error": "Endpoint no mapeado en la API"})
            return

        # 2. Control de I/O: Content-Length debe ser un entero entre 0 y el tope
        try:
            longitud = int(self.headers.get("Content-Length", 0))
        except ValueError:
            longitud = -1
        if longitud < 0:
            self.emitir_json(400, {"error": "Content-Length inválido."})
            return
        if longitud > TAMANO_MAXIMO:
            self.emitir_json(413, {"error": "El cuerpo supera el tamaño máximo de 1 MB."})
            return

        # 3. Lectura acotada: exactamente los bytes declarados, con tiempo límite
        try:
            bytes_recibidos = self.rfile.read(longitud)
        except socket.timeout:
            self.emitir_json(408, {"error": "Tiempo de espera agotado al leer el cuerpo."})
            return
        if len(bytes_recibidos) < longitud:
            self.emitir_json(400, {"error": "El cuerpo recibido está incompleto."})
            return

        # 4. Deserialización y validación del contrato (Fail-Fast)
        try:
            nuevo_registro = json.loads(bytes_recibidos.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.emitir_json(400, {"error": "El cuerpo de la petición debe ser JSON válido."})
            return
        if not isinstance(nuevo_registro, dict):
            self.emitir_json(400, {"error": "El cuerpo debe ser un objeto JSON."})
            return

        # 5. Creación del registro con identificador secuencial -> 201 Created
        nuevo_registro["id"] = coleccion_usuarios[-1]["id"] + 1 if coleccion_usuarios else 1
        coleccion_usuarios.append(nuevo_registro)
        self.emitir_json(201, {"estado": "creado", "datos": nuevo_registro})

    def metodo_no_permitido(self):
        # Verbos sin soporte: 405 con la cabecera Allow que exige el RFC 9110
        self.emitir_json(405, {"error": "Método no permitido en la API"},
                         [("Allow", "GET, POST")])

    do_PUT = do_PATCH = do_DELETE = metodo_no_permitido


if __name__ == "__main__":
    # Arranque del servidor HTTP nativo
    servidor = HTTPServer(("127.0.0.1", 8000), EnrutadorAPI)
    print("API REST en http://127.0.0.1:8000/api/usuarios  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
