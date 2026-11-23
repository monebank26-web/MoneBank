import React from 'react';
import { formatMoney } from '../../../core/utils/format';
import './ResumenMovimientos.css';

const formatoFecha = (fecha) => {
  if (!fecha) return '—';
  return new Date(fecha).toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  });
};

const ResumenMovimientos = ({ data, titulo = 'Balance mensual', periodoTexto }) => {
  if (!data) return null;

  const ingresos = Number(data.total_ingresos) || 0;
  const gastos = Number(data.total_gastos) || 0;
  const balance = Number(data.balance) || 0;
  const balancePositivo = balance >= 0;
  const sinMovimientos = ingresos === 0 && gastos === 0 && balance === 0;

  return (
    <section className="resumen-movimientos">
      <h3 className="resumen-movimientos__titulo">{titulo}</h3>
      <p className="resumen-movimientos__periodo">
        {periodoTexto || `${formatoFecha(data.periodo_inicio)} — ${formatoFecha(data.periodo_fin)}`}
      </p>

      <div className="resumen-movimientos__grid">
        <article className="resumen-movimientos__tarjeta resumen-movimientos__tarjeta--ingreso">
          <span className="resumen-movimientos__etiqueta">Ingresos</span>
          <strong className="resumen-movimientos__monto">{formatMoney(ingresos)}</strong>
        </article>

        <article className="resumen-movimientos__tarjeta resumen-movimientos__tarjeta--gasto">
          <span className="resumen-movimientos__etiqueta">Gastos</span>
          <strong className="resumen-movimientos__monto">{formatMoney(gastos)}</strong>
        </article>

        <article className={`resumen-movimientos__tarjeta resumen-movimientos__tarjeta--balance ${balancePositivo ? 'resumen-movimientos__tarjeta--positivo' : 'resumen-movimientos__tarjeta--negativo'}`}>
          <span className="resumen-movimientos__etiqueta">Balance</span>
          <strong className="resumen-movimientos__monto">{formatMoney(balance)}</strong>
        </article>
      </div>

      {sinMovimientos && (
        <p className="resumen-movimientos__vacio">Aún no hay movimientos registrados.</p>
      )}
    </section>
  );
};

export default ResumenMovimientos;
