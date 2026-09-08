/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Ejercicio 4 - Sistema de reservas de cine
   ========================================================= */

const funciones = [
    { id: 1, pelicula: "Interstellar", sala: 1, precio: 18, disponibles: 12 },
    { id: 2, pelicula: "Dune", sala: 2, precio: 20, disponibles: 5 },
    { id: 3, pelicula: "Avengers", sala: 3, precio: 16, disponibles: 0 },
    { id: 4, pelicula: "Inception", sala: 1, precio: 18, disponibles: 8 }
];

function buscarFuncion(id) {
    const funcion = funciones.find((funcionItem) => funcionItem.id === id);

    if (!funcion) {
        throw new Error(`No existe una función con el ID ${id}`);
    }

    return funcion;
}

function funcionesDisponibles() {
    return funciones.filter((funcionItem) => funcionItem.disponibles > 0);
}

function comprarEntradas(id, cantidad) {
    const funcion = buscarFuncion(id);

    if (cantidad <= 0) {
        throw new Error("La cantidad debe ser mayor que cero");
    }

    if (cantidad > funcion.disponibles) {
        throw new Error("No hay suficientes entradas disponibles");
    }

    funcion.disponibles -= cantidad;

    return {
        pelicula: funcion.pelicula,
        cantidad: cantidad,
        total: funcion.precio * cantidad
    };
}

// Pruebas mínimas

// Compra válida
try {
    console.log(comprarEntradas(1, 3));
} catch (error) {
    console.error(error.message);
}

// Compra superior a las entradas disponibles
try {
    console.log(comprarEntradas(2, 10));
} catch (error) {
    console.error(error.message);
}

// Búsqueda con ID inexistente
try {
    console.log(buscarFuncion(99));
} catch (error) {
    console.error(error.message);
}

console.log("Funciones disponibles:", funcionesDisponibles());
