import { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';

export const useReporte = (periodo = 'mensual', fechaInicio = null, fechaFin = null) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchReporte = async () => {
    try {
      setLoading(true);
      setError(null);
      const resultado = await analyticsService.getReporte(periodo, fechaInicio, fechaFin);
      setData(resultado);
    } catch (err) {
      setError(err.message || 'Error al cargar el reporte');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReporte();
  }, [periodo, fechaInicio, fechaFin]);

  return { data, loading, error, recargar: fetchReporte };
};