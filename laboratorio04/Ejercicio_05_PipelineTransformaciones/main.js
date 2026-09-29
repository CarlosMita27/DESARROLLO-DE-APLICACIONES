/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Ejercicio 5 - Pipeline de transformaciones
   ========================================================= */

function pipeline(...transformaciones) {
    return function (valorInicial) {
        return transformaciones.reduce(
            (valorActual, transformacion) => transformacion(valorActual),
            valorInicial
        );
    };
}

const duplicar = (n) => n * 2;
const sumarDiez = (n) => n + 10;
const cuadrado = (n) => n ** 2;

const operacion = pipeline(duplicar, sumarDiez, cuadrado);
console.log(operacion(5)); // 400

// Segundo pipeline con distinto orden de transformaciones
const otraOperacion = pipeline(sumarDiez, duplicar);
console.log(otraOperacion(5)); // (5 + 10) * 2 = 30
