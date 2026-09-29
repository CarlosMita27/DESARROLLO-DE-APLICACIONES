import { useState, useEffect } from 'react'

function Usuarios() {
  const [usuarios, setUsuarios] = useState([])
  const [cargando, setCargando] = useState(true)

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/users')
      .then((respuesta) => respuesta.json())
      .then((datos) => {
        setUsuarios(datos)
        setCargando(false)
      })
  }, [])

  if (cargando) {
    return <p>Cargando información...</p>
  }

  return (
    <div className="usuarios">
      <h2>Usuarios</h2>
      {usuarios.map((usuario) => (
        <p key={usuario.id}>{usuario.name}</p>
      ))}
    </div>
  )
}

export default Usuarios