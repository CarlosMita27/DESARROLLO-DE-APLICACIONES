/* =========================================================
   ARCHIVO: main.js
   AUTOR: Carlos Mita
   DESCRIPCIÓN: Experiencia N.° 04 - Validación y manejo
   de errores
   ========================================================= */

// Parte 1. El problema
function calcularVentaV1(precio, cantidad) {
    return precio * cantidad;
}

console.log(calcularVentaV1(100, 3));
console.log(calcularVentaV1("abc", 3)); // NaN

// Parte 2. Conversión y validación
function calcularVentaV2(precio, cantidad) {
    precio = Number(precio);
    cantidad = Number(cantidad);

    if (precio <= 0 || cantidad <= 0) {
        return "Datos no válidos";
    }

    return precio * cantidad;
}

console.log(calcularVentaV2("100", "3"));
console.log(calcularVentaV2(-20, 3));
console.log(calcularVentaV2(100, 0));

// Parte 3. Detectando NaN
function calcularVentaV3(precio, cantidad) {
    precio = Number(precio);
    cantidad = Number(cantidad);

    if (Number.isNaN(precio) || Number.isNaN(cantidad)) {
        return "Debe ingresar valores numéricos";
    }

    if (precio <= 0 || cantidad <= 0) {
        return "Datos no válidos";
    }

    return precio * cantidad;
}

console.log(calcularVentaV3("abc", 3));

// Parte 4. Lanzando una excepción
function calcularVenta(precio, cantidad) {
    precio = Number(precio);
    cantidad = Number(cantidad);

    if (Number.isNaN(precio) || Number.isNaN(cantidad)) {
        throw new Error("Precio y cantidad deben ser numéricos");
    }

    if (precio <= 0 || cantidad <= 0) {
        throw new Error("Los valores deben ser mayores que cero");
    }

    return precio * cantidad;
}

// Parte 5. try...catch
try {
    const total = calcularVenta("abc", 3);
    console.log(total);
} catch (error) {
    console.error("No fue posible calcular la venta:", error.message);
}

try {
    const total = calcularVenta(100, 3);
    console.log(total);
} catch (error) {
    console.error("No fue posible calcular la venta:", error.message);
}

// Parte 6. finally
try {
    const total = calcularVenta(100, 3);
    console.log(total);
} catch (error) {
    console.error("No fue posible calcular la venta:", error.message);
} finally {
    console.log("Proceso de venta finalizado");
}

try {
    const total = calcularVenta("abc", 3);
    console.log(total);
} catch (error) {
    console.error("No fue posible calcular la venta:", error.message);
} finally {
    console.log("Proceso de venta finalizado");
}

// Parte 7. Crea tu propia excepción
function registrarProducto(nombre, precio, stock) {
    if (!nombre || nombre.trim() === "") {
        throw new Error("El nombre no puede estar vacío");
    }

    precio = Number(precio);
    if (Number.isNaN(precio) || precio <= 0) {
        throw new Error("El precio debe ser numérico y mayor que cero");
    }

    stock = Number(stock);
    if (Number.isNaN(stock) || stock < 0) {
        throw new Error("El stock debe ser numérico y no puede ser negativo");
    }

    return {
        nombre: nombre,
        precio: precio,
        stock: stock
    };
}

try {
    console.log(registrarProducto("Audífonos", 90, 10));
} catch (error) {
    console.error(error.message);
}

try {
    console.log(registrarProducto("Audífonos", -90, 10));
} catch (error) {
    console.error(error.message);
}

try {
    console.log(registrarProducto("Audífonos", 90, -5));
} catch (error) {
    console.error(error.message);
}
