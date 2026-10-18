# =============================================================================
# ARCHIVO:     practica_reflex/practica_reflex.py
# AUTOR:       Carlos Mita
# FECHA:       17/10/2026
# DESCRIPCIÓN: Crea la aplicación Reflex y registra las páginas de las experiencias y ejercicios.
# =============================================================================
import reflex as rx

from .ejercicio_1 import pagina_ejercicio1
from .ejercicio_2 import pagina_ejercicio2
from .ejercicio_3 import pagina_ejercicio3
from .ejercicio_4 import EstadoDirectorio, pagina_ejercicio4
from .experiencia_1 import index
from .experiencia_2 import pagina_tareas
from .experiencia_3 import pagina_contacto
from .experiencia_4 import pagina_usuarios

app = rx.App()
app.add_page(index, route="/", title="Práctica Reflex")
app.add_page(pagina_tareas, route="/tareas", title="Tareas")
app.add_page(pagina_contacto, route="/contacto", title="Contacto")
app.add_page(pagina_usuarios, route="/usuarios", title="Usuarios")
app.add_page(pagina_ejercicio1, route="/ejercicio1", title="Ejercicio 1: Kanban")
app.add_page(pagina_ejercicio2, route="/ejercicio2", title="Ejercicio 2: Indicadores")
app.add_page(pagina_ejercicio3, route="/ejercicio3", title="Ejercicio 3: Solicitudes")
app.add_page(
    pagina_ejercicio4,
    route="/ejercicio4",
    title="Ejercicio 4: Directorio",
    on_load=EstadoDirectorio.cargar_usuarios,
)
