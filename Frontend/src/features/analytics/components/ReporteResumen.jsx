import React from 'react';

const moneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(v);

const fecha = (f) =>
  new Date(f).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' });

export const ReporteResumen = ({ data }) => {
  if (!data) return null;

  const ingresos = Number(data.total_ingresos) || 0;
  const gastos = Number(data.total_gastos) || 0;
  const pctFlujo = ingresos > 0 ? Math.min(100, (gastos / ingresos) * 100) : 0;
  const pctAhorro = ingresos > 0 ? (data.balance / ingresos) * 100 : 0;

  return (
    <>
      <p className="an-muted an-periodo">
        Periodo: {fecha(data.periodo_inicio)} – {fecha(data.periodo_fin)}
      </p>
      <div className="an-grid3">
        <article className="an-card">
          <h3 className="an-label">Ingresos del periodo</h3>
          <p className="an-big">{moneda(ingresos)}</p>
        </article>
        <article className="an-card">
          <h3 className="an-label">Gastos totales</h3>
          <p className="an-big">{moneda(gastos)}</p>
          <div className="an-bar"><i style={{ width: `${pctFlujo}%` }} /></div>
          <p className="an-muted an-small">{pctFlujo.toFixed(1)}% de tus ingresos</p>
        </article>
        <article className="an-card">
          <h3 className="an-label">Balance neto</h3>
          <p className="an-big">{moneda(data.balance)}</p>
          <p className={`an-chip ${data.balance >= 0 ? 'an-chip--ok' : 'an-chip--neg'}`}>
            Capacidad de ahorro: {pctAhorro.toFixed(1)}%
          </p>
        </article>
      </div>
    </>
  );
};
