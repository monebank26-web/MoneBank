import { useState, useEffect } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { transaccionesService } from '../../transacciones/services/transaccionesService';

export const useMovimientosRecientes = (cantidad = 5) => {
  const { user } = useAuth();
  const [transacciones, setTransacciones] = useState([]);

  useEffect(() => {
    if (!user) return;
    transaccionesService.obtenerHistorial({
      por_pagina: cantidad,
      ordenar_por: 'fecha',
      orden: 'desc',
    })
      .then((data) => setTransacciones(data.items || []))
      .catch(() => setTransacciones([]));
  }, [user, cantidad]);

  return { transacciones };
};