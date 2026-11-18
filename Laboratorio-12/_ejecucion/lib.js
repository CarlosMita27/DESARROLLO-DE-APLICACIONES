// Utilidades para ejecutar las experiencias y capturar la salida (evidencias)
const { spawn, execSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

const espera = (ms) => new Promise((r) => setTimeout(r, ms));

class Registro {
  constructor() { this.lineas = []; }
  add(t) { const s = String(t); this.lineas.push(s); process.stdout.write(s.endsWith('\n') ? s : s + '\n'); }
  guardar(archivo) { fs.writeFileSync(archivo, this.lineas.join('\n').replace(/\n+$/, '') + '\n', 'utf8'); }
}

// Ejecuta un comando y devuelve su salida combinada (stdout + stderr)
function ejecutar(cmd, cwd) {
  try {
    return execSync(cmd, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], shell: true });
  } catch (e) {
    return (e.stdout || '') + (e.stderr || '');
  }
}

// Inicia un proceso de larga duración (servidor) y acumula su salida
function iniciar(cmd, cwd, env = {}) {
  const hijo = spawn(cmd, { cwd, shell: true, env: { ...process.env, FORCE_COLOR: '0', ...env } });
  hijo.salida = '';
  hijo.stdout.on('data', (d) => { hijo.salida += d; });
  hijo.stderr.on('data', (d) => { hijo.salida += d; });
  return hijo;
}

async function esperarTexto(hijo, texto, ms = 20000, desde = 0) {
  const fin = Date.now() + ms;
  while (Date.now() < fin) {
    if (hijo.salida.indexOf(texto, desde) !== -1) return true;
    await espera(200);
  }
  throw new Error(`No apareció "${texto}" en la salida:\n${hijo.salida}`);
}

function detener(hijo) {
  try { execSync(`taskkill /F /T /PID ${hijo.pid}`, { stdio: 'ignore' }); } catch {}
}

module.exports = { espera, Registro, ejecutar, iniciar, esperarTexto, detener, path, fs };
