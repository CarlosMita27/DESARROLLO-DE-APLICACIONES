// Ejecuta las 6 experiencias del Laboratorio 12 y guarda la salida en ../evidencias
// Uso: node _ejecucion/ejecutar_todo.js   (con los servidores MySQL 3307 y 3308 en marcha)
const { espera, Registro, ejecutar, iniciar, esperarTexto, detener, path, fs } = require('./lib');

const RAIZ = path.resolve(__dirname, '..');
const EVID = path.join(RAIZ, 'evidencias');
const MYSQL = '"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe"';
const CA = path.join(RAIZ, 'experiencia4', 'api_biblioteca', 'certs', 'ca.pem');
const proyecto = (n) => path.join(RAIZ, `experiencia${n}`, 'api_biblioteca');
fs.mkdirSync(EVID, { recursive: true });

// Datos del administrador de Aiven: se leen de un archivo FUERA del proyecto (no va al ZIP)
const NUBE = Object.fromEntries(fs.readFileSync(path.resolve(RAIZ, '..', '_aiven', 'admin.env'), 'utf8')
  .split(/\r?\n/).filter((l) => /^\w+=/.test(l)).map((l) => [l.slice(0, l.indexOf('=')), l.slice(l.indexOf('=') + 1)]));

// Clientes mysql: local (3307) y nube Aiven (TLS obligatorio con verificación de la CA)
const local = (args) => `${MYSQL} --default-character-set=utf8mb4 -h 127.0.0.1 -P 3307 -u root ${args}`;
const nube = (args) => `${MYSQL} --default-character-set=utf8mb4 -h ${NUBE.NUBE_HOST} -P ${NUBE.NUBE_PORT} -u ${NUBE.NUBE_ADMIN_USER} --ssl-mode=VERIFY_IDENTITY --ssl-ca="${CA}" ${args}`;
const ENV_LOCAL = { MYSQL_PWD: 'RootLocal#2026' };
const ENV_NUBE = { MYSQL_PWD: NUBE.NUBE_ADMIN_PASSWORD };
const sql = (cliente, env, args, cwd) => {
  Object.assign(process.env, env);
  const out = ejecutar(cliente(args), cwd);
  delete process.env.MYSQL_PWD;
  return out;
};

function cmd(reg, linea, cwd, mostrar = linea) {
  reg.add(`$ ${mostrar}`);
  reg.add(ejecutar(linea, cwd).replace(/\s+$/, ''));
}
const curl = (reg, url, extra = '') =>
  cmd(reg, `curl.exe -s ${extra} -w " -> %{http_code}\\n" ${url}`, RAIZ,
      `curl -s ${extra ? extra + ' ' : ''}-w " -> %{http_code}\\n" ${url}`);

