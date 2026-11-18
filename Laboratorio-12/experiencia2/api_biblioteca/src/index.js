// src/index.js
const app = require('./app');

const PUERTO = process.env.PORT || 3002;

app.listen(PUERTO, () => {
  console.log(`Servidor escuchando en http://localhost:${PUERTO}`);
});
