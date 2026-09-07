import React from 'react';
import { useGraficas } from '../hooks/useGraficas';
import { GraficaIngresosGastos } from '../components/GraficaIngresosGastos';
import { GraficaCategoria } from '../components/GraficaCategoria';

export const GraficasPage = () => {
  const { data, loading, error, recargar } = useGraficas();

  console.log('DATA RECIBIDA:', data);

  if (loading) {
    return <div className="p-4 text-center">Cargando datos financieros...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-red-500">
        <p>{error}</p>
        <button onClick={recargar} className="mt-2 px-4 py-2 bg-blue-500 text-white rounded">
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Gráficas Financieras</h1>
        <button onClick={recargar} className="px-3 py-1 bg-gray-200 rounded text-sm hover:bg-gray-300">
          Actualizar
        </button>
      </div>

     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <GraficaIngresosGastos data={data?.series} />
      <GraficaCategoria data={data?.totales_por_categoria} />
    </div>
    </div>
  );
};

export default GraficasPage;

