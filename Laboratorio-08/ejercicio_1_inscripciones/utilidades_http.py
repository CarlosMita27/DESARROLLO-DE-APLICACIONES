# =============================================================================
# ARCHIVO:      utilidades_http.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Capa de ingesta del micro-servicio de inscripciones: lectura
#               acotada del cuerpo, deserialización polimórfica (JSON o
#               URL-encoded) y validación Fail-Fast del esquema de datos.
# =============================================================================
import re
import json
import socket
from urllib.parse import parse_qs

TAMANO_MAXIMO = 1_048_576  # tope del cuerpo de una petición (1 MB)
CAMPOS_OBLIGATORIOS = ("dni", "correo_electronico", "programa_academico")
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ErrorDePeticion(Exception):
    # Error controlado: transporta el código de estado y el detalle para el cliente
    def __init__(self, estado, mensaje, **detalle):
        super().__init__(mensaje)
        self.estado = estado
        self.contenido = {"error": mensaje, **detalle}


def respuesta_json(start_response, estado, datos, cabeceras_extra=(), exc_info=None):
    # Respuesta JSON uniforme: cuerpo en bytes UTF-8 y Content-Length exacto
    cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
    start_response(estado, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(cuerpo))),
        *cabeceras_extra,
    ], exc_info)
    return [cuerpo]


def leer_cuerpo(environ):
    # 1. Control de I/O: CONTENT_LENGTH debe ser un entero entre 1 y el tope
    try:
        longitud = int(environ.get("CONTENT_LENGTH") or "0")
    except ValueError:
        raise ErrorDePeticion("400 Bad Request", "CONTENT_LENGTH no es un número entero.")
    if longitud <= 0:
        raise ErrorDePeticion("400 Bad Request", "La petición no contiene un cuerpo válido.")
    if longitud > TAMANO_MAXIMO:
        raise ErrorDePeticion("413 Content Too Large",
                              "El cuerpo supera el tamaño máximo de 1 MB.")

    # 2. Lectura acotada: exactamente los bytes declarados, con tiempo límite
    try:
        cuerpo = environ["wsgi.input"].read(longitud)
    except socket.timeout:
        raise ErrorDePeticion("408 Request Timeout",
                              "Tiempo de espera agotado al leer el cuerpo.")
    if len(cuerpo) < longitud:
        raise ErrorDePeticion("400 Bad Request", "El cuerpo recibido está incompleto.")
    return cuerpo


def deserializar_payload(environ, cuerpo):
    # Ingesta polimórfica: la estrategia depende de la cabecera CONTENT_TYPE
    formato = environ.get("CONTENT_TYPE", "")
    try:
        texto = cuerpo.decode("utf-8")
        if "application/json" in formato:
            datos = json.loads(texto)
        elif "application/x-www-form-urlencoded" in formato:
            # parse_qs devuelve listas: se aplanan tomando el primer valor de cada llave
            datos = {clave: valores[0] for clave, valores in parse_qs(texto).items()}
        else:
            raise ErrorDePeticion("415 Unsupported Media Type", "Formatos admitidos: "
                                  "application/json y application/x-www-form-urlencoded.")
    except ValueError:
        # JSONDecodeError y UnicodeDecodeError heredan de ValueError
        raise ErrorDePeticion("400 Bad Request",
                              "El cuerpo no respeta el formato declarado en Content-Type.")
    if not isinstance(datos, dict):
        raise ErrorDePeticion("400 Bad Request",
                              "El cuerpo debe ser un objeto de pares clave-valor.")
    return datos


def validar_esquema(datos):
    # 1. Fail-Fast: se informa cada campo obligatorio ausente o vacío
    faltantes = [campo for campo in CAMPOS_OBLIGATORIOS
                 if not str(datos.get(campo, "")).strip()]
    if faltantes:
        etiqueta = ("Falta el campo obligatorio" if len(faltantes) == 1
                    else "Faltan los campos obligatorios")
        raise ErrorDePeticion("400 Bad Request", f"{etiqueta}: {', '.join(faltantes)}.",
                              campos_faltantes=faltantes)

    # 2. Normalización y validación del formato de cada campo
    aspirante = {campo: str(datos[campo]).strip() for campo in CAMPOS_OBLIGATORIOS}
    if not (aspirante["dni"].isdigit() and len(aspirante["dni"]) == 8):
        raise ErrorDePeticion("400 Bad Request", "El DNI debe tener exactamente 8 dígitos.")
    if not PATRON_CORREO.match(aspirante["correo_electronico"]):
        raise ErrorDePeticion("400 Bad Request",
                              "El correo electrónico no tiene un formato válido.")
    return aspirante
