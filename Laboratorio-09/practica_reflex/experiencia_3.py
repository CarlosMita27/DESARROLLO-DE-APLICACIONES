# =============================================================================
# ARCHIVO:     practica_reflex/experiencia_3.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Experiencia 3: formulario de contacto con validación en Python (EstadoContacto).
# =============================================================================
import re
from typing import Any

import reflex as rx

from .comunes import estilo_tarjeta, pagina

# Expresión regular de un correo básico: usuario@dominio.ext
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


# --- Estado: mensaje de respuesta y bandera de éxito; enviar() valida los datos ---
class EstadoContacto(rx.State):
    respuesta: str = ""
    exito: bool = False

    @rx.event
    def enviar(self, datos: dict[str, Any]):
        nombre = str(datos.get("nombre", "")).strip()
        correo = str(datos.get("correo", "")).strip()
        mensaje = str(datos.get("mensaje", "")).strip()

        # Validaciones en orden; la primera que falla define el mensaje de error
        if not nombre:
            self.exito = False
            self.respuesta = "El nombre no puede estar vacío."
        elif not PATRON_CORREO.match(correo):
            self.exito = False
            self.respuesta = "El correo electrónico no tiene un formato válido."
        elif not mensaje:
            self.exito = False
            self.respuesta = "El mensaje no puede estar vacío."
        elif len(mensaje) < 10:
            self.exito = False
            self.respuesta = "El mensaje debe tener como mínimo diez caracteres."
        else:
            self.exito = True
            self.respuesta = f"Gracias, {nombre}. Su mensaje fue enviado correctamente."
            # Los campos se limpian solo cuando el envío es correcto
            return rx.call_script("document.getElementById('form-contacto').reset()")


# --- Formulario: cada campo tiene name para llegar al manejador en el diccionario ---
def formulario_contacto():
    return rx.form(
        rx.vstack(
            rx.input(name="nombre", placeholder="Nombre completo", width="100%"),
            rx.input(name="correo", type="email", placeholder="Correo electrónico", width="100%"),
            rx.text_area(name="mensaje", placeholder="Mensaje", width="100%", rows="5"),
            rx.button("Enviar", type="submit", color_scheme="green"),
            spacing="3",
            width="100%",
        ),
        on_submit=EstadoContacto.enviar,
        id="form-contacto",
        width="100%",
    )


# --- Página: formulario y mensaje (verde si es éxito, rojo si es error) ---
def pagina_contacto():
    return pagina(
        rx.vstack(
            rx.heading("Formulario de contacto", size="6"),
            formulario_contacto(),
            rx.cond(
                EstadoContacto.respuesta != "",
                rx.cond(
                    EstadoContacto.exito,
                    rx.callout(EstadoContacto.respuesta, color_scheme="green", width="100%"),
                    rx.callout(EstadoContacto.respuesta, color_scheme="red", width="100%"),
                ),
            ),
            spacing="3",
            style=estilo_tarjeta,
        )
    )
