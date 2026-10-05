import { useOutletContext } from "react-router-dom";
import FormularioTarea from "../components/FormularioTarea";
import TareaLista from "../components/TareaLista";

function TareasLista() {
  const { tareas, alternarTarea, agregarTarea } = useOutletContext();

  return (
    <>
      <FormularioTarea onAgregar={agregarTarea} />
      <TareaLista tareas={tareas} onAlternar={alternarTarea} />
    </>
  );
}

export default TareasLista;
