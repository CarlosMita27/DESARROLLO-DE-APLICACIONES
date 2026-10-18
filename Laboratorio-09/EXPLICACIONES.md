# Laboratorio N° 09: Reflex — Explicaciones de las experiencias

## Ejecución del proyecto

```
uv sync
uv run reflex run
```

Requisitos: Python 3.11 o superior, `uv`, Node.js 22.22 o superior y Bun.

La aplicación se abre en `http://localhost:3000` y todas las páginas se acceden desde la barra de navegación:

| Página | Contenido |
|---|---|
| `/` | Experiencia 01: interfaz inicial y contador |
| `/tareas` | Experiencia 02: lista de tareas |
| `/contacto` | Experiencia 03: formulario de contacto |
| `/usuarios` | Experiencia 04: consumo de API |
| `/ejercicio1` | Ejercicio 1: tablero Kanban con filtro dinámico |
| `/ejercicio2` | Ejercicio 2: panel de indicadores |
| `/ejercicio3` | Ejercicio 3: sistema de registro de solicitudes |
| `/ejercicio4` | Ejercicio 4: directorio de usuarios con búsqueda |

Organización del código (`practica_reflex/`):

- `practica_reflex.py`: crea la aplicación y registra las páginas.
- `comunes.py`: estilos, barra de navegación y estructura común de página.
- `experiencia_1.py` a `experiencia_4.py`: Experiencias 01 a 04.
- `ejercicio_1.py` a `ejercicio_4.py`: Ejercicios 1 a 4 (código de referencia).

---

## Experiencia 01: Creación de una aplicación interactiva

### Función de cada elemento del proyecto

- `rxconfig.py`: contiene la configuración principal de Reflex, como el nombre de la aplicación.
- `pyproject.toml`: registra las dependencias y la configuración del proyecto Python.
- `assets/`: almacena recursos estáticos, como imágenes y archivos utilizados por la interfaz.
- `practica_reflex/`: paquete de Python que contiene el código de la aplicación.
- `practica_reflex.py`: contiene la interfaz principal, los estados y el registro de las páginas.

### Función de Python frente a componentes de Reflex

Una función de Python como `contador()` o `tarjeta_tarea()` agrupa y reutiliza una estructura visual que el desarrollador define. Los componentes de Reflex (`rx.heading()`, `rx.text()`, `rx.button()`, `rx.vstack()`) son los elementos básicos que Reflex proporciona y que se traducen a elementos de la interfaz. Las funciones propias se construyen combinando los componentes de Reflex.

### Qué sucede desde que se presiona un botón hasta que cambia la interfaz

1. El usuario presiona el botón «Incrementar».
2. El evento `on_click` detecta la acción y Reflex envía el evento al servidor.
3. El backend ejecuta el manejador `incrementar()`.
4. La variable de estado `conteo` cambia de 0 a 1.
5. Reflex envía el nuevo valor al navegador y la interfaz muestra el resultado actualizado, sin recargar la página.

---

## Experiencia 02: Componentes reutilizables y listas dinámicas

### Ventajas de un componente reutilizable

`tarjeta_tarea()` se define una sola vez y se utiliza para todas las tareas. Esto evita repetir código, garantiza que todas las tareas compartan el mismo diseño y permite modificar la presentación en un único lugar.

### Relación entre `rx.State`, `rx.foreach()`, los eventos y los componentes

`EstadoTareas` almacena la lista `tareas`. El formulario envía el texto al manejador `agregar_tarea()` y el botón Eliminar ejecuta `eliminar_tarea()`. Ambos manejadores modifican la lista del estado. Como `rx.foreach()` está vinculado a esa variable, Reflex vuelve a generar las tarjetas con `tarjeta_tarea()` cada vez que la lista cambia. Además, `rx.cond()` muestra el mensaje «No hay tareas registradas» cuando la lista está vacía.

---

## Experiencia 03: Formularios y validación de datos

### Pruebas sugeridas

1. Enviar el formulario con todos los campos vacíos: el navegador solicita completar los campos obligatorios.
2. Ingresar un correo incorrecto, por ejemplo `correo@`: el navegador o el servidor lo rechazan.
3. Ingresar un mensaje de menos de diez caracteres: se muestra el mensaje de error correspondiente.
4. Ingresar datos válidos: se muestra la confirmación con el nombre de la persona y el formulario se limpia (`reset_on_submit=True`).

### Validación del navegador frente a validación en Python

La validación del navegador (`required=True`, `type="email"`) se ejecuta en el cliente antes de enviar los datos. Mejora la experiencia del usuario, pero puede omitirse fácilmente, por ejemplo, desactivando JavaScript o enviando una solicitud manual. La validación en Python se ejecuta en el servidor, dentro de `enviar()`, y no puede eludirse desde el cliente. Por ello, es la que garantiza la integridad de los datos y debe mantenerse aunque exista validación en el navegador.

---

## Experiencia 04: Consumo de información desde una API

### Por qué se procesa la respuesta antes de mostrarla

