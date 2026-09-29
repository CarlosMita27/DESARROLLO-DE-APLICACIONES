# DevLab React - Experiencia N.° 03

Proyecto React (Vite) que resuelve la Experiencia N.° 03 del Laboratorio N.° 06:
Formularios y consumo de datos.

## Cómo ejecutar

```bash
npm install
npm run dev
```

Abre en el navegador la dirección que muestre la terminal (normalmente
http://localhost:5173).

## Cómo tomar las capturas

Este ZIP ya viene con la versión FINAL de `App.jsx` (Parte 1 + Parte 2
integradas: formulario + consumo de API).

### Figura 11 — Formulario con datos ingresados (antes de enviar)
1. Escribe algo en los campos "Nombre" y "Descripción" del formulario
   (por ejemplo: "TypeScript" / "Superset de JavaScript con tipado").
2. Captura el navegador ANTES de presionar "Registrar", mostrando el
   texto ya escrito en los campos.

### Figura 12 — Nuevo elemento agregado y campos limpios
1. Presiona el botón "Registrar".
2. Captura el navegador mostrando la nueva tarjeta añadida al final de
   la lista, y los campos del formulario ahora vacíos.

### Figura 13 — Mensaje de carga de la API
1. Recarga la página completa (F5) y trata de capturar muy rápido, justo
   cuando aparece el texto "Cargando información..." (antes de que la
   lista de usuarios cargue). Si es muy rápido, puedes simular esto
   fácilmente: abre las DevTools (F12) → pestaña "Network" → activa
   "Slow 3G" o "throttling" para que la carga tome más tiempo y puedas
   capturar el mensaje con calma. Luego no olvides desactivar el
   throttling.
2. Captura el navegador mostrando "Cargando información...".

### Figura 14 — Lista de usuarios obtenida desde la API
1. Espera a que la solicitud termine (unos segundos).
2. Captura el navegador mostrando la lista de nombres de usuarios
   obtenidos desde la API (Leanne Graham, Ervin Howell, etc.).
