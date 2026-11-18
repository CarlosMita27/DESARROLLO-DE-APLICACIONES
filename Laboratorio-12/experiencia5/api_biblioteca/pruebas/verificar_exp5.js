// pruebas/verificar_exp5.js
const { pedir } = require('./http');

const BASE = 'http://localhost:3005/api/auth';
const usuario = { nombre: 'Lucía Quispe', email: 'lucia@biblioteca.pe', password: 'Lectura2026' };

async function main() {
  let r = await pedir('POST', `${BASE}/registro`, usuario);
  console.log('Registro          ->', r.estado, r.datos);

  r = await pedir('POST', `${BASE}/registro`, usuario);
  console.log('Registro repetido ->', r.estado, r.datos.error);

  r = await pedir('POST', `${BASE}/login`, { email: usuario.email, password: 'otraClave1' });
  console.log('Login incorrecto  ->', r.estado, r.datos.error);

  r = await pedir('POST', `${BASE}/login`, { email: usuario.email, password: usuario.password });
  console.log('Login correcto    ->', r.estado, r.datos.tipo, r.datos.token.slice(0, 48) + '...');

  // El payload solo está codificado en Base64URL: cualquiera puede leerlo
  const [, payload] = r.datos.token.split('.');
  console.log('Payload:', JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')));
}

main().catch((e) => console.error('Error:', e.message));
