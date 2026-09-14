import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

export const GraficaIngresosGastos = ({ data }) => {
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
          <CartesianGrid strokeDasharray="3 3" stroke="#0a0101" />
          <XAxis dataKey="fecha" stroke="#888" />
          <YAxis stroke="#fdf1f1" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1d1515',
              border: '1px solid #555',
              borderRadius: '8px',
              color: '#f5f0e8',
            }}
            labelStyle={{ color: '#f5f0e8' }}
            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
          />
          <Legend />
          <Bar dataKey="INGRESO" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          <Bar dataKey="GASTO" fill="#764cd8" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};