La API devuelve objetos con muchos campos y estructuras anidadas (por ejemplo, `address` y `company`). Para mostrar únicamente nombre, usuario, correo y empresa, se extraen esos valores y se almacenan en una lista de diccionarios simples. Esto facilita su uso con `rx.foreach()` y evita errores al intentar mostrar estructuras complejas.

### Recorrido de la información desde la API hasta la interfaz

1. El usuario presiona «Cargar usuarios» y se ejecuta el manejador asincrónico `cargar_usuarios()`.
2. El manejador activa `cargando` y, mediante `yield`, envía ese cambio a la interfaz, que muestra «Cargando usuarios...».
3. `httpx.AsyncClient` realiza la solicitud GET a `https://jsonplaceholder.typicode.com/users`.
4. `raise_for_status()` genera una excepción si la respuesta es incorrecta.
5. La respuesta JSON se procesa y se guarda en la variable de estado `usuarios`.
6. Si ocurre un error, se almacena un mensaje en `error`.
7. `rx.cond()` decide si se muestra el indicador de carga, el error o la lista, y `rx.foreach()` genera una `tarjeta_usuario()` por cada usuario.

### Prueba de error

Para simular un fallo, cambie temporalmente la constante `URL_USUARIOS` por una dirección inexistente (por ejemplo, `.../usuariosx`), presione el botón y verifique el mensaje de error. Luego restablezca la dirección correcta.

---

# Ejercicios propuestos

## Ejercicio 1: Tablero Kanban con filtro dinámico

- `EstadoKanban` administra una colección de seis tareas, cada una con identificador, título, descripción y estado (Pendiente, En progreso o Completada).
- `tarjeta_kanban()` es el componente reutilizable que representa cada tarea. Su color de fondo depende del estado y contiene un selector para cambiarlo.
- El tablero se organiza en tres columnas, generadas con `rx.foreach()` sobre la propiedad calculada `tareas_visibles`.
- La variable booleana `mostrar_solo_pendientes` se inicia en `False` y el botón de filtro la alterna mediante `alternar_filtro()`.
- La propiedad calculada `tareas_visibles` (`@rx.var`) devuelve solo las pendientes cuando el filtro está activo.
- `rx.cond()` modifica el texto del botón y el mensaje informativo, y muestra «No existen tareas que cumplan con el filtro» cuando no hay resultados.
- Al cambiar el estado de una tarea mediante `cambiar_estado()`, el tablero se actualiza automáticamente.

## Ejercicio 2: Panel de indicadores de tareas

- Reutiliza la colección y los estados del ejercicio anterior (`EstadoKanban`).
- `panel_indicadores()` muestra cinco tarjetas creadas con el componente reutilizable `tarjeta_indicador()`: total, pendientes, en progreso, completadas y porcentaje completado.
- Cada valor se obtiene con una propiedad calculada (`total_tareas`, `total_pendientes`, `total_en_progreso`, `total_completadas`, `porcentaje_completadas`), por lo que se actualiza solo al cambiar el estado de una tarea.
- `porcentaje_completadas` devuelve `0%` cuando no existen tareas, evitando la división entre cero.
- Cada indicador tiene un color distinto para diferenciar los estados.
- La página incluye también el tablero para verificar que los indicadores coinciden con la información existente.

## Ejercicio 3: Sistema de registro de solicitudes

- El formulario contiene nombre, correo electrónico, tipo de solicitud (`rx.select` con Consulta, Incidencia y Requerimiento) y descripción.
- `EstadoSolicitudes.registrar()` procesa los datos mediante `on_submit` y valida que el nombre no esté vacío, que el correo tenga un formato válido, que se haya elegido un tipo y que la descripción tenga como mínimo diez caracteres.
- Se muestra un mensaje de error o de confirmación según el resultado.
- Las solicitudes válidas se almacenan en una colección dentro del estado y se muestran con `rx.foreach()` mediante el componente reutilizable `tarjeta_solicitud()`.
- Cada tarjeta incluye un botón para eliminar la solicitud.
- Los campos se limpian solo cuando el registro es exitoso; si hay un error, se conserva lo escrito para que el usuario lo corrija.

## Ejercicio 4: Directorio de usuarios con búsqueda dinámica

- `EstadoDirectorio.cargar_usuarios()` es un manejador asincrónico que consulta la API con HTTPX, procesa la respuesta y guarda nombre, usuario, correo, ciudad y empresa.
- Las variables `cargando` y `error` permiten mostrar «Cargando usuarios...» y el mensaje de error cuando la consulta falla.
- `tarjeta_directorio()` representa a cada usuario y `rx.foreach()` genera las tarjetas.
- El campo de búsqueda actualiza la variable `busqueda` en cada cambio y la propiedad calculada `usuarios_filtrados` devuelve los usuarios cuyo nombre coincide, sin distinguir mayúsculas de minúsculas (`lower().find(...) != -1`).
- Si no hay coincidencias se muestra un mensaje informativo.
- El botón **Actualizar** vuelve a consultar la API conservando el texto de búsqueda.
- Los usuarios se cargan automáticamente al abrir la página.
