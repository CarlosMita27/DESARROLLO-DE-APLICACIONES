# =============================================================================
# ARCHIVO:      inspector_wsgi.py
# AUTOR:        Carlos Mita
# FECHA:        10/10/2026
# DESCRIPCIÓN:  Aplicación WSGI de diagnóstico. Recorre el diccionario environ,
#               clasifica sus claves (variables CGI, cabeceras HTTP_ y claves
#               wsgi.*) y las devuelve en JSON, sin exponer las variables del
#               sistema operativo que wsgiref copia en cada petición.
# =============================================================================
import os
import json
from wsgiref.simple_server import make_server


def inspector_entorno_wsgi(environ, start_response):
    # 1. Introspección: clasificación de cada clave de environ en tres grupos
    variables_cgi, cabeceras_http, claves_wsgi = {}, {}, {}
    omitidas = 0
    for clave, valor in environ.items():
        if os.environ.get(clave) == valor:
            # Variable copiada del sistema operativo: se cuenta, pero no se expone
            omitidas += 1
        elif clave.startswith("HTTP_"):
            cabeceras_http[clave] = valor
        elif clave.startswith("wsgi."):
            # wsgi.input y wsgi.errors son flujos: se muestra su representación en texto
            claves_wsgi[clave] = valor if isinstance(valor, str) else repr(valor)
        else:
            variables_cgi[clave] = valor

    # 2. Serialización ordenada y legible del diagnóstico
    diagnostico = {
        "variables_cgi": dict(sorted(variables_cgi.items())),
        "cabeceras_http": dict(sorted(cabeceras_http.items())),
        "claves_wsgi": dict(sorted(claves_wsgi.items())),
        "variables_del_sistema_omitidas": omitidas,
    }
    cuerpo_bytes = json.dumps(diagnostico, indent=4, ensure_ascii=False).encode("utf-8")

    # 3. Contrato WSGI: estado y cabeceras con start_response, cuerpo como iterable de bytes
    start_response("200 OK", [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(cuerpo_bytes))),
    ])
    return [cuerpo_bytes]


if __name__ == "__main__":
    # Servidor de referencia wsgiref: traduce cada petición HTTP al diccionario environ
    servidor = make_server("127.0.0.1", 8080, inspector_entorno_wsgi)
    print("Inspector WSGI en http://127.0.0.1:8080  (Ctrl + C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        servidor.server_close()
        print("Servidor detenido.")
