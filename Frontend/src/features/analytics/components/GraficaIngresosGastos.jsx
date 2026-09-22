import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import { useTheme } from '../../../core/context/ThemeContext';

export const GraficaIngresosGastos = ({ data }) => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  // Colores según el modo
  const colors = {
    grid: isDark ? '#333' : '#e0e0e0',
    axis: isDark ? '#ccc' : '#555',
    tooltipBg: isDark ? '#1d1515' : '#ffffff',
    tooltipBorder: isDark ? '#555' : '#ddd',
    tooltipText: isDark ? '#f5f0e8' : '#1a1a1a',
    cursorFill: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
  };

  if (!data || data.length === 0) {
    return <p>No existen movimientos registrados para mostrar la gráfica.</p>;
  }

  const agrupado = {};
  data.forEach(item => {
    const fecha = new Date(item.fecha).toLocaleDateString();
    if (!agrupado[fecha]) {
      agrupado[fecha] = { fecha };
    }
    agrupado[fecha][item.tipo_transaccion] = item.total;
  });
  const chartData = Object.values(agrupado);

  return (
    <div className="card">
      <h3>Evolución de Ingresos y Gastos</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
          <XAxis dataKey="fecha" stroke={colors.axis} />
          <YAxis stroke={colors.axis} />
          <Tooltip
            contentStyle={{
              backgroundColor: colors.tooltipBg,
              border: `1px solid ${colors.tooltipBorder}`,
              borderRadius: '8px',
              color: colors.tooltipText,
            }}
            labelStyle={{ color: colors.tooltipText }}
            cursor={{ fill: colors.cursorFill }}
          />
          <Legend />
          <Bar dataKey="INGRESO" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          <Bar dataKey="GASTO" fill="#764cd8" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};