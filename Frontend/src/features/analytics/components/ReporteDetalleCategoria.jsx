import React, { useState } from 'react';

const moneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(v);

export const ReporteDetalleCategoria = ({ detalle }) => {
  const [busqueda, setBusqueda] = useState('');

  if (!detalle || detalle.length === 0) {
    return <div className="an-card"><p>No hay movimientos registrados en este periodo.</p></div>;
  }

  // % de cada fila sobre el total de su mismo tipo (ingresos con ingresos, gastos con gastos)
  const totalPorTipo = detalle.reduce((acc, d) => {
    acc[d.tipo_transaccion] = (acc[d.tipo_transaccion] || 0) + Number(d.total);
    return acc;
  }, {});

  const filas = detalle.filter((d) =>
    d.nombre_categoria.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="an-card">
      <div className="an-table-head">
        <div>
          <h3>Detalle por categoría</h3>
          <p className="an-muted an-small">Mostrando {filas.length} de {detalle.length} categorías</p>
        </div>
        <input type="search" placeholder="Buscar categoría…" value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)} aria-label="Buscar categoría" />
      </div>
      <div className="an-scroll">
        <table className="an-table">
          <thead>
            <tr><th>Categoría</th><th>Tipo</th><th>Total (COP)</th><th>% del tipo</th></tr>
          </thead>
          <tbody>
            {filas.map((d, i) => {
              const pct = totalPorTipo[d.tipo_transaccion] > 0
                ? (Number(d.total) / totalPorTipo[d.tipo_transaccion]) * 100 : 0;
              return (
                <tr key={i}>
                  <td><b>{d.nombre_categoria}</b></td>
                  <td>
                    <span className={`an-pill ${d.tipo_transaccion === 'INGRESO' ? 'an-pill--in' : 'an-pill--out'}`}>
                      {d.tipo_transaccion === 'INGRESO' ? 'Ingreso' : 'Gasto'}
                    </span>
                  </td>
                  <td>{moneda(d.total)}</td>
                  <td><div className="an-bar an-bar--sm"><i style={{ width: `${pct}%` }} /></div>{pct.toFixed(1)}%</td>
                </tr>
              );
            })}
            {filas.length === 0 && (
              <tr><td colSpan={4} className="an-muted">No hay categorías que coincidan con “{busqueda}”.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
