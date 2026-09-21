import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#f97316', '#ec4899'];

export const GraficaCategoria = ({ data }) => {
  if (!data || data.length === 0) {
    return <p>No hay datos por categoría disponibles.</p>;
  }

  return (
    <div className="card">
      <h3>Totales por Categoría</h3>
      <ResponsiveContainer width="100%" height={Math.max(300, data.length * 50)}>
        <BarChart data={data} layout="vertical" margin={{ left: 40 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
          <XAxis type="number" stroke="#ffffff" />
          <YAxis type="category" dataKey="nombre_categoria" width={120} stroke="#ffeaea" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1a1a',
              border: '1px solid #e6dddd',
              borderRadius: '8px',
              color: '#f5f0e8',
            }}
            labelStyle={{ color: '#f5f0e8' }}
            itemStyle={{ color: '#f5f0e8' }}
            cursor={{ fill: 'rgba(199, 199, 199, 0.39)' }}
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