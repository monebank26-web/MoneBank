// features/bolsillos/hooks/useBolsillos.js
import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { bolsillosService } from '../services/bolsillosService';
import { authService } from '../../auth/services/authService';

export const useBolsillos = () => {
  const { user, login } = useAuth();
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
    if (monto > user.saldoCuenta) throw new Error('Saldo insuficiente en Mi Cuenta.');

    const nuevo = await bolsillosService.crear({ nombre, descripcion, color, montoInicial: monto, userId: user.id });

    // Descontar de Mi Cuenta
    const nuevoSaldo = user.saldoCuenta - monto;
    authService.actualizarSaldo(user.id, nuevoSaldo);
    login({ ...user, saldoCuenta: nuevoSaldo });

    setBolsillos((prev) => [...prev, nuevo]);
    return nuevo;
  };

  const eliminar = async (id) => {
    const bolsillo = bolsillos.find((b) => b.id === id);
    await bolsillosService.eliminar(id, user.id);

    // Devolver saldo a Mi Cuenta
    if (bolsillo && bolsillo.saldo > 0) {
      const nuevoSaldo = user.saldoCuenta + bolsillo.saldo;
      authService.actualizarSaldo(user.id, nuevoSaldo);
      login({ ...user, saldoCuenta: nuevoSaldo });
    }

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