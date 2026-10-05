import { Link } from "react-router-dom";

function TareaItem({ tarea, onAlternar }) {
  return (
    <li className={tarea.completada ? "tarea completada" : "tarea"}>
      <Link to={`/tareas/${tarea.id}`}>{tarea.titulo}</Link>
      <button onClick={() => onAlternar(tarea.id)}>
        {tarea.completada ? "Deshacer" : "Completar"}
      </button>
    </li>
  );
}

export default TareaItem;
