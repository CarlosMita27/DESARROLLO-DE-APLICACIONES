// Genera evidencias/index.html: por cada experiencia, su código (archivos clave) y la salida real de la ejecución
const fs = require('node:fs');
const path = require('node:path');

const RAIZ = path.resolve(__dirname, '..');
const EVID = path.join(RAIZ, 'evidencias');

const experiencias = [
  { t: 'Proyecto Node.js, Express y Nodemon',
    d: 'Se crea api_biblioteca con Express y Nodemon y se publican las primeras rutas GET con los libros en memoria.',
    f: ['package.json', 'nodemon.json', 'src/app.js', 'src/index.js', 'pruebas/servidor_http.js'] },
  { t: 'Servicio RESTful CRUD con Express Router',
    d: 'Las cinco operaciones CRUD se separan en rutas y controladores, con los códigos 200, 201, 204, 400 y 404.',
    f: ['src/controllers/libros.controller.js', 'src/routes/libros.routes.js', 'src/app.js', 'pruebas/http.js', 'pruebas/verificar_exp2.js'] },
  { t: 'Persistencia con MySQL y procedimientos almacenados',
    d: 'La lista en memoria se reemplaza por MySQL. Cada operación es un CALL a un procedimiento, con marcadores ? y mysql2/promise.',
    f: ['sql/biblioteca.sql', 'src/db.js', 'src/controllers/libros.controller.js', 'src/index.js', '.env.example'] },
  { t: 'Base de datos MySQL en la nube (Aiven, TLS)',
    d: 'La base se lleva a Aiven for MySQL. Solo cambian el .env y la opción ssl, que valida el certificado CA.',
    f: ['src/db.js', 'sql/nube_base_usuario.sql', 'pruebas/probar_conexion.js', '.env.example', '.gitignore'] },
  { t: 'Registro e inicio de sesión con JWT',
    d: 'Se registran usuarios con bcrypt y el login emite un JWT firmado con HS256 que expira en 1 hora.',
    f: ['sql/usuarios.sql', 'src/controllers/auth.controller.js', 'src/routes/auth.routes.js', 'src/app.js', 'pruebas/verificar_exp5.js'] },
  { t: 'Protección de rutas con middleware JWT y roles',
    d: 'Para escribir en el catálogo se necesita un token válido y rol admin: sin token 401, sin permiso 403. La lectura sigue siendo pública.',
    f: ['src/middlewares/auth.js', 'src/routes/libros.routes.js', 'src/routes/auth.routes.js', 'src/controllers/auth.controller.js', 'scripts/crear_admin.js', 'pruebas/verificar_exp6.js'] },
];

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const lenguaje = (f) => (f.endsWith('.sql') ? 'sql' : f.endsWith('.json') ? 'json' : f.endsWith('.js') ? 'javascript' : 'ini');
const resaltarSalida = (s) => esc(s)
  .replace(/^(\$ .*)$/gm, '<span class="cmd">$1</span>')
  .replace(/^(#.*)$/gm, '<span class="com">$1</span>')
  .replace(/^(\[servidor\].*)$/gm, '<span class="srv">$1</span>')
  .replace(/^(ERROR .*)$/gm, '<span class="errl">$1</span>')
  .replace(/(-&gt;\s*)(2\d\d)/g, '$1<b class="ok">$2</b>')
  .replace(/(-&gt;\s*)([45]\d\d)/g, '$1<b class="err">$2</b>');

const secciones = experiencias.map((e, i) => {
  const n = i + 1;
  const base = path.join(RAIZ, `experiencia${n}`, 'api_biblioteca');
  const salida = fs.readFileSync(path.join(EVID, `experiencia${n}_salida.txt`), 'utf8');
  const codigos = (e.f.map((f, k) => {
    const txt = fs.readFileSync(path.join(base, f), 'utf8');
    return `<div class="file${k === 0 ? ' on' : ''}" data-f="${k}"><div class="path">experiencia${n}/api_biblioteca/<b>${esc(f)}</b></div><pre><code class="language-${lenguaje(f)}">${esc(txt)}</code></pre></div>`;
  })).join('');
  const lista = e.f.map((f, k) => `<button class="fb${k === 0 ? ' on' : ''}" data-f="${k}">${esc(f)}</button>`).join('');
  return `<section id="e${n}">
  <h2><span>Experiencia ${n}</span>${esc(e.t)}</h2><p class="desc">${esc(e.d)}</p>
  <div class="tabs"><button class="tb on" data-t="code">Código</button><button class="tb" data-t="run">Ejecución</button></div>
  <div class="pane code on"><div class="files">${lista}</div><div class="viewer">${codigos}</div></div>
  <div class="pane run"><pre class="out">${resaltarSalida(salida)}</pre></div>
</section>`;
}).join('\n');

const html = `<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Laboratorio 12 — Código y evidencias</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<style>
:root{--bg:#f4f7f2;--card:#fff;--fg:#1d2a1d;--muted:#5b6b5b;--acc:#2f6b1f;--line:#d9e2d5;--pre:#0d1117;--pref:#dfe9dc;--ok:#7fd36b;--err:#ff8a7a;--cmd:#ffd479;--com:#8fb3ff;--srv:#7f8f80}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f140f;--card:#171f17;--fg:#e4ece2;--muted:#9fb09d;--acc:#8fd16f;--line:#2a352a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,Segoe UI,sans-serif}
header{padding:28px 16px 10px;max-width:1200px;margin:auto}h1{margin:0;font-size:26px;color:var(--acc)}header p{margin:6px 0 0;color:var(--muted)}
nav{position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 16px;max-width:1200px;margin:auto;display:flex;gap:8px;flex-wrap:wrap;border-bottom:1px solid var(--line)}
nav a{color:var(--acc);text-decoration:none;padding:4px 12px;border:1px solid currentColor;border-radius:999px;font-size:13px}
main{max-width:1200px;margin:auto;padding:8px 16px 40px}
section{background:var(--card);border:1px solid var(--line);border-radius:14px;margin:20px 0;padding:18px;scroll-margin-top:60px}
h2{margin:0;font-size:19px}h2 span{display:inline-block;background:var(--acc);color:#fff;border-radius:6px;padding:1px 9px;margin-right:10px;font-size:13px;vertical-align:2px}
.desc{margin:6px 0 12px;color:var(--muted)}
.tabs{display:flex;gap:6px;border-bottom:1px solid var(--line);margin-bottom:12px}
.tb{background:none;border:0;border-bottom:3px solid transparent;padding:6px 14px;font:inherit;font-weight:600;color:var(--muted);cursor:pointer}
.tb.on{color:var(--acc);border-color:var(--acc)}
.pane{display:none}.pane.on{display:block}
.code.on{display:grid;grid-template-columns:250px 1fr;gap:12px}
.files{display:flex;flex-direction:column;gap:4px}
.fb{text-align:left;background:none;border:1px solid var(--line);border-radius:8px;padding:6px 10px;font:12.5px Consolas,ui-monospace,monospace;color:var(--fg);cursor:pointer;overflow-wrap:anywhere}
.fb.on{background:var(--acc);border-color:var(--acc);color:#fff}
.file{display:none}.file.on{display:block}
.path{font:12px Consolas,monospace;color:var(--muted);margin-bottom:6px}.path b{color:var(--fg)}
pre{margin:0;background:var(--pre);color:var(--pref);border-radius:10px;overflow:auto;max-height:640px;font:13px/1.5 Consolas,ui-monospace,monospace}
pre code.hljs{padding:14px;background:transparent}pre.out{padding:14px;white-space:pre}
.cmd{color:var(--cmd)}.com{color:var(--com)}.srv{color:var(--srv)}.ok{color:var(--ok)}.err,.errl{color:var(--err)}
@media (max-width:760px){.code.on{grid-template-columns:1fr}.files{flex-direction:row;flex-wrap:wrap}}
</style></head><body>
<header><h1>Laboratorio N° 12 — Servicios REST Node.js y JWT</h1>
<p>Biblioteca Digital. Para cada experiencia, la pestaña <b>Código</b> muestra sus archivos clave y la pestaña <b>Ejecución</b> la salida real. Las experiencias 4 a 6 se ejecutaron contra Aiven for MySQL (nube real). Generado el ${new Date().toLocaleString('es-PE')}.</p></header>
<nav>${experiencias.map((_, i) => `<a href="#e${i + 1}">Exp. ${i + 1}</a>`).join('')}</nav>
<main>${secciones}</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/sql.min.js"></script>
<script>
try { hljs.highlightAll(); } catch (e) {}
document.querySelectorAll('section').forEach((s) => {
  s.querySelectorAll('.tb').forEach((b) => b.onclick = () => {
    s.querySelectorAll('.tb').forEach((x) => x.classList.toggle('on', x === b));
    s.querySelectorAll('.pane').forEach((p) => p.classList.toggle('on', p.classList.contains(b.dataset.t)));
  });
  s.querySelectorAll('.fb').forEach((b) => b.onclick = () => {
    s.querySelectorAll('.fb').forEach((x) => x.classList.toggle('on', x === b));
    s.querySelectorAll('.file').forEach((f) => f.classList.toggle('on', f.dataset.f === b.dataset.f));
  });
});
</script></body></html>`;
fs.writeFileSync(path.join(EVID, 'index.html'), html, 'utf8');
console.log('Informe generado:', path.join(EVID, 'index.html'));
