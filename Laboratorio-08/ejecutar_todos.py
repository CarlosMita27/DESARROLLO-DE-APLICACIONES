# =============================================================================
# ARCHIVO:      ejecutar_todos.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Levanta a la vez las seis prácticas y los dos ejercicios, cada
#               uno en su propio puerto (8001 a 8008) y en su propio hilo.
# =============================================================================
import os
import sys
import threading
from http.server import HTTPServer
from wsgiref.simple_server import make_server

# Cada carpeta del laboratorio se agrega a la ruta de importación
RAIZ = os.path.dirname(os.path.abspath(__file__))
for carpeta in sorted(os.listdir(RAIZ)):
    if carpeta.startswith(("practica_", "ejercicio_")):
        sys.path.insert(0, os.path.join(RAIZ, carpeta))

from servidor_estatico import ServidorEstaticoFortificado
from enrutador_api import EnrutadorAPI
from inspector_wsgi import inspector_entorno_wsgi
from microframework import aplicacion_fortificada
from paginacion import endpoint_inventario_paginado
from deserializador import aplicacion as aplicacion_payloads
from deserializador import ManejadorConTiempoLimite as Manejador
from servidor_inscripciones import aplicacion as aplicacion_inscripciones
from servidor_hibrido import ServidorHibrido

# Tabla de servidores: nombre, instancia y ruta sugerida
servidores = [
    ("Práctica 1 - Servidor estático",
     HTTPServer(("127.0.0.1", 8001), ServidorEstaticoFortificado), "/"),
    ("Práctica 2 - API REST",
     HTTPServer(("127.0.0.1", 8002), EnrutadorAPI), "/api/usuarios"),
    ("Práctica 3 - Inspector WSGI",
     make_server("127.0.0.1", 8003, inspector_entorno_wsgi), "/diagnostico?a=1"),
    ("Práctica 4 - Micro-framework",
     make_server("127.0.0.1", 8004, aplicacion_fortificada), "/saludo"),
    ("Práctica 5 - Paginación",
     make_server("127.0.0.1", 8005, endpoint_inventario_paginado), "/?limite=15&pagina=2"),
    ("Práctica 6 - Payloads (POST)",
     make_server("127.0.0.1", 8006, aplicacion_payloads, handler_class=Manejador), "/"),
    ("Ejercicio 1 - Inscripciones (POST + token)",
     make_server("127.0.0.1", 8007, aplicacion_inscripciones, handler_class=Manejador),
     "/api/inscripciones"),
    ("Ejercicio 2 - Servidor híbrido",
     HTTPServer(("127.0.0.1", 8008), ServidorHibrido), "/"),
]

# Cada servidor atiende en un hilo independiente
for nombre, servidor, ruta in servidores:
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    print(f"{nombre}: http://127.0.0.1:{servidor.server_address[1]}{ruta}")

print("\nPresione Ctrl + C para detener todos los servidores.")
try:
    threading.Event().wait()
except KeyboardInterrupt:
    for _, servidor, _ in servidores:
        servidor.shutdown()
        servidor.server_close()
    print("Servidores detenidos.")
