import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { chatIaService } from '../services/chatIaService';

export const useChatIA = () => {
  const { user } = useAuth();
  const userId = user?.id;
  const [mensajes, setMensajes] = useState([]);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!userId) return;
    setMensajes(chatIaService.obtenerHistorial(userId));
  }, [userId]);

  const enviar = useCallback(async (mensaje) => {
    if (!mensaje || !mensaje.trim()) return;
    setCargando(true);
    setError('');
    try {
      const historial = chatIaService.obtenerHistorial(userId);
      const respuesta = await chatIaService.enviarMensaje({
        userId,
        mensaje: mensaje.trim(),
        historial,
      });
      setMensajes([
        ...historial,
        { rol: 'user', texto: mensaje.trim() },
        { rol: 'model', texto: respuesta.respuesta },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  }, [userId]);

  const limpiar = useCallback(() => {
    chatIaService.limpiarHistorial(userId);
    setMensajes([]);
  }, [userId]);

  return { mensajes, cargando, error, enviar, limpiar };
};
