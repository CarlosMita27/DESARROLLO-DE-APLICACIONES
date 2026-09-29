/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Experiencia N.° 03 - Modelando y procesando
   información con objetos y arrays
   ========================================================= */

// Parte 1. Representando un producto
const producto = {
    id: 1,
    nombre: "Teclado",
    precio: 120,
    stock: 8
};

console.log(producto.nombre);
console.log(producto.precio);

producto.categoria = "Periféricos";
producto.stock = 10;

console.log(producto);

producto.calcularValorStock = function () {
    return this.precio * this.stock;
};

console.log(producto.calcularValorStock());

// Parte 2. Creando un inventario
const productos = [
    { id: 1, nombre: "Teclado", precio: 120, stock: 8 },
    { id: 2, nombre: "Mouse", precio: 70, stock: 15 },
    { id: 3, nombre: "Monitor", precio: 850, stock: 4 },
    { id: 4, nombre: "Webcam", precio: 160, stock: 0 }
];

console.log("Cantidad de elementos:", productos.length);
console.log("Precio del Monitor:", productos[2].precio);

// Parte 3. forEach()
productos.forEach((productoItem) => {
    console.log(
        `${productoItem.nombre} | S/ ${productoItem.precio} | Stock: ${productoItem.stock}`
    );
});

// Parte 4. map()
const nombres = productos.map((productoItem) => productoItem.nombre);
console.log(nombres);

const preciosIncrementados = productos.map(
    (productoItem) => productoItem.precio * 1.10
);
console.log(preciosIncrementados);

// Parte 5. filter()
const bajoStock = productos.filter((productoItem) => productoItem.stock < 10);
console.log(bajoStock);

const conStockDisponible = productos.filter((productoItem) => productoItem.stock > 0);
console.log(conStockDisponible);

// Parte 6. find()
const encontrado = productos.find((productoItem) => productoItem.id === 3);
console.log(encontrado);

const noEncontrado = productos.find((productoItem) => productoItem.id === 15);
console.log(noEncontrado); // undefined

// Parte 7. reduce()
const totalInventario = productos.reduce(
    (total, productoItem) => total + productoItem.precio * productoItem.stock,
    0
);
console.log("Valor total del inventario:", totalInventario);

// Parte 8. Practica
productos.push(
    { id: 5, nombre: "Parlante", precio: 90, stock: 12 },
    { id: 6, nombre: "Micrófono", precio: 200, stock: 6 }
);

const mayoresA150 = productos.filter((productoItem) => productoItem.precio > 150);
console.log(mayoresA150);

const todosLosNombres = productos.map((productoItem) => productoItem.nombre);
console.log(todosLosNombres);

const productoPorId = productos.find((productoItem) => productoItem.id === 6);
console.log(productoPorId);

const totalInventarioActualizado = productos.reduce(
    (total, productoItem) => total + productoItem.precio * productoItem.stock,
    0
);
console.log("Valor total actualizado del inventario:", totalInventarioActualizado);
