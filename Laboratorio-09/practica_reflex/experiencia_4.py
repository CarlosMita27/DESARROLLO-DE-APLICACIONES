# =============================================================================
# ARCHIVO:     practica_reflex/experiencia_4.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Experiencia 4: consumo de la API JSONPlaceholder con HTTPX (EstadoUsuarios).
# =============================================================================
import httpx
import reflex as rx

from .comunes import estilo_tarjeta, pagina

URL_USUARIOS = "https://jsonplaceholder.typicode.com/users"


# --- Estado: usuarios obtenidos, indicador de carga y mensaje de error ---
class EstadoUsuarios(rx.State):
    usuarios: list[dict[str, str]] = []
    cargando: bool = False
    error: str = ""

    @rx.event
    async def cargar_usuarios(self):
        self.cargando = True
        self.error = ""
        self.usuarios = []
        yield  # envía de inmediato el estado "cargando" a la interfaz
        try:
            async with httpx.AsyncClient(timeout=10) as cliente:
                respuesta = await cliente.get(URL_USUARIOS)  # no bloquea el servidor
                respuesta.raise_for_status()  # lanza excepción si el código es 4xx/5xx
                datos = respuesta.json()
            # Se conservan solo los campos necesarios, en diccionarios simples
            self.usuarios = [
                {
                    "name": u["name"],
                    "username": u["username"],
                    "email": u["email"],
                    "empresa": u["company"]["name"],
                }
                for u in datos
            ]
        except (httpx.HTTPError, KeyError, ValueError):
            self.error = "No fue posible obtener los datos de la API."
        finally:
            self.cargando = False  # se ejecuta siempre, con éxito o con error


# --- Componente reutilizable: tarjeta de un usuario ---
def tarjeta_usuario(usuario: rx.Var[dict[str, str]]):
    return rx.box(
        rx.heading(usuario["name"], size="4"),
        rx.text("Usuario: ", usuario["username"]),
        rx.text("Correo: ", usuario["email"]),
        rx.text("Empresa: ", usuario["empresa"]),
        style=estilo_tarjeta,
        background_color="#F5F5F5",
    )


# --- Directorio: botón, indicador de carga, error o lista de tarjetas ---
def directorio_usuarios():
    return rx.vstack(
        rx.heading("Directorio de usuarios", size="6"),
        rx.button(
            "Cargar usuarios",
            on_click=EstadoUsuarios.cargar_usuarios,
            loading=EstadoUsuarios.cargando,
            color_scheme="green",
        ),
        rx.cond(
            EstadoUsuarios.cargando,
            rx.text("Cargando usuarios..."),
            rx.cond(
                EstadoUsuarios.error != "",
                rx.callout(EstadoUsuarios.error, color_scheme="red", width="100%"),
                rx.vstack(
                    rx.foreach(EstadoUsuarios.usuarios, tarjeta_usuario),
                    spacing="2",
                    width="100%",
                ),
            ),
        ),
        spacing="3",
        width="100%",
    )


def pagina_usuarios():
    return pagina(directorio_usuarios())
