/*
    ARCHIVO:      app.js
    AUTOR:        Carlos Mita
    FECHA:        10/10/2026
    DESCRIPCIÓN:  Consume /api/inventario con fetch y muestra los resultados
                  paginados en la tabla de la interfaz.
*/
let paginaActual = 1;

// Consulta a la API con los parámetros de la cadena de consulta
async function cargarInventario() {
    const parametros = new URLSearchParams({
        filtro: document.getElementById("filtro").value,
        limite: document.getElementById("limite").value,
        pagina: paginaActual
    });
    const respuesta = await fetch(`/api/inventario?${parametros}`);
    const datos = await respuesta.json();

    // Error de validación de la API (400): se muestra el mensaje recibido
    if (!respuesta.ok) {
        document.getElementById("resumen").textContent = datos.error;
        return;
    }

    // Construcción de las filas con textContent (sin interpretar HTML)
    const { meta, resultados } = datos;
    const filas = resultados.map(equipo => {
        const fila = document.createElement("tr");
        const valores = [equipo.id, equipo.nombre, equipo.categoria, equipo.precio.toFixed(2)];
        valores.forEach(valor => {
            const celda = document.createElement("td");
            celda.textContent = valor;
            fila.appendChild(celda);
        });
        return fila;
    });
    document.getElementById("resultados").replaceChildren(...filas);

    // Resumen e indicador de paginación
    document.getElementById("resumen").textContent =
        `${meta.total_coincidencias} coincidencias · límite aplicado: ${meta.limite_aplicado}`;
    document.getElementById("indicador-pagina").textContent =
        `Página ${meta.pagina} de ${Math.max(meta.total_paginas, 1)}`;
    document.getElementById("anterior").disabled = meta.pagina <= 1;
    document.getElementById("siguiente").disabled = meta.pagina >= meta.total_paginas;
}

// Eventos: nueva búsqueda y navegación entre páginas
document.getElementById("formulario-busqueda").addEventListener("submit", evento => {
    evento.preventDefault();
    paginaActual = 1;
    cargarInventario();
});
document.getElementById("anterior").addEventListener("click", () => {
    paginaActual--;
    cargarInventario();
});
document.getElementById("siguiente").addEventListener("click", () => {
    paginaActual++;
    cargarInventario();
});

cargarInventario();
