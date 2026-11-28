import {
  obtenerToken,
  guardarToken,
  limpiarSesion,
  redirigirAlLogin,
} from '../utils/tokenSesion';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const CODIGOS_SESION_INVALIDA = ['CUENTA_BLOQUEADA', 'CUENTA_INACTIVA'];
const CODIGOS_TOKEN_INVALIDO = ['TOKEN_EXPIRADO', 'TOKEN_INVALIDO'];

const aplicarTokenRenovado = (res) => {
  const nuevo = res.headers.get('X-Token-Renovado');
  if (nuevo) guardarToken(nuevo);
};

const cerrarSesionInvalidada = (codigo) => {
  const motivo = CODIGOS_TOKEN_INVALIDO.includes(codigo)
    ? 'expirada'
    : null;
  if (
    !CODIGOS_SESION_INVALIDA.includes(codigo) &&
    motivo !== 'expirada'
  ) {
    return;
  }
  limpiarSesion({ motivo });
  redirigirAlLogin(motivo);
};

const lanzarErrorDeRespuesta = async (res) => {
  let cuerpo;
  let mensaje;
  try {
    cuerpo = await res.json();
    mensaje = cuerpo.message || cuerpo.detail || JSON.stringify(cuerpo);
  } catch {
    mensaje = await res.text();
  }
  if (cuerpo?.code) {
    cerrarSesionInvalidada(cuerpo.code);
  }
  const error = new Error(mensaje);
  error.status = res.status;
  if (cuerpo?.code) {
    error.code = cuerpo.code;
  }
  throw error;
};

export const apiClient = {
  get: async (endpoint, params = {}) => {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    const url = query ? `${BASE_URL}${endpoint}?${query}` : `${BASE_URL}${endpoint}`;
    const token = obtenerToken();
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    if (!res.ok) await lanzarErrorDeRespuesta(res);
    aplicarTokenRenovado(res);
    return res.json();
  },

  post: async (endpoint, body) => {
    const token = obtenerToken();
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) await lanzarErrorDeRespuesta(res);
    aplicarTokenRenovado(res);
    return res.json();
  },

  put: async (endpoint, body) => {
    const token = obtenerToken();
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) await lanzarErrorDeRespuesta(res);
    aplicarTokenRenovado(res);
    return res.json();
  },

  delete: async (endpoint) => {
    const token = obtenerToken();
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    if (!res.ok) await lanzarErrorDeRespuesta(res);
    aplicarTokenRenovado(res);
    return res.json();
  },

  getBlob: async (endpoint, params = {}) => {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
    ).toString();
    const url = query ? `${BASE_URL}${endpoint}?${query}` : `${BASE_URL}${endpoint}`;
    const token = obtenerToken();
    const res = await fetch(url, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    if (!res.ok) await lanzarErrorDeRespuesta(res);
    aplicarTokenRenovado(res);
    return res.blob();
  },
};
