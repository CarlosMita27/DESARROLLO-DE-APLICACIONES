/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Ejercicio 2 - Análisis de calificaciones
   ========================================================= */

const estudiantes = [
    { nombre: "Andrea", nota: 17 },
    { nombre: "Carlos", nota: 11 },
    { nombre: "Lucía", nota: 19 },
    { nombre: "Mateo", nota: 8 },
    { nombre: "Valeria", nota: 14 }
];

// 1. Nombres de los estudiantes
const nombres = estudiantes.map((estudiante) => estudiante.nombre);
console.log("Nombres:", nombres);

// 2. Estudiantes con nota >= 13
const aprobadosMinimo13 = estudiantes.filter((estudiante) => estudiante.nota >= 13);
console.log("Nota mayor o igual a 13:", aprobadosMinimo13);

// 3. Buscar a "Lucía"
const lucia = estudiantes.find((estudiante) => estudiante.nombre === "Lucía");
console.log("Estudiante encontrado:", lucia);

// 4. Promedio general
const promedio = estudiantes.reduce(
    (total, estudiante) => total + estudiante.nota,
    0
) / estudiantes.length;
console.log("Promedio general:", promedio);

// 5. Cantidad de desaprobados (nota < 11, criterio UCSM)
const desaprobados = estudiantes.filter((estudiante) => estudiante.nota < 11);
console.log("Cantidad de desaprobados:", desaprobados.length);

// 7. Nuevo array con propiedad "estado"
const estudiantesConEstado = estudiantes.map((estudiante) => ({
    ...estudiante,
    estado: estudiante.nota >= 11 ? "Aprobado" : "Desaprobado"
}));
console.log("Estudiantes con estado:", estudiantesConEstado);
