# Experiencia N° 2: Enrutador HTTP multiverbo RESTful con memoria volátil

**Autor:** Carlos Mita

**Ejecución:** `python enrutador_api.py` y abrir http://127.0.0.1:8000/api/usuarios

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** El recurso `/api/usuarios` opera sobre una lista en memoria. GET devuelve la colección y POST crea un registro (201). El cuerpo se lee de forma acotada: `Content-Length` negativo o no numérico produce 400, mayor que 1 MB produce 413 y un cuerpo que no llega a tiempo produce 408. Los verbos no admitidos reciben 405 con la cabecera `Allow`.
