import { apiClient } from '../../../core/api/client';

export const authService = {

  login: async ({ email, password }) => {

    return await apiClient.post(
      '/usuarios/login',
      {
        correo: email,
        contrasena: password
      }
    );

  },

  register: async ({ nombre, email, password }) => {

    const partes = nombre.trim().split(' ');

    const nombres = partes[0];
    const apellidos =
      partes.length > 1
        ? partes.slice(1).join(' ')
        : 'Sin apellido';

    return await apiClient.post(
      '/usuarios/',
      {
        nombres,
        apellidos,
        correo: email,
        contrasena: password,
        estado: 'ACTIVO',
        id_rol: 1,
        id_tipo_usuario: 1
      }
    );
  }

};