import { apiClient } from '../../../core/api/client';

const BASE_URL = '/control-parental/dashboard';

export const mesadaService = {
  obtener: (idHijo) =>
    apiClient.get(`${BASE_URL}/hijos/${idHijo}/mesada`),

  crear: (idHijo, datos) =>
    apiClient.post(`${BASE_URL}/hijos/${idHijo}/mesada`, datos),

  ejecutar: (idHijo) =>
    apiClient.post(`${BASE_URL}/hijos/${idHijo}/mesada/ejecutar`),

  actualizar: (idHijo, datos) =>
    apiClient.put(`${BASE_URL}/hijos/${idHijo}/mesada`, datos),

  cancelar: (idHijo) =>
    apiClient.delete(`${BASE_URL}/hijos/${idHijo}/mesada`),
};
