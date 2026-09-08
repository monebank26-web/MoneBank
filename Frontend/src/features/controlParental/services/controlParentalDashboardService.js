import { apiClient } from '../../../core/api/client';

const BASE_URL = '/control-parental/dashboard';

export const controlParentalDashboardService = {
  listarHijos: () =>
    apiClient.get(`${BASE_URL}/hijos`),

  obtenerResumen: (idHijo) =>
    apiClient.get(
      `${BASE_URL}/hijos/${idHijo}/resumen`
    ),

  obtenerTransacciones: (idHijo, limite = 20) =>
    apiClient.get(
      `${BASE_URL}/hijos/${idHijo}/transacciones`,
      { limite }
    ),

  obtenerPermisos: (idHijo) =>
    apiClient.get(
      `${BASE_URL}/hijos/${idHijo}/permisos`
    ),

  actualizarPermisos: (idHijo, permisos) =>
    apiClient.put(
      `${BASE_URL}/hijos/${idHijo}/permisos`,
      { permisos }
    ),
};
