import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell, LabelList } from 'recharts';
import { useTheme } from '../../../core/context/ThemeContext';

const COLORS = ['#f5b73d', '#3b9ad9', '#4cc38a', '#7a8cff', '#ff8a5c', '#b58cf0', '#06b6d4', '#ec4899'];
const moneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(v);

export const GraficaCategoria = ({ data }) => {
  const isDark = useTheme().theme === 'dark';
  const axis = isDark ? '#8a8174' : '#555';
  const grid = isDark ? '#2e2820' : '#e0e0e0';

  // Solo gastos: se excluyen los ingresos (Salario, Ventas), de mayor a menor
  const gastos = (data || [])
    .filter((d) => d.tipo_transaccion !== 'INGRESO')
    .sort((a, b) => b.total - a.total);

  if (gastos.length === 0) {
    return <div className="an-card"><p>No hay gastos por categoría disponibles.</p></div>;
  }

  return (
    <div className="an-card">
      <h3>Gastos por categoría</h3>
      <ResponsiveContainer width="100%" height={Math.max(220, gastos.length * 44)}>
        <BarChart data={gastos} layout="vertical" margin={{ left: 10, right: 80 }}>
          <CartesianGrid strokeDasharray="3 3" stroke={grid} horizontal={false} />
          <XAxis type="number" hide />
          <YAxis type="category" dataKey="nombre_categoria" width={110} stroke={axis} tickLine={false} axisLine={false} />
          <Tooltip
            formatter={(v) => moneda(v)}
            contentStyle={{ background: isDark ? '#1d1914' : '#fff', border: `1px solid ${grid}`, borderRadius: 8 }}
            cursor={{ fill: 'rgba(255,255,255,.04)' }}
          />
          <Bar dataKey="total" radius={[0, 4, 4, 0]}>
            {gastos.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            <LabelList dataKey="total" position="right" formatter={moneda} fill={axis} fontSize={12} />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};