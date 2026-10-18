# =============================================================================
# ARCHIVO:     practica_reflex/ejercicio_4.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Ejercicio 4: directorio de usuarios con consulta a API (HTTPX) y búsqueda dinámica.
# =============================================================================
import httpx
import reflex as rx

from .comunes import COLOR_PRIMARIO, estilo_tarjeta, pagina

URL_API = "https://jsonplaceholder.typicode.com/users"


class EstadoDirectorio(rx.State):
    usuarios: list[dict[str, str]] = []
    busqueda: str = ""
    cargando: bool = False
    error: str = ""

    @rx.var
    def usuarios_filtrados(self) -> list[dict[str, str]]:
        texto = self.busqueda.strip().lower()
        return [u for u in self.usuarios if u["nombre"].lower().find(texto) != -1]

    @rx.event
    def actualizar_busqueda(self, valor: str):
        self.busqueda = valor

    @rx.event
    async def cargar_usuarios(self):
        self.cargando = True
        self.error = ""
        yield
        try:
            async with httpx.AsyncClient(timeout=10) as cliente:
                respuesta = await cliente.get(URL_API)
                respuesta.raise_for_status()
                datos = respuesta.json()
            self.usuarios = [
                {
                    "nombre": u["name"],
                    "usuario": u["username"],
                    "correo": u["email"],
                    "ciudad": u["address"]["city"],
                    "empresa": u["company"]["name"],
                }
                for u in datos
            ]
        except (httpx.HTTPError, KeyError, ValueError):
            self.usuarios = []
            self.error = "No fue posible obtener los datos de la API."
        finally:
            self.cargando = False


def tarjeta_directorio(usuario: rx.Var[dict[str, str]]):
    return rx.box(
        rx.heading(usuario["nombre"], size="4", color=COLOR_PRIMARIO),
        rx.text("Usuario: ", usuario["usuario"]),
        rx.text("Correo: ", usuario["correo"]),
        rx.text("Ciudad: ", usuario["ciudad"]),
        rx.text("Empresa: ", usuario["empresa"]),
        style=estilo_tarjeta,
        background_color="#F5F5F5",
    )


def resultados_directorio():
    return rx.cond(
        EstadoDirectorio.cargando,
        rx.text("Cargando usuarios..."),
        rx.cond(
            EstadoDirectorio.error != "",
            rx.callout(EstadoDirectorio.error, color_scheme="red", width="100%"),
            rx.cond(
                EstadoDirectorio.usuarios_filtrados.length() == 0,
                rx.callout(
                    "No se encontraron usuarios que coincidan con la búsqueda.",
                    color_scheme="orange",
                    width="100%",
                ),
                rx.vstack(
                    rx.foreach(EstadoDirectorio.usuarios_filtrados, tarjeta_directorio),
                    spacing="2",
                    width="100%",
                ),
            ),
        ),
    )


def directorio_con_busqueda():
    return rx.vstack(
        rx.heading("Directorio de usuarios", size="6"),
        rx.hstack(
            rx.input(
                placeholder="Buscar por nombre",
                value=EstadoDirectorio.busqueda,
                on_change=EstadoDirectorio.actualizar_busqueda,
                width="100%",
            ),
            rx.button(
                "Actualizar",
                on_click=EstadoDirectorio.cargar_usuarios,
                loading=EstadoDirectorio.cargando,
                color_scheme="green",
            ),
            width="100%",
        ),
        resultados_directorio(),
        spacing="3",
        width="100%",
    )


def pagina_ejercicio4():
    return pagina(directorio_con_busqueda())
