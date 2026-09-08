import React from 'react';

export const EstadoSinMovimientos = ({ mensaje }) => {
  return (
    <div className="card">
      <p>{mensaje || 'No existen movimientos registrados para este periodo.'}</p>
    </div>
  );
};