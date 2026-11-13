import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { useTheme } from '../../../core/context/ThemeContext';

const moneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(v);

export const GraficaIngresosGastos = ({ data }) => {
  const isDark = useTheme().theme === 'dark';
  const c = {
    grid: isDark ? '#2e2820' : '#e0e0e0',
    axis: isDark ? '#8a8174' : '#555',
    tipBg: isDark ? '#1d1914' : '#ffffff',
    tipBorder: isDark ? '#2e2820' : '#ddd',
    tipText: isDark ? '#f2ede4' : '#1a1a1a',
  };

  if (!data || data.length === 0) {
    return <div className="an-card"><p>No existen movimientos registrados para mostrar la gráfica.</p></div>;
  }

  const agrupado = {};
  data.forEach((item) => {
    const f = new Date(item.fecha).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', timeZone: 'UTC' });
    if (!agrupado[f]) agrupado[f] = { fecha: f };
    agrupado[f][item.tipo_transaccion] = item.total;
  });
  const chartData = Object.values(agrupado);

  return (
    <div className="an-card">
      <h3>Evolución de ingresos y gastos</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={c.grid} vertical={false} />
          <XAxis dataKey="fecha" stroke={c.axis} tickLine={false} />
          <YAxis stroke={c.axis} tickLine={false} axisLine={false} />
          <Tooltip
            formatter={(v) => moneda(v)}
            contentStyle={{ background: c.tipBg, border: `1px solid ${c.tipBorder}`, borderRadius: 8, color: c.tipText }}
            labelStyle={{ color: c.tipText }}
            cursor={{ fill: isDark ? 'rgba(255,255,255,.04)' : 'rgba(0,0,0,.04)' }}
          />
          <Bar dataKey="INGRESO" name="Ingresos" fill="#3b9ad9" radius={[4, 4, 0, 0]} />
          <Bar dataKey="GASTO" name="Gastos" fill="#f5b73d" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="an-legend"><i style={{ background: '#3b9ad9' }} />Ingresos <i style={{ background: '#f5b73d' }} />Gastos</p>
    </div>
  );
};
