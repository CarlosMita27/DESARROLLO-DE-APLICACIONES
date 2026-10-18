import reflex as rx

config = rx.Config(
    app_name="practica_reflex",
    plugins=[
        rx.plugins.RadixThemesPlugin(theme=rx.theme(accent_color="green")),
        rx.plugins.SitemapPlugin(),
    ],
)
