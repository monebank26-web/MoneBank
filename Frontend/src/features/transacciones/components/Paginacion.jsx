import React from 'react';
import './Paginacion.css';

const Paginacion = ({ pagina, totalPaginas, onChange }) => {
  if (totalPaginas <= 1) return null;

  return (
    <div className="paginacion">
      <button
        className="paginacion__btn"
        disabled={pagina <= 1}
        onClick={() => onChange(pagina - 1)}
      >
        ← Anterior
      </button>

      <span className="paginacion__info">
        Página {pagina} de {totalPaginas}
      </span>

      <button
        className="paginacion__btn"
        disabled={pagina >= totalPaginas}
        onClick={() => onChange(pagina + 1)}
      >
        Siguiente →
      </button>
    </div>
  );
};

export default Paginacion;