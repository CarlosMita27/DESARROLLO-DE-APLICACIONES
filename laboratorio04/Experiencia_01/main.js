/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Experiencia N.° 01 - Primer contacto con JavaScript
   ========================================================= */

// Parte 2. Comparando formas de incorporar JavaScript
console.log("JavaScript desde un archivo externo");

// Parte 3. Variables, constantes y tipos
const nombreProducto = "Teclado mecánico";
let precio = 180;
let stock = 5;
const disponible = true;

console.log(nombreProducto);
console.log(precio);
console.log(stock);
console.log(disponible);

console.log(typeof nombreProducto);
console.log(typeof precio);
console.log(typeof stock);
console.log(typeof disponible);

precio = "180";
console.log(typeof precio);

// Parte 4. const, let y scope
if (stock > 0) {
    const mensaje = "Producto disponible";
    let unidades = stock;
    console.log(mensaje);
    console.log(unidades);
}
// console.log(mensaje); // ReferenceError: mensaje no existe fuera del bloque

// Parte 5. Explorando el hoisting
console.log(cantidad);
var cantidad = 10;

// console.log(descuento);
// let descuento = 20; // ReferenceError

// Parte 6. Nuevas variables
const clienteNombre = "Andrea";
const cantidadProductos = 3;
const precioUnitario = 120;
const importe = cantidadProductos * precioUnitario;

console.log("Cliente:", clienteNombre);
console.log("Cantidad:", cantidadProductos);
console.log("Precio unitario:", precioUnitario);
console.log("Importe:", importe);
