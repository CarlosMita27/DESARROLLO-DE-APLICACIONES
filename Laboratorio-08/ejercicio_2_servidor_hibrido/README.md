# Ejercicio 2: Servidor híbrido HTTP con prevención de Path Traversal y motor de búsqueda

**Autor:** Carlos Mita

**Ejecución:** `python servidor_hibrido.py` y abrir http://127.0.0.1:8000/

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** Sirve la interfaz de `public/` con validación de frontera (403) e inferencia MIME, y expone `/api/inventario` con los parámetros `filtro`, `limite` (tope de 100) y `pagina`, paginación Offset/Limit y respuestas 200 o 400 en JSON.
