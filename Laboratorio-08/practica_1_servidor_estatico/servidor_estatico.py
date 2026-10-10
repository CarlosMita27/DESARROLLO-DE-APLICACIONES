# =============================================================================
# ARCHIVO:      servidor_estatico.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Servidor de archivos estáticos construido con http.server.
#               Sirve la carpeta public/, infiere el tipo MIME de cada archivo
#               y bloquea los intentos de Path Traversal con un código 403.
# =============================================================================
import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote

# Directorio público: la única carpeta que el servidor puede leer
DIRECTORIO_PUBLICO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

# Tipos MIME explícitos: en Windows el registro del sistema puede alterar la inferencia
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/javascript", ".js")


class ServidorEstaticoFortificado(BaseHTTPRequestHandler):
    # Tiempo límite del socket: un cliente lento no bloquea el servidor
    timeout = 10

    def do_GET(self):
        # 1. Se descarta la query string y se decodifica la URL una sola vez
        ruta_url = unquote(urlparse(self.path).path)
        ruta_cruda = ruta_url.lstrip("/") or "index.html"

        # 2. Sanitización: join arma la ruta y abspath colapsa los segmentos ".."
        try:
            ruta_resuelta = os.path.abspath(os.path.join(DIRECTORIO_PUBLICO, ruta_cruda))
            # commonpath compara carpetas completas, no prefijos de texto
            ruta_comun = os.path.commonpath([DIRECTORIO_PUBLICO, ruta_resuelta])
            dentro = ruta_comun == DIRECTORIO_PUBLICO
        except ValueError:
            # Rutas con caracteres nulos o ubicadas en otra unidad de disco
            dentro = False

        # 3. Validación de frontera (Fail-Fast): fuera de public -> 403, inexistente -> 404
        if not dentro:
            self.send_error(403, explain="Acceso denegado: ruta fuera de la carpeta pública.")
            return
        if not os.path.isfile(ruta_resuelta):
            self.send_error(404, explain="El recurso solicitado no existe.")
            return

        # 4. Inferencia del tipo MIME según la extensión del archivo
        tipo_mime, _ = mimetypes.guess_type(ruta_resuelta)
        tipo_mime = tipo_mime or "application/octet-stream"
        if tipo_mime.startswith("text/"):
            tipo_mime += "; charset=utf-8"

        # 5. Lectura binaria del archivo físico
        try:
            with open(ruta_resuelta, "rb") as archivo:
                contenido = archivo.read()
        except OSError:
            self.send_error(500, explain="No se pudo leer el archivo.")
            return

        # 6. Respuesta: línea de estado, cabeceras, línea vacía y cuerpo en bytes
        self.send_response(200)
        self.send_header("Content-Type", tipo_mime)
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)


if __name__ == "__main__":
    # Arranque: HTTPServer enlaza el socket TCP y atiende las peticiones en un bucle
    servidor = HTTPServer(("127.0.0.1", 8000), ServidorEstaticoFortificado)
    print("Servidor estático en http://127.0.0.1:8000  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
