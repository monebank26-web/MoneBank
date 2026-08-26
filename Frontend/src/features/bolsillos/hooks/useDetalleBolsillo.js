import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { bolsillosService } from '../services/bolsillosService';

export const useDetalleBolsillo = ({ id, bolsillos, editar, depositar, transferir }) => {
  const { user } = useAuth();

  const [bolsillo, setBolsillo] = useState(null);
  const [movimientos, setMovimientos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [noEncontrado, setNoEncontrado] = useState(false);

  const cargarDatos = useCallback(async () => {
    if (!user) return;
    setCargando(true);
    try {
      const encontrado = await bolsillosService.obtener(id, user.id);
      setBolsillo(encontrado);
      const historial = await bolsillosService.historialTransacciones(user.id, id);
      setMovimientos(historial);
      setNoEncontrado(false);
    } catch (e) {
      setNoEncontrado(true);
    } finally {
      setCargando(false);
    }
  }, [id, user]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  useEffect(() => {
    const actualizado = bolsillos.find((b) => b.id === id);
    if (actualizado) setBolsillo(actualizado);
  }, [bolsillos, id]);

  const editarYRecargar = async (bolsilloId, datos) => {
    await editar(bolsilloId, datos);
    await cargarDatos();
  };

  const depositarYRecargar = async (datos) => {
    const resultado = await depositar(datos);
    await cargarDatos();
    return resultado;
  };

  const transferirYRecargar = async (datos) => {
    const resultado = await transferir(datos);
    await cargarDatos();
    return resultado;
  };

  return {
    bolsillo,
    movimientos,
    cargando,
    noEncontrado,
    editarYRecargar,
    depositarYRecargar,
    transferirYRecargar,
  };
};
