# Experiencia N° 6: Deserializador polimórfico de payloads con validación estricta

**Autor:** Carlos Mita

**Ejecución:** `python deserializador.py` y abrir http://127.0.0.1:8080/ (solo POST y PUT)

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** Acepta POST y PUT (405 con `Allow` en otro caso), valida `CONTENT_LENGTH` (400, 413) y lee exactamente esa cantidad de bytes con tiempo límite (408). Según `CONTENT_TYPE` usa `json.loads` o `parse_qs` con aplanamiento (415 para otros formatos) y valida las llaves obligatorias con una resta de conjuntos (Fail-Fast).
