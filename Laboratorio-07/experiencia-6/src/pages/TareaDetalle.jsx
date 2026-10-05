import { Link, useOutletContext, useParams } from "react-router-dom";

function TareaDetalle() {
  const { id } = useParams();
  const { tareas } = useOutletContext();
  const tarea = tareas.find((t) => String(t.id) === id);

  if (!tarea) {
    return (
      <div className="detalle">
        <p>No se encontró la tarea con id: {id}</p>
        <Link to="/tareas">Volver a la lista</Link>
      </div>
    );
  }

  return (
    <div className="detalle">
      <h3>Detalle de la tarea</h3>
      <p><strong>Id:</strong> {tarea.id}</p>
      <p><strong>Título:</strong> {tarea.titulo}</p>
      <p><strong>Estado:</strong> {tarea.completada ? "Completada" : "Pendiente"}</p>
      <Link to="/tareas">Volver a la lista</Link>
    </div>
  );
}

export default TareaDetalle;
