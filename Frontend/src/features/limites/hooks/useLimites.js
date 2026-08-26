import { useState, useEffect, useCallback } from 'react';
import { limitesService } from '../services/limitesService';

export const useLimites = () => {
  const [limites, setLimites] = useState([]);
  const [alertas, setAlertas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const [datosLimites, datosAlertas] = await Promise.all([
        limitesService.listar(),
        limitesService.alertas().catch(() => []),
      ]);
      setLimites(Array.isArray(datosLimites) ? datosLimites : []);
      setAlertas(Array.isArray(datosAlertas) ? datosAlertas : []);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);

  const crear = async (datos) => {
    await limitesService.crear(datos);
    await cargar();
  };

  return { limites, alertas, loading, error, crear, recargar: cargar };
};
