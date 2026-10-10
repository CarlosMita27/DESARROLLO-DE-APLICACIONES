# Experiencia N° 1: Servidor de archivos estáticos con prevención de Path Traversal

**Autor:** Carlos Mita

**Ejecución:** `python servidor_estatico.py` y abrir http://127.0.0.1:8000/

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** El servidor expone solo la carpeta `public/`. La ruta se decodifica con `unquote`, se une al directorio base y se normaliza con `os.path.abspath`; luego `os.path.commonpath` verifica que permanezca dentro de `public/` (403 en caso contrario y 404 si el archivo no existe). El tipo MIME se infiere con `mimetypes` y el archivo se transmite en binario por `self.wfile`. `servidor_estatico_guia.py` conserva la validación original con `startswith`, que permite leer `public-privado/clave.txt`.
