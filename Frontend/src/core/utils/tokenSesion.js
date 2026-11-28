import { STORAGE_KEYS } from '../constants';

export const MENSAJE_SESION_EXPIRADA =
  'Tu sesión expiró. Vuelve a iniciar sesión.';

const listeners = new Set();
let motivoActual = null;

const notificar = (evento) => {
  listeners.forEach((fn) => fn(evento));
};

const leerPayload = (token) => {
  if (!token) return null;
  try {
    const segmento = token
      .split('.')[1]
      .replace(/-/g, '+')
      .replace(/_/g, '/');
    const relleno = segmento.padEnd(
      Math.ceil(segmento.length / 4) * 4,
      '='
    );
    return JSON.parse(atob(relleno));
  } catch {
    return null;
  }
};

export const leerExp = (token) =>
  leerPayload(token)?.exp ?? 0;

export const obtenerToken = () =>
  localStorage.getItem(STORAGE_KEYS.TOKEN);

export const tokenVigente = () =>
  leerExp(obtenerToken()) * 1000 > Date.now();

export const motivoSesion = () => motivoActual;

export const guardarToken = (token) => {
  if (leerExp(token) <= leerExp(obtenerToken())) return;
  localStorage.setItem(STORAGE_KEYS.TOKEN, token);
  motivoActual = null;
  notificar({ tipo: 'token', token });
};

export const limpiarSesion = ({
  motivo = null,
  borrarChat = false,
  userId = null,
} = {}) => {
  if (borrarChat && userId) {
    localStorage.removeItem(
      `${STORAGE_KEYS.CHAT_HISTORIAL}_${userId}`
    );
  }
  localStorage.removeItem(STORAGE_KEYS.USER);
  localStorage.removeItem(STORAGE_KEYS.TOKEN);
  motivoActual = motivo;
  notificar({ tipo: 'logout', motivo });
};

export const suscribirse = (fn) => {
  listeners.add(fn);
  return () => listeners.delete(fn);
};

export const redirigirAlLogin = (motivo = null) => {
  const url =
    motivo === 'expirada'
      ? '/login?sesion=expirada'
      : '/login';
  const actual =
    window.location.pathname + window.location.search;
  if (actual !== url) {
    window.location.assign(url);
  }
};
