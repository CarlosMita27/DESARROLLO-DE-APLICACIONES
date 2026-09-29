# DevLab React - Experiencia N.° 02

Proyecto React (Vite) que resuelve la Experiencia N.° 02 del Laboratorio N.° 06:
Componentes, props e interactividad.

## Cómo ejecutar

```bash
npm install
npm run dev
```

Abre en el navegador la dirección que muestre la terminal (normalmente
http://localhost:5173).

## Cómo tomar las capturas por Parte

El archivo `src/App.jsx` que viene en este ZIP es la versión FINAL (Parte 4:
con useState y el botón "Eliminar"). Para capturar las figuras de las partes
anteriores, reemplaza temporalmente el contenido de `App.jsx` por cada
versión indicada abajo, guarda, espera a que el navegador se actualice, y
toma la captura. Luego continúa con la siguiente versión.

### Parte 1 (Figura 6) — Header, Card y Footer con una sola tarjeta
```jsx
import Header from './components/Header'
import Footer from './components/Footer'
import Card from './components/Card'

function App() {
  return (
    <div className="contenedor">
      <Header />
      <Card
        nombre="React"
        descripcion="Biblioteca para construir interfaces"
        categoria="Frontend"
      />
      <Footer />
    </div>
  )
}

export default App
```

### Parte 2 (Figura 7) — Card reutilizado con props distintas
```jsx
import Header from './components/Header'
import Footer from './components/Footer'
import Card from './components/Card'

function App() {
  return (
    <div className="contenedor">
      <Header />
      <Card
        nombre="React"
        descripcion="Biblioteca para construir interfaces"
        categoria="Frontend"
      />
      <Card
        nombre="Node.js"
        descripcion="Entorno de ejecución de JavaScript"
        categoria="Backend"
      />
      <Footer />
    </div>
  )
}

export default App
```

### Parte 3 (Figura 8) — Tarjetas generadas con map(), sin botones aún
```jsx
import Header from './components/Header'
import Footer from './components/Footer'
import Card from './components/Card'

const tecnologias = [
  { id: 1, nombre: 'React', descripcion: 'Biblioteca de interfaces', categoria: 'Frontend' },
  { id: 2, nombre: 'Vite', descripcion: 'Herramienta de desarrollo web', categoria: 'Build tool' },
  { id: 3, nombre: 'Node.js', descripcion: 'Entorno de ejecución de JavaScript', categoria: 'Backend' },
  { id: 4, nombre: 'PostgreSQL', descripcion: 'Sistema de gestión de bases de datos', categoria: 'Base de datos' }
]

function App() {
  return (
    <div className="contenedor">
      <Header />
      {tecnologias.map((tecnologia) => (
        <Card
          key={tecnologia.id}
          nombre={tecnologia.nombre}
          descripcion={tecnologia.descripcion}
          categoria={tecnologia.categoria}
        />
      ))}
      <Footer />
    </div>
  )
}

export default App
```

### Parte 4 (Figuras 9 y 10) — versión final, ya incluida en src/App.jsx
Esta es la versión que ya viene puesta en el proyecto. Para la Figura 9,
captura el navegador con las 4 tarjetas y sus botones "Eliminar" visibles.
Para la Figura 10, haz clic en "Eliminar" sobre cualquiera de las tarjetas
y vuelve a capturar mostrando que ahora hay una tarjeta menos.
