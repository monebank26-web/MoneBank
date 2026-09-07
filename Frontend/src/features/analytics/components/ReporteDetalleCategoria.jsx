import React from 'react';

const formatoMoneda = (valor) =>
  new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(valor);

export const ReporteDetalleCategoria = ({ detalle }) => {
  if (!detalle || detalle.length === 0) {
    return (
      <div className="card">
        <p>No hay movimientos registrados en este periodo.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3>Detalle por categoría</h3>
      <table className="tabla-detalle">
        <thead>
          <tr>
            <th>Categoría</th>
            <th>Tipo</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {detalle.map((item, index) => (
            <tr key={index} className={item.tipo_transaccion === 'INGRESO' ? 'fila-ingreso' : 'fila-gasto'}>
              <td>{item.nombre_categoria}</td>
              <td>{item.tipo_transaccion}</td>
              <td>{formatoMoneda(item.total)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};