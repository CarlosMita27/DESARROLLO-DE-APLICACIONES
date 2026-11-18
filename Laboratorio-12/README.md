# Laboratorio N° 12: Servicios REST con Node.js y JWT

Caso de estudio: **Biblioteca Digital**, una API REST hecha con Node.js, Express, MySQL y JWT.

Cada carpeta `experienciaN/api_biblioteca` contiene el proyecto **completo** tal como queda al terminar esa experiencia, porque cada experiencia parte del proyecto de la anterior.

| Carpeta | Experiencia | Qué se agrega |
|---|---|---|
| `experiencia1` | Proyecto Node.js, Express y Nodemon | `package.json`, `nodemon.json`, `src/app.js`, `src/index.js`, rutas GET en memoria, `pruebas/servidor_http.js` (ejemplo del punto 12.2) |
| `experiencia2` | CRUD con Express Router | `src/controllers`, `src/routes`, manejadores 404 y de errores, `pruebas/http.js`, `pruebas/verificar_exp2.js` |
| `experiencia3` | MySQL y procedimientos almacenados | `sql/biblioteca.sql`, `.env`, `src/db.js` (pool `mysql2/promise` + `CALL ?`), controlador async |
| `experiencia4` | MySQL en la nube con TLS | `src/db.js` con `ssl { ca, rejectUnauthorized: true }`, `certs/ca.pem`, `sql/nube_base_usuario.sql`, `pruebas/probar_conexion.js` |
| `experiencia5` | Registro e inicio de sesión con JWT | `sql/usuarios.sql`, `auth.controller.js` (bcrypt y `jwt.sign`), `auth.routes.js`, `pruebas/verificar_exp5.js` |
| `experiencia6` | Middleware JWT y roles | `src/middlewares/auth.js` (`verificarToken` y `permitirRoles`), rutas protegidas, `/api/auth/perfil`, `scripts/crear_admin.js`, `pruebas/verificar_exp6.js` |

**Evidencias:** en `evidencias/` está la salida real de cada ejecución (`experienciaN_salida.txt`). Para leerlas todas juntas, abre `evidencias/index.html`.

## Entorno donde se ejecutó

- Node.js v24.20.0, npm 11.19.0, Express 5.3.0, Nodemon 3.1.14, mysql2 3.x, jsonwebtoken y bcryptjs.
- **MySQL local** (Experiencia 3): MySQL Server 8.0.46 en `127.0.0.1:3307`, que hace el papel del MySQL local de la guía.
- **Nube real: Aiven for MySQL** (Experiencias 4 a 6). Plan Developer con créditos de prueba, MySQL 8.4 en DigitalOcean (nyc), con SSL mode REQUIRED. Del panel se copiaron el host, el puerto, el usuario `avnadmin` y la contraseña, y se descargó el certificado CA a `certs/ca.pem`. La API se conecta con el usuario `biblioteca_app`, que solo tiene permisos SELECT, INSERT, UPDATE, DELETE y EXECUTE, y valida el certificado con `rejectUnauthorized: true`.
  - Para pasar de MySQL local a la nube **solo se cambió el `.env`** y se agregó `certs/ca.pem`. El código de la API no cambió.

## Puertos

Cada experiencia usa su propio puerto, así que las 6 APIs pueden correr a la vez:

| Exp. | API |
|---|---|
| 1 | http://localhost:3001/api/libros |
| 2 | http://localhost:3002/api/libros |
| 3 | http://localhost:3003/api/libros |
| 4 | http://localhost:3004/api/libros |
| 5 | http://localhost:3005/api/libros (y /api/auth) |
| 6 | http://localhost:3006/api/libros (y /api/auth) |

El ejemplo `pruebas/servidor_http.js` del punto 12.2 usa el puerto 3000.

**Para levantar todo de una vez:** haz doble clic en `abrir_experiencias.bat`. Se abre Windows Terminal con una pestaña por experiencia: a la izquierda corre el servidor (`npm run dev`) y a la derecha están las pruebas que hay que ejecutar.

## Cómo ejecutarlo de nuevo

1. Para la Experiencia 3, inicia el MySQL local con `entorno_mysql/iniciar_mysql_lab12.bat`. Las experiencias 4 a 6 usan Aiven, así que el servicio tiene que estar encendido en console.aiven.io.
2. Instala las dependencias en cada proyecto:

   ```bash
   cd experiencia6/api_biblioteca
   npm install
   ```

3. Copia `.env.example` como `.env` y completa tus datos. El ZIP no incluye `.env` porque está en `.gitignore`.
4. Levanta el servidor con `npm run dev` y, en otra terminal, ejecuta `node pruebas/verificar_exp6.js` (o el script que corresponda a la experiencia).
5. Para repetir automáticamente las 6 experiencias y regenerar las evidencias:

   ```bash
   node _ejecucion/ejecutar_todo.js
   node _ejecucion/generar_informe.js
   ```

> En Windows PowerShell, escribe `curl.exe` en lugar de `curl` para no llamar al alias de Invoke-WebRequest.
