/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Experiencia N.° 02 - De instrucciones aisladas
   a funciones reutilizables
   ========================================================= */

// Parte 1. Nuestra primera función
function calcularSubtotal(precio, cantidad) {
    return precio * cantidad;
}

console.log(calcularSubtotal(120, 3));
console.log(calcularSubtotal(80, 5));

// Parte 2. Comparando formas de definir una función
const calcularSubtotalExpresion = function (precio, cantidad) {
    return precio * cantidad;
};

const calcularSubtotalFlecha = (precio, cantidad) => precio * cantidad;

console.log(calcularSubtotalExpresion(120, 3));
console.log(calcularSubtotalFlecha(120, 3));

// Parte 3. Parámetros predeterminados
function calcularTotal(precio, cantidad = 1, descuento = 0) {
    const subtotal = precio * cantidad;
    return subtotal - (subtotal * descuento) / 100;
}

console.log(calcularTotal(100));
console.log(calcularTotal(100, 3));
console.log(calcularTotal(100, 3, 10));

// Parte 4. Parámetros rest
function sumarImportes(...importes) {
    console.log(importes);
    return importes.reduce((total, importe) => total + importe, 0);
}

console.log(sumarImportes(100, 50));
console.log(sumarImportes(100, 50, 80, 25));

// Parte 5. Funciones como argumentos
const aplicarDescuento = (precio) => precio * 0.90;
const aplicarIGV = (precio) => precio * 1.18;

function procesarPrecio(precio, operacion) {
    return operacion(precio);
}

console.log(procesarPrecio(100, aplicarDescuento));
console.log(procesarPrecio(100, aplicarIGV));

// Parte 6. calcularVenta()
function calcularVenta(precio, cantidad, descuento = 0) {
    const subtotal = precio * cantidad;
    return subtotal - (subtotal * descuento) / 100;
}

console.log(calcularVenta(50, 2));
console.log(calcularVenta(200, 1, 15));
console.log(calcularVenta(30, 10, 5));
