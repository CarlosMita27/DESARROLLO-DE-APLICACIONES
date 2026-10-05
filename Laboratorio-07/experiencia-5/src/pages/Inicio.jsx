import Encabezado from "../components/Encabezado";

function Inicio() {
  return (
    <div className="contenido">
      <Encabezado usuario="Carlos" />
      <p>Bienvenido a TaskFlow. Use el menú para ir a la lista de tareas.</p>
    </div>
  );
}

export default Inicio;
