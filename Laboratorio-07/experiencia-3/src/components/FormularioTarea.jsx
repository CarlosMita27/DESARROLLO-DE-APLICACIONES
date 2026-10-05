import { useState } from "react";

function FormularioTarea({ onAgregar }) {
  const [titulo, setTitulo] = useState("");

  const manejarEnvio = (evento) => {
    evento.preventDefault();
    const limpio = titulo.trim();
    if (limpio === "") return;
    onAgregar(limpio);
    setTitulo("");
  };

  return (
    <form onSubmit={manejarEnvio} className="formulario-tarea">
      <input
        type="text"
        value={titulo}
        onChange={(evento) => setTitulo(evento.target.value)}
        placeholder="Escribe una nueva tarea"
      />
      <button type="submit">Agregar</button>
    </form>
  );
}

export default FormularioTarea;
