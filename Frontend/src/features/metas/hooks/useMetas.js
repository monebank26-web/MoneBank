import { useState, useEffect, useCallback } from 'react';
import { metasService } from '../services/metasService';

export const useMetas = () => {
  const [metas, setMetas] = useState([]);
  const [programaciones, setProgramaciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const data = await metasService.listar();
      setMetas(Array.isArray(data) ? data : []);
      setError('');
    } catch (err) {
      setError(err.message);
    }

    try {
      const dataProgramaciones = await metasService.listarProgramaciones();
      setProgramaciones(Array.isArray(dataProgramaciones) ? dataProgramaciones : []);
    } catch {
      setProgramaciones([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);

  const crear = async (datos) => {
    await metasService.crear(datos);
    await cargar();
  };

  const abonar = async (datos) => {
    await metasService.abonar(datos);
    await cargar();
  };

  const programar = async (datos) => {
    await metasService.programarAporte(datos);
    await cargar();
  };

  const actualizarEstado = async (datos) => {
    await metasService.actualizarEstadoProgramacion(datos);
    await cargar();
  };

  return { metas, programaciones, loading, error, crear, abonar, programar, actualizarEstado, recargar: cargar };
};
