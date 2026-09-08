import { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';

export const useGraficas = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGraficas = async () => {
    try {
      setLoading(true);
      const resultado = await analyticsService.getGraficas();
      setData(resultado);
    } catch (err) {
      setError(err.message || 'Error al cargar las gráficas');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraficas();
  }, []);

  return { data, loading, error, recargar: fetchGraficas };
};