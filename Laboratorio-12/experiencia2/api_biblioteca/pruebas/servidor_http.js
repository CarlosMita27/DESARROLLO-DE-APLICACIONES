// servidor_http.js — servidor REST mínimo solo con el módulo http de Node.js (punto 12.2)
const http = require('node:http');

const servidor = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/api/saludo') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    return res.end(JSON.stringify({ mensaje: 'Hola desde Node.js' }));
  }
  res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify({ error: 'Ruta no encontrada' }));
});

const PUERTO = process.env.PORT || 3000;
servidor.listen(PUERTO, () => console.log(`Servidor en http://localhost:${PUERTO}`));
