import React from 'react';
import { EstadoSinMovimientos } from './EstadoSinMovimientos';

const formatoMoneda = (valor) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(valor);

const formatoFecha = (fecha) =>
  new Date(fecha).toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  });
  
export const ResumenSemanalCard = ({ data }) => {
  if (!data) return null;

  if (!data.tiene_movimientos) {
    return <EstadoSinMovimientos mensaje={data.mensaje} />;
  }

  const balancePositivo = data.balance >= 0;

  return (
    <div className="card">
      <h3>Resumen semanal</h3>
      <p className="periodo">
        {formatoFecha(data.periodo_inicio)} — {formatoFecha(data.periodo_fin)}
      </p>

      <div className="resumen-grid">
        <div className="resumen-item ingreso">
          <span>Ingresos</span>
          <strong>{formatoMoneda(data.total_ingresos)}</strong>
        </div>
        <div className="resumen-item gasto">
          <span>Gastos</span>
          <strong>{formatoMoneda(data.total_gastos)}</strong>
        </div>
        <div className={`resumen-item balance ${balancePositivo ? 'positivo' : 'negativo'}`}>
          <span>Balance</span>
          <strong>{formatoMoneda(data.balance)}</strong>
        </div>
      </div>
    </div>
  );
};

