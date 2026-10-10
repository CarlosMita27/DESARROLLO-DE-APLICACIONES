# =============================================================================
# ARCHIVO:      pruebas.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Pruebas automáticas del Ejercicio 2: archivos estáticos con tipo
#               MIME, bloqueo de Path Traversal y motor de búsqueda con filtro,
#               paginación, tope máximo y validación de parámetros.
# =============================================================================
import json
import socket
import threading
from http.server import HTTPServer
from servidor_hibrido import ServidorHibrido


class ServidorSilencioso(ServidorHibrido):
    # Se desactiva el registro de peticiones para mostrar solo los resultados
    def log_message(self, *args):
        pass


# Servidor de prueba en un hilo aparte y en un puerto libre
servidor = HTTPServer(("127.0.0.1", 0), ServidorSilencioso)
puerto = servidor.server_address[1]
threading.Thread(target=servidor.serve_forever, daemon=True).start()


def pedir(ruta, metodo="GET"):
    # Petición cruda (la ruta viaja sin normalizar) y separación de cabeceras y cuerpo
    peticion = (f"{metodo} {ruta} HTTP/1.1\r\nHost: localhost\r\n"
                "Content-Length: 0\r\nConnection: close\r\n\r\n")
    with socket.create_connection(("127.0.0.1", puerto)) as conexion:
        conexion.sendall(peticion.encode())
        datos = b""
        while bloque := conexion.recv(65536):
            datos += bloque
    cabeceras, _, cuerpo = datos.partition(b"\r\n\r\n")
    return cabeceras.decode("latin-1"), cuerpo


def mostrar(descripcion, resultado):
    print(f"OK  {descripcion:48s} -> {resultado}")


# 1. Recursos estáticos y Path Traversal
estaticos = [
    ("/", "200", "text/html"),
    ("/public/index.html", "200", "text/html"),
    ("/public/estilos.css", "200", "text/css"),
    ("/public/app.js", "200", "text/javascript"),
    ("/public/no_existe.css", "404", ""),
    ("/otra-ruta", "404", ""),
    ("/public/../servidor_hibrido.py", "403", ""),
    ("/public/%2e%2e/servidor_hibrido.py", "403", ""),
    ("/public/../../../../etc/passwd", "403", ""),
]
for ruta, codigo, tipo in estaticos:
    cabeceras, _ = pedir(ruta)
    linea_estado = cabeceras.split("\r\n")[0]
    assert codigo in linea_estado and tipo in cabeceras, (ruta, cabeceras)
    mostrar(ruta, linea_estado)


# 2. Motor de búsqueda: filtro, paginación, tope y validación de parámetros
def ids(datos):
    return [equipo["id"] for equipo in datos["resultados"]]


consultas = [
    ("/api/inventario", 200,
     lambda d: d["meta"]["total_coincidencias"] == 120 and len(d["resultados"]) == 10),
    ("/api/inventario?filtro=laptop&limite=5&pagina=2", 200,
     lambda d: d["meta"]["total_coincidencias"] == 15 and ids(d) == [6, 7, 8, 9, 10]),
    ("/api/inventario?filtro=LENOVO", 200,
     lambda d: d["meta"]["total_coincidencias"] == 8),
    ("/api/inventario?limite=1000", 200,
     lambda d: d["meta"]["limite_aplicado"] == 100 and len(d["resultados"]) == 100),
    ("/api/inventario?filtro=tablet", 200,
     lambda d: d["meta"]["total_coincidencias"] == 0 and d["resultados"] == []),
    ("/api/inventario?pagina=dos", 400, lambda d: "enteros" in d["error"]),
    ("/api/inventario?limite=0", 400, lambda d: "mayores que cero" in d["error"]),
]
for ruta, codigo, verificar in consultas:
    cabeceras, cuerpo = pedir(ruta)
    datos = json.loads(cuerpo)
    assert f" {codigo} " in cabeceras.split("\r\n")[0] and verificar(datos), (ruta, datos)
    if codigo == 200:
        meta = datos["meta"]
        resumen = (f"coincidencias={meta['total_coincidencias']}, "
                   f"limite_aplicado={meta['limite_aplicado']}")
    else:
        resumen = datos["error"]
    mostrar(ruta, f"{codigo} | {resumen}")

# 3. Verbos no permitidos
cabeceras, _ = pedir("/api/inventario", "POST")
assert " 405 " in cabeceras and "Allow: GET" in cabeceras
mostrar("POST /api/inventario", "405 | Allow: GET")

servidor.shutdown()
print("Todas las pruebas del Ejercicio 2 fueron superadas.")
