import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { useTheme } from '../../../core/context/ThemeContext';

const moneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(v);

export const GraficaMovimientos = ({ data }) => {
  const isDark = useTheme().theme === 'dark';

  if (!data || data.length === 0) {
    return <div className="an-card"><p>No hay datos de movimientos disponibles.</p></div>;
  }

  // El backend debe marcar cada categoría con tipo_transaccion.
  const tieneTipo = data.some((d) => 'tipo_transaccion' in d);
  if (!tieneTipo) {
    console.warn(
      '[GraficaMovimientos] totales_por_categoria no trae "tipo_transaccion". ' +
      'No se puede separar ingresos de gastos; pide ese campo al backend.'
    );
    return (
      <div className="an-card">
        <h3>Ingresos vs. Gastos</h3>
        <p className="an-muted an-small">
          Falta el campo <code>tipo_transaccion</code> en la respuesta del backend.
        </p>
      </div>
    );
  }

  const totalIngresos = data
    .filter((d) => d.tipo_transaccion === 'INGRESO')
    .reduce((s, d) => s + Number(d.total), 0);
  const totalGastos = data
    .filter((d) => d.tipo_transaccion === 'GASTO')
    .reduce((s, d) => s + Number(d.total), 0);

  const total = totalIngresos + totalGastos;

  if (total === 0) {
    return (
      <div className="an-card">
        <h3>Ingresos vs. Gastos</h3>
        <p>No hay movimientos registrados en este periodo.</p>
      </div>
    );
  }

  const movimientos = [
    { nombre: 'Ingresos', total: totalIngresos, color: '#3b9ad9' },
    { nombre: 'Gastos', total: totalGastos, color: '#f5b73d' },
  ].filter((m) => m.total > 0);

  const pctIngresos = ((totalIngresos / total) * 100).toFixed(1);
  const pctGastos = ((totalGastos / total) * 100).toFixed(1);

  return (
    <div className="an-card">
      <h3>Ingresos vs. Gastos</h3>
      <p className="an-muted an-small">
        {pctIngresos}% ingresos · {pctGastos}% gastos, sobre {moneda(total)}
      </p>
      <div className="an-donut-row">
        <ResponsiveContainer width="100%" height={220} className="an-donut-chart">
          <PieChart>
            <Pie data={movimientos} dataKey="total" nameKey="nombre" innerRadius={62} outerRadius={95} stroke="none">
              {movimientos.map((m, i) => <Cell key={i} fill={m.color} />)}
            </Pie>
            <Tooltip
              formatter={(v) => moneda(v)}
              contentStyle={{
                background: isDark ? '#1d1914' : '#fff',
                border: `1px solid ${isDark ? '#2e2820' : '#ddd'}`,
                borderRadius: 8,
                color: isDark ? '#f2ede4' : '#1a1a1a',
              }}
              itemStyle={{ color: isDark ? '#f2ede4' : '#1a1a1a' }}
            />
          </PieChart>
        </ResponsiveContainer>
        <ul className="an-cats an-cats--aside">
          {movimientos.map((m, i) => (
            <li key={i}>
              <i style={{ background: m.color }} />
              {m.nombre}
              <b>{moneda(m.total)}</b>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};