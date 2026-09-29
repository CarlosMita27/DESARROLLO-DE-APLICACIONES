import { useState } from 'react'

function Formulario({ agregarTecnologia }) {
  const [formulario, setFormulario] = useState({
    nombre: '',
    descripcion: ''
  })

  function manejarCambio(event) {
    const { name, value } = event.target
    setFormulario({
      ...formulario,
      [name]: value
    })
  }

  function manejarEnvio(event) {
    event.preventDefault()
    agregarTecnologia(formulario)
    setFormulario({ nombre: '', descripcion: '' })
  }

  return (
    <form onSubmit={manejarEnvio}>
      <label>
        Nombre:
        <input
          type="text"
          name="nombre"
          value={formulario.nombre}
          onChange={manejarCambio}
        />
      </label>
      <label>
        Descripción:
        <input
          type="text"
          name="descripcion"
          value={formulario.descripcion}
          onChange={manejarCambio}
        />
      </label>
      <button type="submit">Registrar</button>
    </form>
  )
}

export default Formulario
