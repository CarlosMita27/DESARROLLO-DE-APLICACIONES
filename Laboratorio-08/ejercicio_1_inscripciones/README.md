# Ejercicio 1: Micro-framework WSGI con middleware de seguridad por token y deserializador polimórfico

**Autor:** Carlos Mita

**Ejecución:** `python servidor_inscripciones.py` y abrir POST http://127.0.0.1:8080/api/inscripciones (cabecera Authorization: Bearer TOKEN_SECRETO_2026)

**Pruebas automáticas:** `python pruebas.py`

**Descripción.** Arquitectura en capas: `MiddlewareErrores -> MiddlewareTokenSeguridad -> aplicacion_inscripciones`. Sin token válido se responde 401; la aplicación acepta solo POST en `/api/inscripciones` (405 y 404 en otros casos), lee el cuerpo de forma acotada, lo deserializa según `CONTENT_TYPE` y valida `dni`, `correo_electronico` y `programa_academico` antes de responder 201.
