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
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="fecha" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="INGRESO" fill="#0d49a8" radius={[4, 4, 0, 0]} />
          <Bar dataKey="GASTO" fill="#7b1fb8" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};