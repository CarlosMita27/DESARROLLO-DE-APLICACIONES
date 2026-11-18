// pruebas/verificar_exp6.js
const { pedir } = require('./http');

const API = 'http://localhost:3006/api';
const nuevo = { titulo: 'El zorro de arriba y el zorro de abajo',
                autor: 'José María Arguedas', anio: 1971 };

async function iniciarSesion(email, password) {
  const r = await pedir('POST', `${API}/auth/login`, { email, password });
  return r.datos.token;
}

async function main() {
  let r = await pedir('GET', `${API}/libros`);
  console.log('GET público         ->', r.estado, r.datos.length, 'libros');

  r = await pedir('POST', `${API}/libros`, nuevo);
  console.log('POST sin token      ->', r.estado, r.datos.error);

  r = await pedir('POST', `${API}/libros`, nuevo, 'abc.def.ghi');
  console.log('POST token falso    ->', r.estado, r.datos.error);

  const tokenLector = await iniciarSesion('lucia@biblioteca.pe', 'Lectura2026');
  r = await pedir('POST', `${API}/libros`, nuevo, tokenLector);
  console.log('POST como lector    ->', r.estado, r.datos.error);

  const tokenAdmin = await iniciarSesion('admin@biblioteca.pe', 'Admin#2026');
  r = await pedir('POST', `${API}/libros`, nuevo, tokenAdmin);
  const id = r.datos.id;
  console.log('POST como admin     ->', r.estado, 'id =', id);

  r = await pedir('DELETE', `${API}/libros/${id}`, null, tokenAdmin);
  console.log('DELETE como admin   ->', r.estado);

  r = await pedir('GET', `${API}/auth/perfil`, null, tokenLector);
  console.log('Perfil del lector   ->', r.estado, r.datos.nombre, '-', r.datos.rol);
}

main().catch((e) => console.error('Error:', e.message));
