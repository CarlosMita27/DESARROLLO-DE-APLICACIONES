function Card({ nombre, descripcion, categoria }) {
  return (
    <article className="card">
      <h2>{nombre}</h2>
      <p>{descripcion}</p>
      <span>{categoria}</span>
    </article>
  )
}

export default Card
