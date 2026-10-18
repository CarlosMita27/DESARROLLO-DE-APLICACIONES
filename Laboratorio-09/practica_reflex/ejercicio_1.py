# =============================================================================
# ARCHIVO:     practica_reflex/ejercicio_1.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Ejercicio 1: tablero Kanban con filtro dinámico (EstadoKanban, tarjeta_kanban, tablero_kanban).
# =============================================================================
import reflex as rx

from .comunes import pagina

ESTADOS = ["Pendiente", "En progreso", "Completada"]

# ---------------------------------------------------------------------------
# Ejercicio 1: tablero Kanban con filtro dinámico
# ---------------------------------------------------------------------------


class EstadoKanban(rx.State):
    tareas: list[dict[str, str]] = [
        {
            "id": "1",
            "titulo": "Diseñar la interfaz",
            "descripcion": "Definir la estructura visual del tablero.",
            "estado": "Completada",
        },
        {
            "id": "2",
            "titulo": "Declarar el estado",
            "descripcion": "Crear la clase de estado que administra las tareas.",
            "estado": "Completada",
        },
        {
            "id": "3",
            "titulo": "Crear la tarjeta",
            "descripcion": "Implementar el componente reutilizable de tarea.",
            "estado": "En progreso",
        },
        {
            "id": "4",
            "titulo": "Implementar el filtro",
            "descripcion": "Mostrar únicamente las tareas pendientes.",
            "estado": "En progreso",
        },
        {
            "id": "5",
            "titulo": "Probar el tablero",
            "descripcion": "Cambiar estados y verificar la actualización.",
            "estado": "Pendiente",
        },
        {
            "id": "6",
            "titulo": "Redactar el informe",
            "descripcion": "Incluir capturas y explicaciones del laboratorio.",
            "estado": "Pendiente",
        },
    ]
    mostrar_solo_pendientes: bool = False

    @rx.var
    def tareas_visibles(self) -> list[dict[str, str]]:
        if self.mostrar_solo_pendientes:
            return [t for t in self.tareas if t["estado"] == "Pendiente"]
        return self.tareas

    @rx.var
    def total_tareas(self) -> int:
        return len(self.tareas)

    @rx.var
    def total_pendientes(self) -> int:
        return sum(1 for t in self.tareas if t["estado"] == "Pendiente")

    @rx.var
    def total_en_progreso(self) -> int:
        return sum(1 for t in self.tareas if t["estado"] == "En progreso")

    @rx.var
    def total_completadas(self) -> int:
        return sum(1 for t in self.tareas if t["estado"] == "Completada")

    @rx.var
    def porcentaje_completadas(self) -> str:
        total = len(self.tareas)
        if total == 0:
            return "0%"
        return f"{round(self.total_completadas * 100 / total)}%"

    @rx.event
    def alternar_filtro(self):
        self.mostrar_solo_pendientes = not self.mostrar_solo_pendientes

    @rx.event
    def cambiar_estado(self, id_tarea: str, estado: str):
        for tarea in self.tareas:
            if tarea["id"] == id_tarea:
                tarea["estado"] = estado


def tarjeta_kanban(tarea: rx.Var[dict[str, str]]):
    return rx.box(
        rx.heading(tarea["titulo"], size="3"),
        rx.text(tarea["descripcion"], size="2", color="gray"),
        rx.select(
            ESTADOS,
            value=tarea["estado"],
            on_change=lambda estado: EstadoKanban.cambiar_estado(tarea["id"], estado),
            size="1",
            margin_top="8px",
        ),
        padding="12px",
        border_radius="8px",
        width="100%",
        border="1px solid #CFE0CF",
        background_color=rx.match(
            tarea["estado"],
            ("Pendiente", "#FFF4E0"),
            ("En progreso", "#E3F0FF"),
            "#E6F6E8",
        ),
    )


def columna_kanban(estado: str, color: str):
    return rx.vstack(
        rx.heading(estado, size="4", color=color),
        rx.foreach(
            EstadoKanban.tareas_visibles,
            lambda tarea: rx.cond(tarea["estado"] == estado, tarjeta_kanban(tarea)),
        ),
        spacing="3",
        align="start",
        flex="1",
        min_width="220px",
        padding="12px",
        background_color="#FFFFFF",
        border="1px solid #CFE0CF",
        border_radius="10px",
    )


def tablero_kanban():
    return rx.vstack(
        rx.hstack(
            rx.heading("Tablero Kanban", size="6"),
            rx.spacer(),
            rx.button(
                rx.cond(
                    EstadoKanban.mostrar_solo_pendientes,
                    "Mostrar todas las tareas",
                    "Mostrar solo pendientes",
                ),
                on_click=EstadoKanban.alternar_filtro,
                color_scheme=rx.cond(EstadoKanban.mostrar_solo_pendientes, "orange", "green"),
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            EstadoKanban.mostrar_solo_pendientes,
            rx.text("Filtro activo: se muestran únicamente las tareas pendientes.", color="orange"),
            rx.text("Se muestran todas las tareas registradas.", color="gray"),
        ),
        rx.cond(
            EstadoKanban.tareas_visibles.length() == 0,
            rx.callout("No existen tareas que cumplan con el filtro.", color_scheme="orange"),
            rx.hstack(
                columna_kanban("Pendiente", "#B26A00"),
                columna_kanban("En progreso", "#1A5FB4"),
                columna_kanban("Completada", "#1B6B2F"),
                spacing="3",
                width="100%",
                align="start",
                wrap="wrap",
            ),
        ),
        spacing="3",
        width="100%",
    )


def pagina_ejercicio1():
    return pagina(tablero_kanban())
