# =============================================================================
# ARCHIVO:      servidor_estatico_guia.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Versión original de la guía, usada solo para comparar. Conserva
#               la validación con startswith(), que confunde la carpeta public
#               con una carpeta hermana de nombre parecido (public-privado).
#               Único cambio: el directorio base es public/ en lugar de os.getcwd().
# =============================================================================
import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

DIRECTORIO_PUBLICO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")


class ServidorEstaticoGuia(BaseHTTPRequestHandler):
    def do_GET(self):
        # Ruta solicitada sin la barra inicial, unida al directorio base y normalizada
        ruta_cruda = self.path.lstrip("/") or "index.html"
        ruta_resuelta = os.path.abspath(os.path.join(DIRECTORIO_PUBLICO, ruta_cruda))

        # Validación original: compara prefijos de texto, no carpetas completas
        fuera = not ruta_resuelta.startswith(DIRECTORIO_PUBLICO)
        if fuera or not os.path.isfile(ruta_resuelta):
            self.send_error(404, "Recurso no encontrado o acceso estrictamente denegado.")
            return

        # Lectura binaria y respuesta con el tipo MIME inferido
        tipo_mime, _ = mimetypes.guess_type(ruta_resuelta)
        with open(ruta_resuelta, "rb") as archivo_fisico:
            contenido = archivo_fisico.read()
        self.send_response(200)
        self.send_header("Content-Type", tipo_mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)


if __name__ == "__main__":
    servidor = HTTPServer(("127.0.0.1", 8000), ServidorEstaticoGuia)
    print("Versión de la guía en http://127.0.0.1:8000  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
