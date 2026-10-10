# Laboratorio N° 08: Python Web

**Autor:** Carlos Mita
**Curso:** Desarrollo de Aplicaciones — Universidad Católica de Santa María
**Fecha:** 10/10/2026

Resolución de las seis experiencias de práctica y de los dos ejercicios propuestos, utilizando solo la biblioteca estándar de Python (3.8 o superior). No requiere instalar dependencias.

## Estructura

| Carpeta | Contenido | Archivo principal | Puerto |
|---|---|---|---|
| `practica_1_servidor_estatico` | Servidor de archivos estáticos con prevención de Path Traversal | `servidor_estatico.py` | 8000 |
| `practica_2_api_rest` | Enrutador HTTP multiverbo RESTful con memoria volátil | `enrutador_api.py` | 8000 |
| `practica_3_inspector_wsgi` | Inspección del entorno WSGI y diagnóstico de cabeceras | `inspector_wsgi.py` | 8080 |
| `practica_4_microframework` | Micro-framework con decoradores, streaming y middlewares | `microframework.py` | 8080 |
| `practica_5_paginacion` | Filtrado y paginación por Query String | `paginacion.py` | 8080 |
| `practica_6_payloads` | Deserializador polimórfico con validación estricta | `deserializador.py` | 8080 |
| `ejercicio_1_inscripciones` | Micro-servicio WSGI con seguridad por token | `servidor_inscripciones.py` | 8080 |
| `ejercicio_2_servidor_hibrido` | Servidor híbrido: archivos estáticos y motor de búsqueda | `servidor_hibrido.py` | 8000 |

Las prácticas 1 y 5 incluyen la versión original de la guía (`servidor_estatico_guia.py` y `paginacion_guia.py`), usada solo para comparar el comportamiento antes y después de las correcciones.

## Ejecución (Símbolo del sistema de Windows)

Un servidor a la vez:

```
cd practica_1_servidor_estatico
python servidor_estatico.py
```

- Pruebas automáticas de una carpeta: `python pruebas.py`
- Pruebas de todo el laboratorio: `python ejecutar_pruebas.py`
- Todos los servidores a la vez (puertos 8001 a 8008): `python ejecutar_todos.py`

En PowerShell se debe escribir `curl.exe` en lugar de `curl`.

## Mejoras respecto al código de la guía

1. **Práctica 1:** `os.path.commonpath` en lugar de `startswith` (la carpeta hermana `public-privado` deja de ser accesible), decodificación de la URL con `unquote`, distinción entre 403 y 404, y tipos MIME explícitos.
2. **Práctica 2:** `Content-Length` negativo o no numérico → 400; mayor que 1 MB → 413; tiempo límite de 10 s → 408; JSON que no es objeto → 400; verbos no admitidos → 405 con `Allow`; decorador de manejo global de errores.
3. **Práctica 3:** clasificación de `environ` en variables CGI, cabeceras `HTTP_` y claves `wsgi.*`, sin exponer las variables del sistema operativo.
4. **Práctica 4:** ruta en streaming con `yield` (`/exportar`) y `MiddlewareErrores` dentro de la cadena de responsabilidad.
5. **Práctica 5:** rechazo de `limite` y `pagina` menores que 1 y metadato `total_paginas`.
6. **Práctica 6:** respuesta 405 con `Allow`, control de tamaño (413), tiempo límite (408) y manejo global de errores.
