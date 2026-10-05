import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Inicio from "./pages/Inicio";
import TareasLayout from "./pages/TareasLayout";
import TareasLista from "./pages/TareasLista";
import TareaDetalle from "./pages/TareaDetalle";

function App() {
  return (
    <BrowserRouter>
      <nav className="nav">
        <Link to="/">Inicio</Link>
        <Link to="/tareas">Tareas</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/tareas" element={<TareasLayout />}>
          <Route index element={<TareasLista />} />
          <Route path=":id" element={<TareaDetalle />} />
        </Route>
        <Route path="*" element={<p className="contenido">Página no encontrada</p>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
