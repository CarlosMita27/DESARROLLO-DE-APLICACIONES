# =============================================================================
# ARCHIVO:      aplicacion_inscripciones.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Aplicación WSGI principal del micro-servicio. Acepta solo POST
#               en /api/inscripciones, procesa el cuerpo con la capa de ingesta
#               y registra la inscripción en memoria (201 Created).
# =============================================================================
from datetime import datetime
from utilidades_http import (ErrorDePeticion, respuesta_json, leer_cuerpo,
                             deserializar_payload, validar_esquema)

RUTA_INSCRIPCIONES = "/api/inscripciones"
inscripciones = []  # almacenamiento volátil en memoria


def aplicacion_inscripciones(environ, start_response):
    # 1. Enrutamiento: ruta desconocida -> 404; verbo distinto de POST -> 405
    if environ.get("PATH_INFO") != RUTA_INSCRIPCIONES:
        return respuesta_json(start_response, "404 Not Found",
                              {"error": "Ruta no encontrada."})
    if environ.get("REQUEST_METHOD") != "POST":
        return respuesta_json(start_response, "405 Method Not Allowed",
                              {"error": "Este endpoint solo acepta POST."},
                              [("Allow", "POST")])

    # 2. Ingesta: lectura acotada, deserialización polimórfica y validación Fail-Fast
    try:
        cuerpo = leer_cuerpo(environ)
        datos = deserializar_payload(environ, cuerpo)
        aspirante = validar_esquema(datos)
    except ErrorDePeticion as error:
        return respuesta_json(start_response, error.estado, error.contenido)

    # 3. Registro de la inscripción y confirmación con 201 Created
    inscripcion = {"id": len(inscripciones) + 1, **aspirante,
                   "fecha_registro": datetime.now().isoformat(timespec="seconds")}
    inscripciones.append(inscripcion)
    return respuesta_json(start_response, "201 Created",
                          {"estado": "Inscripción registrada", "datos": inscripcion})
