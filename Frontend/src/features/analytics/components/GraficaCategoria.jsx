import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';
import { useTheme } from '../../../core/context/ThemeContext';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316', '#ec4899'];

export const GraficaCategoria = ({ data }) => {
  const { theme } = useTheme();
  const isDark = theme === 'dark';

  const colors = {
    grid: isDark ? '#333' : '#e0e0e0',
    axis: isDark ? '#ccc' : '#555',
    tooltipBg: isDark ? '#1a1a1a' : '#ffffff',
    tooltipBorder: isDark ? '#e6dddd' : '#ddd',
    tooltipText: isDark ? '#f5f0e8' : '#1a1a1a',
    cursorFill: isDark ? 'rgba(199, 199, 199, 0.39)' : 'rgba(0, 0, 0, 0.06)',
  };

  if (!data || data.length === 0) {
    return <p>No hay datos por categoría disponibles.</p>;
  }

  return (
    <div className="card">
      <h3>Totales por Categoría</h3>
      <ResponsiveContainer width="100%" height={Math.max(300, data.length * 50)}>
        <BarChart data={data} layout="vertical" margin={{ left: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={colors.grid} />
          <XAxis type="number" stroke={colors.axis} />
          <YAxis type="category" dataKey="nombre_categoria" width={120} stroke={colors.axis} />
          <Tooltip
            contentStyle={{
              backgroundColor: colors.tooltipBg,
              border: `1px solid ${colors.tooltipBorder}`,
              borderRadius: '8px',
              color: colors.tooltipText,
            }}
            labelStyle={{ color: colors.tooltipText }}
            itemStyle={{ color: colors.tooltipText }}
            cursor={{ fill: colors.cursorFill }}
          />
          <Bar dataKey="total" radius={[0, 4, 4, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};