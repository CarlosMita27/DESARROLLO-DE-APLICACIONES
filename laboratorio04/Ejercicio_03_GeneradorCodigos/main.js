/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Ejercicio 3 - Generador de códigos únicos (closures)
   ========================================================= */

function crearGeneradorCodigo(prefijo) {
    let contador = 0;

    return function () {
        contador++;
        return `${prefijo}-${contador}`;
    };
}

const generarAlumno = crearGeneradorCodigo("ALU");
console.log(generarAlumno()); // ALU-1
console.log(generarAlumno()); // ALU-2

const generarDocente = crearGeneradorCodigo("DOC");
console.log(generarDocente()); // DOC-1
console.log(generarAlumno());  // ALU-3
console.log(generarDocente()); // DOC-2
