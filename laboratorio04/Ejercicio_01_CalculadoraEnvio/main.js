/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Ejercicio 1 - Calculadora de costo de envío
   ========================================================= */

function calcularEnvio(peso, tipo = "normal") {
    peso = Number(peso);

    if (Number.isNaN(peso) || peso <= 0) {
        throw new Error("El peso ingresado no es válido");
    }

    let costoBase;

    if (peso <= 2) {
        costoBase = 8.00;
    } else if (peso <= 5) {
        costoBase = 12.00;
    } else {
        costoBase = 18.00;
    }

    let costoFinal = costoBase;

    if (tipo === "express") {
        costoFinal = costoBase * 1.40;
    }

    return {
        peso: peso,
        tipo: tipo,
        costoBase: costoBase,
        costoFinal: costoFinal
    };
}

// Pruebas
try {
    console.log(calcularEnvio(1.5)); // envío normal menor de 2 kg
} catch (error) {
    console.error(error.message);
}

try {
    console.log(calcularEnvio(4, "express")); // envío express
} catch (error) {
    console.error(error.message);
}

try {
    console.log(calcularEnvio(-3)); // peso inválido
} catch (error) {
    console.error(error.message);
}
