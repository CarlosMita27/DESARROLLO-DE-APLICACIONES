# =============================================================================
# ARCHIVO:     practica_reflex/ejercicio_3.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Ejercicio 3: sistema de registro de solicitudes con formulario y validación.
# =============================================================================
import re
from typing import Any

import reflex as rx

from .comunes import estilo_tarjeta, pagina

TIPOS_SOLICITUD = ["Consulta", "Incidencia", "Requerimiento"]
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class EstadoSolicitudes(rx.State):
    solicitudes: list[dict[str, str]] = []
    mensaje: str = ""
    exito: bool = False
    siguiente_id: int = 1

    @rx.event
    def registrar(self, datos: dict[str, Any]):
        nombre = str(datos.get("nombre", "")).strip()
        correo = str(datos.get("correo", "")).strip()
        tipo = str(datos.get("tipo", "")).strip()
        descripcion = str(datos.get("descripcion", "")).strip()

        self.exito = False
        if not nombre:
            self.mensaje = "El nombre del solicitante es obligatorio."
        elif not PATRON_CORREO.match(correo):
            self.mensaje = "El correo electrónico no tiene un formato válido."
        elif tipo not in TIPOS_SOLICITUD:
            self.mensaje = "Seleccione un tipo de solicitud."
        elif len(descripcion) < 10:
            self.mensaje = "La descripción debe tener como mínimo diez caracteres."
        else:
            self.solicitudes.append(
                {
                    "id": str(self.siguiente_id),
                    "nombre": nombre,
                    "correo": correo,
                    "tipo": tipo,
                    "descripcion": descripcion,
                }
            )
            self.siguiente_id += 1
            self.exito = True
            self.mensaje = "La solicitud fue registrada correctamente."
            return rx.call_script("document.getElementById('form-solicitud').reset()")

    @rx.event
    def eliminar(self, id_solicitud: str):
        self.solicitudes = [s for s in self.solicitudes if s["id"] != id_solicitud]


def formulario_solicitud():
    return rx.form(
        rx.vstack(
            rx.input(name="nombre", placeholder="Nombre del solicitante", width="100%"),
            rx.input(name="correo", type="email", placeholder="Correo electrónico", width="100%"),
            rx.select(
                TIPOS_SOLICITUD,
                name="tipo",
                default_value="Consulta",
                width="100%",
            ),
            rx.text_area(
                name="descripcion",
                placeholder="Descripción de la solicitud (mínimo 10 caracteres)",
                width="100%",
                rows="4",
            ),
            rx.button("Registrar solicitud", type="submit", color_scheme="green"),
            spacing="3",
            width="100%",
        ),
        on_submit=EstadoSolicitudes.registrar,
        id="form-solicitud",
        width="100%",
    )


def tarjeta_solicitud(solicitud: rx.Var[dict[str, str]]):
    return rx.box(
        rx.hstack(
            rx.heading(solicitud["nombre"], size="3"),
            rx.badge(
                solicitud["tipo"],
                color_scheme=rx.match(
                    solicitud["tipo"],
                    ("Consulta", "blue"),
                    ("Incidencia", "red"),
                    "green",
                ),
            ),
            rx.spacer(),
            rx.button(
                "Eliminar",
                on_click=EstadoSolicitudes.eliminar(solicitud["id"]),
                color_scheme="red",
                size="1",
            ),
            width="100%",
            align="center",
        ),
        rx.text(solicitud["correo"], size="2", color="gray"),
        rx.text(solicitud["descripcion"], margin_top="6px"),
        padding="12px",
        width="100%",
        background_color="#F5F5F5",
        border="1px solid #D5D5D5",
        border_radius="8px",
    )


def sistema_solicitudes():
    return rx.vstack(
        rx.vstack(
            rx.heading("Registro de solicitudes", size="6"),
            formulario_solicitud(),
            rx.cond(
                EstadoSolicitudes.mensaje != "",
                rx.cond(
                    EstadoSolicitudes.exito,
                    rx.callout(EstadoSolicitudes.mensaje, color_scheme="green", width="100%"),
                    rx.callout(EstadoSolicitudes.mensaje, color_scheme="red", width="100%"),
                ),
            ),
            spacing="3",
            style=estilo_tarjeta,
        ),
        rx.vstack(
            rx.heading("Solicitudes registradas", size="5"),
            rx.cond(
                EstadoSolicitudes.solicitudes.length() > 0,
                rx.vstack(
                    rx.foreach(EstadoSolicitudes.solicitudes, tarjeta_solicitud),
                    spacing="2",
                    width="100%",
                ),
                rx.text("Aún no hay solicitudes registradas.", color="gray"),
            ),
            spacing="3",
            style=estilo_tarjeta,
        ),
        spacing="4",
        width="100%",
    )


def pagina_ejercicio3():
    return pagina(sistema_solicitudes())
