import { apiClient } from '../../../core/api/client';

const ROLES_MAP = { 1: 'administrador', 2: 'normal' };

const toFrontend = (u) => ({
  id: u.id_usuario,
  nombres: u.nombres,
  apellidos: u.apellidos,
  email: u.correo,
  rol: ROLES_MAP[u.id_rol] || 'normal',
});

export const authService = {
  login: async ({ email, password }) => {
    const data = await apiClient.post('/auth/login', {
      correo: email,
      contrasena: password,
    });
    return {
      id: data.usuario_id,
      nombres: data.nombres,
      apellidos: data.apellidos,
      email: data.correo,
      rol: ROLES_MAP[data.id_rol] || 'normal',
      access_token: data.access_token,
    };
  },

  register: async ({ nombres, apellidos, email, password }) => {
    const data = await apiClient.post('/usuarios/', {
      nombres,
      apellidos,
      correo: email,
      contrasena: password,
    });
    return toFrontend(data);
  },

  obtenerUsuarioPorId: async (id) => {
    const data = await apiClient.get(`/usuarios/${id}`);
    return toFrontend(data);
  },

  obtenerTodosLosUsuarios: async () => {
    const data = await apiClient.get('/usuarios/');
    return Array.isArray(data) ? data.map(toFrontend) : [];
  },

  eliminarUsuario: async (id) => {
    return apiClient.delete(`/usuarios/${id}`);
  },

  actualizarUsuario: async (id, datos) => {
    const payload = {};
    if (datos.nombres !== undefined) payload.nombres = datos.nombres;
    if (datos.apellidos !== undefined) payload.apellidos = datos.apellidos;
    if (datos.email !== undefined) payload.correo = datos.email;
    const data = await apiClient.put(`/usuarios/${id}`, payload);
    return toFrontend(data);
  },

  cambiarPassword: async (contrasenaActual, contrasenaNueva) => {
    return apiClient.post('/auth/cambiar-password', {
      contrasena_actual: contrasenaActual,
      contrasena_nueva: contrasenaNueva,
    });
  },

  obtenerSaldo: async () => {
    const data = await apiClient.get('/cuentas/');
    const cuentas = Array.isArray(data) ? data : [];
    const cuenta = cuentas.find((c) => c.estado === 'ACTIVA') || cuentas[0];
    return cuenta
      ? { saldo: parseFloat(cuenta.saldo), id_cuenta: cuenta.id_cuenta }
      : { saldo: 0, id_cuenta: null };
  },

  registrarGasto: async ({ monto, descripcion, id_cuenta, id_categoria = 3, id_tipo_transaccion = 1 }) => {
    return apiClient.post('/transacciones/gastos', {
      monto,
      fecha: new Date().toISOString().split('T')[0],
      descripcion: descripcion || null,
      id_tipo_transaccion,
      id_cuenta,
      id_categoria,
    });
  },
};
