import { useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';

export const useConsignarSaldo = () => {
  const { user, login } = useAuth();
  const [modalConsignarAbierto, setModalConsignarAbierto] = useState(false);
  const [montoConsignar, setMontoConsignar] = useState('');
  const [errorConsignar, setErrorConsignar] = useState('');

  const handleConsignar = () => {
    const monto = parseInt(montoConsignar, 10);
    if (!monto || monto <= 0) {
      setErrorConsignar('Ingresa un monto válido.');
      return;
    }
    const nuevoSaldo = (user.saldoCuenta || 0) + monto;
    authService.actualizarSaldo(user.id, nuevoSaldo);
    login({ ...user, saldoCuenta: nuevoSaldo });
    setMontoConsignar('');
    setErrorConsignar('');
    setModalConsignarAbierto(false);
  };

  return {
    modalConsignarAbierto,
    setModalConsignarAbierto,
    montoConsignar,
    setMontoConsignar,
    errorConsignar,
    handleConsignar,
  };
};
