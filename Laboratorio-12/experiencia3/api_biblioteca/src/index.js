// src/index.js
require('dotenv').config({ quiet: true }); // carga las variables de .env en process.env
const app = require('./app');

const PUERTO = process.env.PORT || 3003;

app.listen(PUERTO, () => {
  console.log(`Servidor escuchando en http://localhost:${PUERTO}`);
});
