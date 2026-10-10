# Experiencia N° 4: Micro-framework con decoradores y cadena de responsabilidad

**Autor:** Carlos Mita

**Ejecución:** `python microframework.py` y abrir http://127.0.0.1:8080/saludo

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** `NucleoWSGI` registra las rutas con el decorador `@app.registrar_endpoint`. La ruta `/exportar` responde en streaming con un generador (`yield`). La cadena de middlewares es `MiddlewareAuditoria -> MiddlewareErrores -> NucleoWSGI`; la ruta `/fallo` comprueba el manejo global de errores (500).
