import { useCallback, useEffect, useState } from 'react';
import { controlParentalService } from '../services/controlParentalServices';

export const useControlParental = () => {
  const [relaciones, setRelaciones] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');

  const cargar = useCallback(async () => {
    try {
      setCargando(true);
      setError('');

      const data = await controlParentalService.obtenerVinculaciones();

      setRelaciones(Array.isArray(data) ? data : []);
    } catch (e) {
      setError(e.message || 'No se pudieron cargar las vinculaciones.');
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const ejecutar = async (fn, mensajeExito) => {
    try {
      setError('');
      setMensaje('');

      await fn();

      setMensaje(mensajeExito);
      await cargar();

      return true;
    } catch (e) {
      setError(e.message || 'No se pudo completar la operación.');
      return false;
    }
  };

  return {
    relaciones,
    cargando,
    error,
    mensaje,
    cargar,
    ejecutar,
  };
};
