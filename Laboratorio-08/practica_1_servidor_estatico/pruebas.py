# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas de la Práctica 1. Levanta el servidor en un
#               puerto libre, envía peticiones HTTP escritas a mano por un socket
#               y verifica los códigos de estado y los tipos MIME.
# =============================================================================
import socket
import threading
from http.server import HTTPServer
from servidor_estatico import ServidorEstaticoFortificado


class ServidorSilencioso(ServidorEstaticoFortificado):
    # Se desactiva el registro de peticiones para mostrar solo los resultados
    def log_message(self, *args):
        pass


# Servidor de prueba en un hilo aparte y en un puerto libre (puerto 0)
servidor = HTTPServer(("127.0.0.1", 0), ServidorSilencioso)
puerto = servidor.server_address[1]
threading.Thread(target=servidor.serve_forever, daemon=True).start()


def pedir(ruta):
    # Petición cruda: línea de petición, cabeceras y la línea vacía \r\n\r\n
    peticion = f"GET {ruta} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
    with socket.create_connection(("127.0.0.1", puerto)) as conexion:
        conexion.sendall(peticion.encode())
        datos = b""
        while bloque := conexion.recv(4096):
            datos += bloque
    return datos.split(b"\r\n")[0].decode("latin-1"), datos


# Casos: (ruta solicitada, código esperado, fragmento esperado en la respuesta)
casos = [
    ("/", "200", b"text/html"),
    ("/estilo.css", "200", b"text/css"),
    ("/app.js", "200", b"text/javascript"),
    ("/index.html?version=2", "200", b"text/html"),
    ("/no_existe.txt", "404", b""),
    ("/../servidor_estatico.py", "403", b""),
    ("/../../../../etc/passwd", "403", b""),
    ("/%2e%2e/servidor_estatico.py", "403", b""),
    ("/..%2fservidor_estatico.py", "403", b""),
    ("/../public-privado/clave.txt", "403", b""),
]
for ruta, codigo, marca in casos:
    linea_estado, datos = pedir(ruta)
    assert codigo in linea_estado and marca in datos, (ruta, linea_estado)
    print(f"OK  {ruta:32s} -> {linea_estado}")

servidor.shutdown()
print("Todas las pruebas de la Práctica 1 fueron superadas.")
