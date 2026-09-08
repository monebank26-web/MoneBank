import { apiClient } from '../../../core/api/client';
import { STORAGE_KEYS } from '../../../core/constants';

const claveHistorial = (userId) => `${STORAGE_KEYS.CHAT_HISTORIAL}_${userId}`;

const obtenerHistorial = (userId) => {
  if (!userId) return [];
  const data = localStorage.getItem(claveHistorial(userId));
  return data ? JSON.parse(data) : [];
};

const guardarHistorial = (userId, historial) => {
  if (!userId) return;
  localStorage.setItem(claveHistorial(userId), JSON.stringify(historial));
};

const agregarTurnos = (userId, turnos) => {
  const historial = obtenerHistorial(userId);
  const actualizado = [...historial, ...turnos];
  guardarHistorial(userId, actualizado);
  return actualizado;
};

const limpiarHistorial = (userId) => {
  if (!userId) return;
  localStorage.removeItem(claveHistorial(userId));
};

const enviarMensaje = async ({ userId, mensaje, historial }) => {
  const respuesta = await apiClient.post('/chat-ia/mensaje', {
    mensaje,
    historial: historial || [],
  });

  const turnos = [
    { rol: 'user', texto: mensaje },
    { rol: 'model', texto: respuesta.respuesta },
  ];
  agregarTurnos(userId, turnos);

  return respuesta;
};

export const chatIaService = {
  obtenerHistorial,
  agregarTurnos,
  limpiarHistorial,
  enviarMensaje,
};
