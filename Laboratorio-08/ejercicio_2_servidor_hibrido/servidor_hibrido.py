# =============================================================================
# ARCHIVO:      servidor_hibrido.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Servidor híbrido con http.server. Sirve la interfaz estática de
#               la carpeta public/ con protección contra Path Traversal y expone
#               /api/inventario, un motor de búsqueda con filtro y paginación.
# =============================================================================
import os
import json
import math
import functools
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote, parse_qs

DIRECTORIO_PUBLICO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
TOPE_LIMITE = 100  # hard limit: máximo de registros por página

# Tipos MIME explícitos: en Windows el registro del sistema puede alterar la inferencia
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/javascript", ".js")

# Colección en memoria: 120 equipos (8 categorías x 15 marcas)
CATEGORIAS = ["Laptop", "Monitor", "Teclado", "Mouse",
              "Impresora", "Router", "Switch", "Disco SSD"]
MARCAS = ["HP", "Lenovo", "Dell", "Asus", "Acer", "LG", "Samsung", "Logitech",
          "TP-Link", "Kingston", "Epson", "Cisco", "Xiaomi", "Huawei", "MSI"]
combinaciones = [(categoria, marca) for categoria in CATEGORIAS for marca in MARCAS]
inventario = [
    {"id": numero, "nombre": f"{categoria} {marca}", "categoria": categoria,
     "precio": round(49.9 + (numero * 37) % 900, 2)}
    for numero, (categoria, marca) in enumerate(combinaciones, start=1)
]


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


class ServidorHibrido(BaseHTTPRequestHandler):
    # Tiempo límite del socket: un cliente lento no bloquea el servidor
    timeout = 10

    @con_manejo_de_errores
    def do_GET(self):
        # Enrutamiento: la API no usa el sistema de archivos; el resto es contenido estático
        url = urlparse(self.path)
        if url.path == "/api/inventario":
            self.atender_inventario(url.query)
        else:
            self.servir_estatico(unquote(url.path))

    def servir_estatico(self, ruta_url):
        # 1. Solo "/" y las rutas bajo "/public/" corresponden a recursos estáticos
        if ruta_url == "/":
            relativa = "index.html"
        elif ruta_url.startswith("/public/"):
            relativa = ruta_url[len("/public/"):]
        else:
            self.emitir_json(404, {"error": "Recurso no encontrado."})
            return

        # 2. Sanitización con join y abspath, y validación de frontera con commonpath
        try:
            ruta_resuelta = os.path.abspath(os.path.join(DIRECTORIO_PUBLICO, relativa))
            ruta_comun = os.path.commonpath([DIRECTORIO_PUBLICO, ruta_resuelta])
            dentro = ruta_comun == DIRECTORIO_PUBLICO
        except ValueError:
            dentro = False
        if not dentro:
            mensaje = "Acceso denegado: ruta fuera de la carpeta pública."
            self.emitir_json(403, {"error": mensaje})
            return
        if not os.path.isfile(ruta_resuelta):
            self.emitir_json(404, {"error": "Recurso no encontrado."})
            return

        # 3. Inferencia del tipo MIME y transmisión binaria por self.wfile
        tipo_mime, _ = mimetypes.guess_type(ruta_resuelta)
        tipo_mime = tipo_mime or "application/octet-stream"
        if tipo_mime.startswith("text/"):
            tipo_mime += "; charset=utf-8"
        with open(ruta_resuelta, "rb") as archivo:
            contenido = archivo.read()
        self.send_response(200)
        self.send_header("Content-Type", tipo_mime)
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def atender_inventario(self, consulta):
        # 1. Extracción de parámetros: parse_qs devuelve una lista por cada llave
        parametros = parse_qs(consulta)
        filtro = parametros.get("filtro", [""])[0].strip().lower()

        # 2. Casting seguro y validación de rangos (Fail-Fast)
        try:
            limite = int(parametros.get("limite", ["10"])[0])
            pagina = int(parametros.get("pagina", ["1"])[0])
        except ValueError:
            self.emitir_json(400, {"error": "limite y pagina deben ser números enteros."})
            return
        if limite < 1 or pagina < 1:
            self.emitir_json(400, {"error": "limite y pagina deben ser mayores que cero."})
            return
        limite_aplicado = min(limite, TOPE_LIMITE)

        # 3. Búsqueda por coincidencia parcial y paginación Offset/Limit
        coincidencias = [equipo for equipo in inventario if filtro in equipo["nombre"].lower()]
        desplazamiento = (pagina - 1) * limite_aplicado
        self.emitir_json(200, {
            "meta": {
                "filtro": filtro,
                "pagina": pagina,
                "limite_solicitado": limite,
                "limite_aplicado": limite_aplicado,
                "total_coincidencias": len(coincidencias),
                "total_paginas": math.ceil(len(coincidencias) / limite_aplicado),
            },
            "resultados": coincidencias[desplazamiento:desplazamiento + limite_aplicado],
        })

    def emitir_json(self, codigo_http, datos, cabeceras_extra=()):
        # Serialización centralizada de las respuestas JSON
        payload = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo_http)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for nombre, valor in cabeceras_extra:
            self.send_header(nombre, valor)
        self.end_headers()
        self.wfile.write(payload)

    def metodo_no_permitido(self):
        # El servidor es de solo lectura: 405 con la cabecera Allow
        self.emitir_json(405, {"error": "Método no permitido."}, [("Allow", "GET")])

    do_POST = do_PUT = do_PATCH = do_DELETE = metodo_no_permitido


if __name__ == "__main__":
    servidor = HTTPServer(("127.0.0.1", 8000), ServidorHibrido)
    print("Servidor híbrido en http://127.0.0.1:8000  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
