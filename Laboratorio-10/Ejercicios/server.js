const express = require('express');
const multer = require('multer');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const ESPECIALIDADES = ['Estadistica', 'DesarrolloWeb', 'Testing', 'BasesDeDatos', 'Redes'];
const RAIZ = path.join(__dirname, 'uploads');
ESPECIALIDADES.forEach(e => fs.mkdirSync(path.join(RAIZ, e), { recursive: true }));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const escapar = t => String(t).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const usuarios = [];

app.post('/registro', (req, res) => {
  const { nombres, apellidos, correo, clave, confirmar, nacimiento, genero, carrera } = req.body;
  const errores = [];
  if (!nombres || !apellidos) errores.push('Los nombres y apellidos son obligatorios.');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo || '')) errores.push('El correo no tiene un formato válido.');
  if (!clave || clave.length < 6) errores.push('La contraseña debe tener al menos 6 caracteres.');
  if (clave !== confirmar) errores.push('Las contraseñas no coinciden.');
  if (errores.length) {
    return res.status(400).send(`<h2>No se pudo registrar</h2><ul>${errores.map(e => `<li>${escapar(e)}</li>`).join('')}</ul><a href="/registro.html">Volver</a>`);
  }
  usuarios.push({ nombres, apellidos, correo, nacimiento, genero, carrera });
  res.redirect('/confirmacion/' + (usuarios.length - 1));
});

app.get('/confirmacion/:id', (req, res) => {
  const u = usuarios[Number(req.params.id)];
  if (!u) return res.status(404).send('Registro no encontrado.');
  res.send(`<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Registro exitoso</title><link rel="stylesheet" href="/estilos.css"></head><body><main>
    <h1>Registro exitoso</h1>
    <p>Bienvenido(a), <strong>${escapar(u.nombres)} ${escapar(u.apellidos)}</strong>. Sus datos fueron registrados.</p>
    <table>
      <tr><th>Correo</th><td>${escapar(u.correo)}</td></tr>
      <tr><th>Fecha de nacimiento</th><td>${escapar(u.nacimiento || '-')}</td></tr>
      <tr><th>Género</th><td>${escapar(u.genero || '-')}</td></tr>
      <tr><th>Carrera</th><td>${escapar(u.carrera || '-')}</td></tr>
    </table>
    <p><a href="/registro.html">Registrar otro usuario</a> | <a href="/">Inicio</a></p></main></body></html>`);
});

const almacenamiento = multer.diskStorage({
  destination: (req, file, cb) => {
    const esp = req.body.especialidad;
    if (!ESPECIALIDADES.includes(esp)) return cb(new Error('Especialidad no válida'));
    cb(null, path.join(RAIZ, esp));
  },
  filename: (req, file, cb) => cb(null, Date.now() + '_' + path.basename(file.originalname))
});
const subir = multer({ storage: almacenamiento, limits: { fileSize: 5 * 1024 * 1024 } });

app.get('/api/especialidades', (req, res) => res.json(ESPECIALIDADES));

app.post('/api/archivos', (req, res) => {
  subir.single('archivo')(req, res, err => {
    if (err) return res.status(400).json({ mensaje: err.message });
    if (!req.file) return res.status(400).json({ mensaje: 'Seleccione un archivo.' });
    res.json({ mensaje: 'Archivo guardado en ' + req.body.especialidad });
  });
});

app.get('/api/archivos', (req, res) => {
  const lista = {};
  ESPECIALIDADES.forEach(e => { lista[e] = fs.readdirSync(path.join(RAIZ, e)); });
  res.json(lista);
});

app.get('/api/archivos/:esp/:nombre', (req, res) => {
  const { esp, nombre } = req.params;
  if (!ESPECIALIDADES.includes(esp)) return res.status(404).send('No existe');
  const ruta = path.join(RAIZ, esp, path.basename(nombre));
  if (!fs.existsSync(ruta)) return res.status(404).send('No existe');
  const ext = path.extname(ruta).toLowerCase();
  if (['.txt', '.md', '.csv', '.json', '.js', '.html', '.css', '.sql', '.py'].includes(ext)) {
    res.type('text/plain; charset=utf-8').send(fs.readFileSync(ruta, 'utf8'));
  } else {
    res.sendFile(ruta);
  }
});

app.listen(PORT, () => console.log(`Servidor en http://localhost:${PORT}`));
