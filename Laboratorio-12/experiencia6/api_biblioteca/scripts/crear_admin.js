// scripts/crear_admin.js
require('dotenv').config({ quiet: true });
const bcrypt = require('bcryptjs');
const { pool, llamar } = require('../src/db');

async function main() {
  const [nombre, email, password] = process.argv.slice(2);
  if (!nombre || !email || !password) {
    console.log('Uso: node scripts/crear_admin.js "Nombre" correo clave');
    return;
  }
  const hash = await bcrypt.hash(password, 10);
  const [{ id }] = await llamar('sp_usuario_registrar',
    [nombre, email.toLowerCase(), hash, 'admin']);
  console.log(`Administrador creado con id ${id}`);
}

main()
  .catch((e) => console.error('Error:', e.message))
  .finally(() => pool.end());
