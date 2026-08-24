import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { bolsillosService } from '../services/bolsillosService';

export const useBolsillos = () => {
  const { user } = useAuth();
  const [bolsillos, setBolsillos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const cargar = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      const data = await bolsillosService.listar(user.id);
      setBolsillos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => { cargar(); }, [cargar]);

  const crear = async ({ nombre, descripcion, color, montoInicial }) => {
    const monto = parseFloat(montoInicial) || 0;
    const nuevo = await bolsillosService.crear({ nombre, descripcion, color, montoInicial: monto, userId: user.id });
    setBolsillos((prev) => [...prev, nuevo]);
    return nuevo;
  };

  const eliminar = async (id) => {
    await bolsillosService.eliminar(id, user.id);
    setBolsillos((prev) => prev.filter((b) => b.id !== id));
  };

  const editar = async (id, datos) => {
    const bolsillosActuales = JSON.parse(localStorage.getItem('mb_bolsillos') || '[]');
    const actualizados = bolsillosActuales.map((b) => b.id === id ? { ...b, ...datos } : b);
    localStorage.setItem('mb_bolsillos', JSON.stringify(actualizados));
    await cargar();
  };

  const transferir = async (datos) => {
    const resultado = await bolsillosService.transferir({ ...datos, userId: user.id });
    await cargar();
    return resultado;
  };

  const depositar = async (datos) => {
    const resultado = await bolsillosService.depositar({ ...datos, userId: user.id });
    await cargar();
    return resultado;
  };

  const totalSaldo = bolsillos.reduce((acc, b) => acc + b.saldo, 0);

  return { bolsillos, loading, error, crear, eliminar, transferir, depositar, editar, totalSaldo, recargar: cargar };
};