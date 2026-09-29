/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Ejercicio 6 - Registro de participantes
   ========================================================= */

function registrarParticipante(nombre, edad, correo, tipo = "general") {
    if (!nombre || nombre.trim() === "") {
        throw new Error("El nombre no puede estar vacío");
    }

    edad = Number(edad);
    if (Number.isNaN(edad) || edad < 18) {
        throw new Error("La edad debe ser numérica y mayor o igual a 18");
    }

    if (!correo || correo.trim() === "") {
        throw new Error("El correo no puede estar vacío");
    }

    if (tipo !== "general" && tipo !== "estudiante") {
        throw new Error("El tipo debe ser 'general' o 'estudiante'");
    }

    const costo = tipo === "estudiante" ? 30 : 50;

    return {
        nombre: nombre,
        edad: edad,
        correo: correo,
        tipo: tipo,
        costo: costo
    };
}

const participantes = [];

const datosPrueba = [
    ["Andrea Flores", 22, "andrea@correo.com", "estudiante"],
    ["Carlos Mita", 21, "carlos@correo.com", "estudiante"],
    ["José Lima", 25, "jose@correo.com", "general"],
    ["André Lazo", 23, "andre@correo.com", "general"],
    ["Valeria Rojas", 19, "valeria@correo.com", "estudiante"]
];

datosPrueba.forEach(([nombre, edad, correo, tipo]) => {
    try {
        const participante = registrarParticipante(nombre, edad, correo, tipo);
        participantes.push(participante);
    } catch (error) {
        console.error("Error al registrar:", error.message);
    }
});

console.log("Todos los participantes:", participantes);

// 3. Solo participantes de tipo estudiante
const soloEstudiantes = participantes.filter(
    (participante) => participante.tipo === "estudiante"
);
console.log("Estudiantes:", soloEstudiantes);

// 4. Nombres mediante map()
const nombresParticipantes = participantes.map((participante) => participante.nombre);
console.log("Nombres:", nombresParticipantes);

// 5. Monto total recaudado mediante reduce()
const totalRecaudado = participantes.reduce(
    (total, participante) => total + participante.costo,
    0
);
console.log("Total recaudado:", totalRecaudado);

// 6. Buscar participante por correo
const participanteBuscado = participantes.find(
    (participante) => participante.correo === "jose@correo.com"
);
console.log("Participante encontrado:", participanteBuscado);