async function conServidor(reg, cwd, fn) {
  reg.add('$ npm run dev');
  const srv = iniciar('npm run dev', cwd);
  try {
    await esperarTexto(srv, 'Servidor escuchando');
    await espera(300);
    const antes = srv.salida.length;
    await fn(srv);
    return { srv, antes };
  } finally {
    reg.add(srv.salida.replace(/\x1b\[[0-9;]*m/g, '').replace(/\s+$/, '').split('\n').map((l) => '[servidor] ' + l).join('\n'));
    detener(srv);
    await espera(800);
  }
}

async function exp1() {
  const reg = new Registro();
  const cwd = proyecto(1);
  reg.add('===== EXPERIENCIA 1: PROYECTO NODE.JS, EXPRESS Y NODEMON =====');
  cmd(reg, 'node -v', cwd); cmd(reg, 'npm -v', cwd);
  cmd(reg, 'npm ls --depth=0', cwd);
  reg.add('\n--- Servidor con Express + Nodemon ---');
  const app = path.join(cwd, 'src', 'app.js');
  const original = fs.readFileSync(app, 'utf8');
  await conServidor(reg, cwd, async (srv) => {
    curl(reg, 'http://localhost:3001/');
    curl(reg, 'http://localhost:3001/api/libros');
    curl(reg, 'http://localhost:3001/api/libros/2');
    curl(reg, 'http://localhost:3001/api/libros/99');
    reg.add('\n# Se modifica el mensaje de src/app.js y se guarda -> Nodemon reinicia');
    const desde = srv.salida.length;
    fs.writeFileSync(app, original.replace('en funcionamiento', 'en funcionamiento (modificado)'));
    await esperarTexto(srv, 'Servidor escuchando', 20000, desde + 1);
    await espera(300);
    curl(reg, 'http://localhost:3001/');
    const desde2 = srv.salida.length;
    fs.writeFileSync(app, original);
    await esperarTexto(srv, 'Servidor escuchando', 20000, desde2 + 1);
    await espera(300);
    reg.add('# Se restaura el mensaje original (Nodemon reinicia de nuevo)');
    curl(reg, 'http://localhost:3001/');
  });
  fs.writeFileSync(app, original);
  reg.add('\n--- Ejemplo 12.2: servidor mínimo con el módulo http ---');
  reg.add('$ node pruebas/servidor_http.js');
  const http = iniciar('node pruebas/servidor_http.js', cwd);
  await esperarTexto(http, 'Servidor en');
  reg.add(http.salida.trim());
  curl(reg, 'http://localhost:3000/api/saludo');
  curl(reg, 'http://localhost:3000/otra');
  detener(http); await espera(500);
  reg.guardar(path.join(EVID, 'experiencia1_salida.txt'));
}

async function exp2() {
  const reg = new Registro();
  const cwd = proyecto(2);
  reg.add('===== EXPERIENCIA 2: SERVICIO RESTFUL CRUD CON EXPRESS ROUTER =====');
  await conServidor(reg, cwd, async () => {
    cmd(reg, 'node pruebas/verificar_exp2.js', cwd);
    reg.add('\n# Casos adicionales: PUT inválido, PUT/DELETE inexistente y ruta no encontrada');
    curl(reg, 'http://localhost:3002/api/libros/1', '-X PUT -H "Content-Type: application/json" -d "{\\"titulo\\":\\"\\"}"');
    curl(reg, 'http://localhost:3002/api/libros/99', '-X PUT -H "Content-Type: application/json" -d "{\\"titulo\\":\\"X\\",\\"autor\\":\\"Y\\"}"');
    curl(reg, 'http://localhost:3002/api/libros/99', '-X DELETE');
    curl(reg, 'http://localhost:3002/api/autores');
  });
  reg.guardar(path.join(EVID, 'experiencia2_salida.txt'));
}

async function exp3() {
  const reg = new Registro();
  const cwd = proyecto(3);
  reg.add('===== EXPERIENCIA 3: PERSISTENCIA CON MYSQL Y PROCEDIMIENTOS ALMACENADOS =====');
  reg.add('# Servidor MySQL 8 local (puerto 3307 en este equipo)');
  sql(local, ENV_LOCAL, '-e "DROP DATABASE IF EXISTS biblioteca"', cwd); // base limpia para la demostración
  reg.add('$ mysql -u root -p < sql/biblioteca.sql');
  reg.add(sql(local, ENV_LOCAL, '< sql/biblioteca.sql', cwd).trim() || '(script ejecutado sin errores)');
  reg.add("$ mysql> SHOW PROCEDURE STATUS WHERE Db = 'biblioteca';");
  reg.add(sql(local, ENV_LOCAL, `-t -e "SELECT ROUTINE_NAME AS procedimiento, ROUTINE_TYPE AS tipo FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA='biblioteca' ORDER BY 1"`, cwd).trim());
  cmd(reg, 'type .env', cwd, 'cat .env');
  await conServidor(reg, cwd, async () => {
    cmd(reg, 'node pruebas/verificar_exp2.js', cwd);
    reg.add('\n# Se crea un libro que queda guardado en MySQL');
    curl(reg, 'http://localhost:3003/api/libros', '-X POST -H "Content-Type: application/json" -d "{\\"titulo\\":\\"Tradiciones peruanas\\",\\"autor\\":\\"Ricardo Palma\\",\\"anio\\":1872}"');
  });
  reg.add('\n# El servidor se detuvo y se vuelve a iniciar: los datos persisten');
  await conServidor(reg, cwd, async () => { curl(reg, 'http://localhost:3003/api/libros'); });
  reg.add('\n$ mysql> CALL sp_libros_listar();');
  reg.add(sql(local, ENV_LOCAL, '-t -D biblioteca -e "CALL sp_libros_listar();"', cwd).trim());
  // Se elimina el libro de demostración para dejar el catálogo con los 2 libros iniciales
  sql(local, ENV_LOCAL, `-D biblioteca -e "DELETE FROM libros WHERE titulo='Tradiciones peruanas'"`, cwd);
  reg.guardar(path.join(EVID, 'experiencia3_salida.txt'));
}

async function exp4() {
  const reg = new Registro();
  const cwd = proyecto(4);
  reg.add('===== EXPERIENCIA 4: BASE DE DATOS MYSQL EN LA NUBE (TLS) =====');
  reg.add('# Proveedor: Aiven for MySQL (plan Developer, DigitalOcean nyc). SSL mode: REQUIRED.');
  reg.add(`# Host: ${NUBE.NUBE_HOST}  Puerto: ${NUBE.NUBE_PORT}  CA: certs/ca.pem (descargado del panel)`);
  // base y usuario limpios para la demostración
  sql(nube, ENV_NUBE, `-e "DROP DATABASE IF EXISTS biblioteca; DROP USER IF EXISTS 'biblioteca_app'@'%'"`, cwd);
  reg.add('\n# Cliente mysql con SSL verificado, usuario administrador del proveedor (avnadmin):');
  reg.add('$ mysql -h <host> -P <puerto> -u avnadmin -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=certs/ca.pem < sql/nube_base_usuario.sql');
  const base = fs.readFileSync(path.join(cwd, 'sql', 'nube_base_usuario.sql'), 'utf8')
    .split(/\r?\n/).filter((l) => l && !l.startsWith('--')).join(' ')
    .replace('ClaveGeneradaPorElProveedor', NUBE.NUBE_APP_PASSWORD);
  reg.add(sql(nube, ENV_NUBE, `-e "${base}"`, cwd).trim() || '(base biblioteca y usuario biblioteca_app creados; la clave real está en .env)');
  reg.add('$ mysql ... -D biblioteca < sql/biblioteca_nube.sql   (biblioteca.sql sin el bloque del usuario local)');
  reg.add(sql(nube, ENV_NUBE, '-D biblioteca < sql/biblioteca_nube.sql', cwd).trim() || '(tablas y procedimientos creados)');
  reg.add('\n$ mysql (nube)> SHOW PROCEDURE STATUS WHERE Db = \'biblioteca\';');
  reg.add(sql(nube, ENV_NUBE, `-t -e "SELECT ROUTINE_NAME AS procedimiento FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA='biblioteca' ORDER BY 1"`, cwd).trim());
  reg.add('\n# Validación del certificado: con una CA equivocada la conexión TLS se rechaza');
  reg.add('$ mysql -h <host> -P <puerto> -u avnadmin -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA de otro servidor>');
  const caFalsa = path.resolve(RAIZ, '..', '_mysql_lab12_v2', 'certs', 'ca.pem');
  reg.add(sql((a) => `${MYSQL} -h ${NUBE.NUBE_HOST} -P ${NUBE.NUBE_PORT} -u avnadmin --ssl-mode=VERIFY_IDENTITY --ssl-ca="${caFalsa}" ${a}`, ENV_NUBE, '-e "SELECT 1"', cwd).trim());
  cmd(reg, 'type .gitignore', cwd, 'cat .gitignore');
  cmd(reg, 'node pruebas/probar_conexion.js', cwd);
  await conServidor(reg, cwd, async () => {
    cmd(reg, 'node pruebas/verificar_exp2.js', cwd);
  });
  reg.guardar(path.join(EVID, 'experiencia4_salida.txt'));
}

async function exp5() {
  const reg = new Registro();
  const cwd = proyecto(5);
  reg.add('===== EXPERIENCIA 5: REGISTRO E INICIO DE SESIÓN CON JWT =====');
  reg.add('$ mysql (nube, TLS) < sql/usuarios.sql');
  reg.add(sql(nube, ENV_NUBE, '< sql/usuarios.sql', cwd).trim() || '(tabla usuarios y procedimientos creados)');
  cmd(reg, `node -e "console.log(require('node:crypto').randomBytes(32).toString('hex'))"`, cwd);
  reg.add('(ejemplo del comando; la clave real del proyecto está en .env como JWT_SECRET y no se muestra)');
  await conServidor(reg, cwd, async () => {
    cmd(reg, 'node pruebas/verificar_exp5.js', cwd);
    reg.add('\n# Registro con datos inválidos (password corta)');
    curl(reg, 'http://localhost:3005/api/auth/registro', '-X POST -H "Content-Type: application/json" -d "{\\"nombre\\":\\"Ana\\",\\"email\\":\\"ana@x.pe\\",\\"password\\":\\"123\\"}"');
  });
  reg.add('\n# Las contraseñas se guardan como hash bcrypt (nunca en texto plano):');
  reg.add(sql(nube, ENV_NUBE, '-t -D biblioteca -e "SELECT id, email, password_hash, rol FROM usuarios"', cwd).trim());
  reg.guardar(path.join(EVID, 'experiencia5_salida.txt'));
}

async function exp6() {
  const reg = new Registro();
  const cwd = proyecto(6);
  reg.add('===== EXPERIENCIA 6: PROTECCIÓN DE RUTAS CON MIDDLEWARE JWT Y ROLES =====');
  cmd(reg, 'node scripts/crear_admin.js "Administrador" admin@biblioteca.pe "Admin#2026"', cwd);
  await conServidor(reg, cwd, async () => {
    cmd(reg, 'node pruebas/verificar_exp6.js', cwd);
    reg.add('\n# Token expirado (firmado con exp en el pasado) y perfil sin token');
    require(path.join(cwd, 'node_modules', 'dotenv')).config({ path: path.join(cwd, '.env'), quiet: true });
    const jwt = require(path.join(cwd, 'node_modules', 'jsonwebtoken'));
    const vencido = jwt.sign({ sub: '1', rol: 'admin', exp: Math.floor(Date.now() / 1000) - 60 }, process.env.JWT_SECRET);
    curl(reg, 'http://localhost:3006/api/libros', `-X POST -H "Authorization: Bearer ${vencido}" -H "Content-Type: application/json" -d "{}"`);
    curl(reg, 'http://localhost:3006/api/auth/perfil');
  });
  reg.guardar(path.join(EVID, 'experiencia6_salida.txt'));
}

(async () => {
  const solo = process.argv[2];
  const todas = { 1: exp1, 2: exp2, 3: exp3, 4: exp4, 5: exp5, 6: exp6 };
  for (const [n, fn] of Object.entries(todas)) {
    if (solo && solo !== n) continue;
    await fn();
    console.log('');
  }
})().catch((e) => { console.error(e); process.exit(1); });
