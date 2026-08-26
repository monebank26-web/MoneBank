import React from 'react';
import { ROLES } from '../../../core/constants';
import { etiquetaRol } from '../../../core/utils/roles';

const BarraFiltrosUsuarios = ({ busqueda, setBusqueda, filtroRol, setFiltroRol }) => {
  return (
    <div className="barra-filtros-admin">
      <input
        className="campo-busqueda-admin"
        type="text"
        placeholder="Buscar por nombre o correo..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />
      <div className="filtros-rol-admin">
        {['todos', ROLES.NORMAL, ROLES.PADRE, ROLES.HIJO, ROLES.ADMIN].map((rol) => (
          <button
            key={rol}
            className={`boton-filtro-admin ${filtroRol === rol ? 'boton-filtro-admin--activo' : ''}`}
            onClick={() => setFiltroRol(rol)}
          >
            {rol === 'todos' ? 'Todos' : etiquetaRol(rol)}
          </button>
        ))}
      </div>
    </div>
  );
};

export default BarraFiltrosUsuarios;
