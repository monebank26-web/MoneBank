import { useState, useEffect } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { bolsillosService } from '../../bolsillos/services/bolsillosService';

export const useMovimientosRecientes = (cantidad = 5) => {
  const { user } = useAuth();
  const [transacciones, setTransacciones] = useState([]);

  useEffect(() => {
    if (user) {
      bolsillosService.historialTransacciones(user.id).then((data) => {
        setTransacciones(data.slice(0, cantidad));
      });
    }
  }, [user, cantidad]);

  return { transacciones };
};
