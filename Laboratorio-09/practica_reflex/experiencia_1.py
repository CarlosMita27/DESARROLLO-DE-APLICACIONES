# =============================================================================
# ARCHIVO:     practica_reflex/experiencia_1.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Experiencia 1: interfaz inicial (index) y contador con estado (EstadoContador).
# =============================================================================
import reflex as rx

from .comunes import COLOR_PRIMARIO, estilo_tarjeta, pagina


# --- Estado: almacena el valor del contador y los manejadores que lo modifican ---
class EstadoContador(rx.State):
    conteo: int = 0  # variable de estado (valor inicial 0)

    @rx.event
    def incrementar(self):
        self.conteo += 1  # suma 1 al valor actual

    @rx.event
    def disminuir(self):
        self.conteo -= 1  # resta 1 al valor actual

    @rx.event
    def reiniciar(self):
        self.conteo = 0  # vuelve al valor inicial


# --- Mensaje condicional: positivo, negativo o cero según el valor de conteo ---
def mensaje_contador():
    return rx.cond(
        EstadoContador.conteo > 0,
        rx.text("El contador es positivo.", color="green", weight="bold"),
        rx.cond(
            EstadoContador.conteo < 0,
            rx.text("El contador es negativo.", color="red", weight="bold"),
            rx.text("El contador es igual a cero.", color="gray", weight="bold"),
        ),
    )


# --- Componente contador: valor, mensaje y tres botones vinculados con on_click ---
def contador():
    return rx.vstack(
        rx.heading(EstadoContador.conteo, size="9"),
        mensaje_contador(),
        rx.hstack(
            rx.button("Incrementar", on_click=EstadoContador.incrementar, color_scheme="green"),
            rx.button("Disminuir", on_click=EstadoContador.disminuir, color_scheme="red"),
            rx.button("Reiniciar", on_click=EstadoContador.reiniciar, color_scheme="gray"),
            spacing="3",
        ),
        align="center",
        spacing="3",
        style=estilo_tarjeta,
    )


# --- Página principal: título, equipo, descripción, botón de navegación y contador ---
def index():
    return pagina(
        rx.heading("Práctica Reflex", size="8", color=COLOR_PRIMARIO),
        rx.text("Equipo: Ingeniería de Sistemas - UCSM", weight="medium"),
        rx.text(
            "Aplicación desarrollada con Reflex para el curso de Desarrollo de Aplicaciones.",
            text_align="center",
        ),
        rx.button("Ir a la lista de tareas", on_click=rx.redirect("/tareas"), color_scheme="green"),
        contador(),
    )
