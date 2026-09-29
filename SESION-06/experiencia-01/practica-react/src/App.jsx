function App() {
  const nombreApp = 'DevLab React'
  const equipo = 'André Lazo, José Lima, Carlos Mita, Carlos Yepez'
  const curso = 'Desarrollo de Aplicaciones'
  const practica = 6

  return (
    <div className="contenedor">
      <h1>{nombreApp}</h1>
      <p>Equipo: {equipo}</p>
      <p>{curso} - Práctica N.° {practica}</p>
      <img
        src="/vite.svg"
        alt="Logo del proyecto"
        width="80"
      />
    </div>
  )
}

export default App