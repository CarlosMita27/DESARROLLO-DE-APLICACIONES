# Experiencia N° 3: Inspección del entorno WSGI y diagnóstico de cabeceras

**Autor:** Carlos Mita

**Ejecución:** `python inspector_wsgi.py` y abrir http://127.0.0.1:8080/diagnostico?curso=python&seccion=web

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** La aplicación recorre `environ` y lo clasifica en variables CGI, cabeceras con prefijo `HTTP_` y claves `wsgi.*`. Las variables del sistema operativo que wsgiref copia en cada petición se cuentan, pero no se exponen.
