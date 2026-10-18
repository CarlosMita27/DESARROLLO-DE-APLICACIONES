# =============================================================================
# ARCHIVO:     practica_reflex/ejercicio_2.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Ejercicio 2: panel de indicadores de tareas (reutiliza EstadoKanban del Ejercicio 1).
# =============================================================================
import reflex as rx

from .comunes import pagina
from .ejercicio_1 import EstadoKanban, tablero_kanban


def tarjeta_indicador(titulo: str, valor: rx.Var, fondo: str, borde: str):
    return rx.vstack(
        rx.text(titulo, size="2", weight="medium", text_align="center"),
        rx.heading(valor, size="8"),
        align="center",
        spacing="1",
        padding="14px",
        flex="1",
        min_width="150px",
        background_color=fondo,
        border=f"2px solid {borde}",
        border_radius="10px",
    )


def panel_indicadores():
    return rx.vstack(
        rx.heading("Panel de indicadores", size="6"),
        rx.hstack(
            tarjeta_indicador("Total de tareas", EstadoKanban.total_tareas, "#F0F0F0", "#8A8A8A"),
            tarjeta_indicador("Pendientes", EstadoKanban.total_pendientes, "#FFF4E0", "#E09A1A"),
            tarjeta_indicador("En progreso", EstadoKanban.total_en_progreso, "#E3F0FF", "#3A7BD5"),
            tarjeta_indicador("Completadas", EstadoKanban.total_completadas, "#E6F6E8", "#2E9E4A"),
            tarjeta_indicador(
                "Porcentaje completado", EstadoKanban.porcentaje_completadas, "#F3EAFB", "#8E4EC6"
            ),
            spacing="3",
            width="100%",
            wrap="wrap",
        ),
        spacing="3",
        width="100%",
    )


def pagina_ejercicio2():
    return pagina(panel_indicadores(), tablero_kanban())
