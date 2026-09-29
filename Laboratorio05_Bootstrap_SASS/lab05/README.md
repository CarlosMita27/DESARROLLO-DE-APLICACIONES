# Laboratorio N.° 05 — Bootstrap y SASS

**Curso:** Desarrollo de Aplicaciones
**Escuela Profesional de Ingeniería de Sistemas — UCSM**

## Integrantes

| Código | Apellidos y Nombres |
|---|---|
| 2024001399 | Lazo Villavicencio, André Fabricio |
| 2024001337 | Lima Filinich, Jose Francisco |
| 2024001462 | Mita Mamani, Carlos Alberto |
| 2024004642 | Yepez Corimanya, Carlos Augusto |

## Estructura del repositorio

```
lab05/
├── Experiencia01/   → Grid System (Bootstrap)
├── Experiencia02/   → Componentes y utilitarios (Bootstrap)
├── Experiencia03/   → Navbar colapsable y Modal (Bootstrap)
├── Experiencia04/   → Variables y Nesting (Sass)
├── Experiencia05/   → Mixins y @extend (Sass)
├── Experiencia06/   → Mapas y bucles @each/@for (Sass)
├── Ejercicio01_Dashboard/       → Panel administrativo responsivo (Bootstrap)
└── Ejercicio02_MicroFramework/  → Micro-framework CSS modular (Sass)
```

Cada carpeta de experiencia incluye el archivo `.html` o `.scss` resuelto, y en el caso de las experiencias de Sass (04, 05 y 06) también el archivo `.css` ya compilado junto con un HTML de prueba para visualizar el resultado en el navegador.

## Cómo ejecutar

- Los archivos `.html` pueden abrirse directamente en el navegador o mediante la extensión **Live Server** de VS Code.
- Los archivos `.scss` requieren la extensión **Live Sass Compiler** para generar su respectivo `.css`.
- El Ejercicio 02 utiliza una arquitectura de archivos parciales: compilar `scss/main.scss` genera `css/main.css`, el cual es consumido por `index.html`.
