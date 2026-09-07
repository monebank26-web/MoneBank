import { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';

export const useResumenSemanal = (fechaInicio = null, fechaFin = null) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchResumen = async () => {
    try {
      setLoading(true);
      setError(null);
      const resultado = await analyticsService.getResumenSemanal(fechaInicio, fechaFin);
      setData(resultado);
    } catch (err) {
      setError(err.message || 'Error al cargar el resumen semanal');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumen();
  }, [fechaInicio, fechaFin]);

  return { data, loading, error, recargar: fetchResumen };
};