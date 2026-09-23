import { useState, useEffect, useCallback } from 'react';
import { metasService } from '../services/metasService';

const RESULTADO_VACIO = {
  total_ahorrado: 0,
  monto_objetivo_total: 0,
  porcentaje_consolidado: 0,
  cantidad_metas: 0,
};

export const useResumenGlobalMetas = () => {
  const [resumen, setResumen] = useState(RESULTADO_VACIO);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const data = await metasService.resumenGlobal();
      setResumen({ ...RESULTADO_VACIO, ...data });
      setError('');
    } catch (err) {
      setResumen(RESULTADO_VACIO);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);

  return { resumen, loading, error, recargar: cargar };
};