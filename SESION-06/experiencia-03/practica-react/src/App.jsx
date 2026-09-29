import { useState } from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import Card from './components/Card'
import Formulario from './components/Formulario'
import Usuarios from './components/Usuarios'

function App() {
  const [tecnologias, setTecnologias] = useState([
    { id: 1, nombre: 'React', descripcion: 'Biblioteca de interfaces', categoria: 'Frontend' },
    { id: 2, nombre: 'Vite', descripcion: 'Herramienta de desarrollo web', categoria: 'Build tool' },
    { id: 3, nombre: 'Node.js', descripcion: 'Entorno de ejecución de JavaScript', categoria: 'Backend' },
    { id: 4, nombre: 'PostgreSQL', descripcion: 'Sistema de gestión de bases de datos', categoria: 'Base de datos' }
  ])

  function eliminarTecnologia(id) {
    setTecnologias(tecnologias.filter((tecnologia) => tecnologia.id !== id))
  }

  function agregarTecnologia(nuevaTecnologia) {
    setTecnologias([
      ...tecnologias,
      { id: Date.now(), ...nuevaTecnologia, categoria: 'Nueva' }
    ])
  }

  return (
    <div className="contenedor">
      <Header />
      {tecnologias.map((tecnologia) => (
        <div key={tecnologia.id}>
          <Card
            nombre={tecnologia.nombre}
            descripcion={tecnologia.descripcion}
            categoria={tecnologia.categoria}
          />
          <button onClick={() => eliminarTecnologia(tecnologia.id)}>
            Eliminar
          </button>
        </div>
      ))}
      <Formulario agregarTecnologia={agregarTecnologia} />
      <Usuarios />
      <Footer />
    </div>
  )
}

export default App
