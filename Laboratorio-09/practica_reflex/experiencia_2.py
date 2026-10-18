# =============================================================================
# ARCHIVO:     practica_reflex/experiencia_2.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Experiencia 2: componentes reutilizables y lista dinámica de tareas (EstadoTareas).
# =============================================================================
from typing import Any

import reflex as rx

from .comunes import estilo_tarjeta, pagina


# --- Estado: lista de tareas y manejadores para agregar y eliminar ---
class EstadoTareas(rx.State):
    tareas: list[str] = [
        "Diseñar interfaz",
        "Crear componentes",
        "Probar aplicación",
        "Documentar el laboratorio",
    ]

    @rx.event
    def agregar_tarea(self, datos: dict[str, Any]):
        # Los datos del formulario llegan en un diccionario {name: valor}
        nueva = str(datos.get("tarea", "")).strip()  # strip() elimina espacios sobrantes
        if nueva:  # una cadena vacía o de solo espacios se ignora
            self.tareas.append(nueva)

    @rx.event
    def eliminar_tarea(self, indice: int):
        self.tareas.pop(indice)  # elimina la tarea de la posición indicada


# --- Componente reutilizable: una tarjeta por tarea, con botón Eliminar ---
def tarjeta_tarea(tarea: rx.Var[str], indice: rx.Var[int]):
    return rx.hstack(
        rx.text(tarea),
        rx.spacer(),
        rx.button(
            "Eliminar",
            on_click=EstadoTareas.eliminar_tarea(indice),
            color_scheme="red",
            size="1",
        ),
        align="center",
        padding="12px",
        background_color="#E8F0FE",
        border="1px solid #B6C8EA",
        border_radius="8px",
        width="100%",
    )


# --- Formulario para agregar tareas; se limpia después de cada envío ---
def formulario_tarea():
    return rx.form(
        rx.hstack(
            rx.input(name="tarea", placeholder="Nueva tarea", width="100%"),
            rx.button("Agregar tarea", type="submit", color_scheme="green"),
            width="100%",
        ),
        on_submit=EstadoTareas.agregar_tarea,
        reset_on_submit=True,
        width="100%",
    )


# --- Lista: rx.foreach genera una tarjeta por elemento; rx.cond cubre la lista vacía ---
def lista_tareas():
    return rx.vstack(
        rx.heading("Lista de tareas", size="6"),
        formulario_tarea(),
        rx.cond(
            EstadoTareas.tareas.length() > 0,
            rx.vstack(
                rx.foreach(EstadoTareas.tareas, tarjeta_tarea),
                spacing="2",
                width="100%",
            ),
            rx.text("No hay tareas registradas", color="gray"),
        ),
        spacing="3",
        style=estilo_tarjeta,
    )


def pagina_tareas():
    return pagina(lista_tareas())
