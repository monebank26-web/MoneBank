import { apiClient } from '../../../core/api/client';

export const controlParentalService = {
  solicitarVinculacion: ({ correoHijo, nombreHijo }) => {
    return apiClient.post('/control-parental/vinculaciones', {
      correo_hijo: correoHijo,
      nombre_hijo: nombreHijo,
    });
  },

  confirmarVinculacion: (codigo) => {
    return apiClient.post('/control-parental/vinculaciones/confirmar', {
      codigo,
    });
  },

  obtenerVinculaciones: () => {
    return apiClient.get('/control-parental/vinculaciones');
  },

  solicitarDesvinculacion: (correoPadre) => {
    return apiClient.post('/control-parental/desvinculaciones', {
      correo_padre: correoPadre,
    });
  },

  confirmarDesvinculacion: (codigo) => {
    return apiClient.post('/control-parental/desvinculaciones/confirmar', {
      codigo,
    });
  },
};
