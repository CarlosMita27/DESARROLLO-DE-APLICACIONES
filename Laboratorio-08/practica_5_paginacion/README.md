# Experiencia N° 5: Motor de filtrado, búsqueda y paginación por Query String

**Autor:** Carlos Mita

**Ejecución:** `python paginacion.py` y abrir http://127.0.0.1:8080/api/inventario?limite=15&pagina=2

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** El endpoint interpreta `QUERY_STRING` con `parse_qs`, convierte los valores a entero, rechaza los no numéricos y los menores que 1 con 400, aplica un tope de 50 registros y pagina con `(pagina - 1) * limite`. `paginacion_guia.py` conserva la versión original, que acepta valores negativos.
