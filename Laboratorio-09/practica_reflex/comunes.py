# =============================================================================
# ARCHIVO:     practica_reflex/comunes.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Colores, estilos reutilizables, barra de navegación y estructura común de página.
# =============================================================================
import reflex as rx

COLOR_PRIMARIO = "#1B6B2F"
COLOR_FONDO = "#F4F8F4"
COLOR_TEXTO = "#1F2A1F"

estilo_tarjeta = {
    "padding": "16px",
    "background_color": "#FFFFFF",
    "border": "1px solid #CFE0CF",
    "border_radius": "10px",
    "box_shadow": "0 2px 6px #00000020",
    "width": "100%",
}

estilo_pagina = {
    "width": "100%",
    "max_width": "960px",
    "padding": "24px",
    "align_items": "center",
}

ENLACES = [
    ("Inicio", "/"),
    ("Tareas", "/tareas"),
    ("Contacto", "/contacto"),
    ("Usuarios", "/usuarios"),
    ("Ejercicio 1", "/ejercicio1"),
    ("Ejercicio 2", "/ejercicio2"),
    ("Ejercicio 3", "/ejercicio3"),
    ("Ejercicio 4", "/ejercicio4"),
]


def barra_navegacion():
    return rx.hstack(
        *[rx.link(texto, href=ruta, color="white") for texto, ruta in ENLACES],
        spacing="5",
        wrap="wrap",
        padding="14px 24px",
        width="100%",
        justify="center",
        background_color=COLOR_PRIMARIO,
    )


def pagina(*contenido):
    return rx.vstack(
        barra_navegacion(),
        rx.vstack(*contenido, spacing="4", style=estilo_pagina),
        width="100%",
        min_height="100vh",
        align="center",
        spacing="0",
        background_color=COLOR_FONDO,
        color=COLOR_TEXTO,
    )
