import { apiClient } from '../../../core/api/client';

export const transaccionesService = {
  listarCategorias: () => apiClient.get('/transacciones/categorias'),

  obtenerHistorial: (params = {}) =>
    apiClient.get('/transacciones/historial', params),
  
  obtenerDetalle: (id) =>
    apiClient.get(`/transacciones/${id}`),
  
  registrarGasto: ({ monto, descripcion, id_cuenta, id_categoria }) =>
    apiClient.post('/transacciones/gastos', {
      monto,
      fecha: new Date().toISOString().split('T')[0],
      descripcion: descripcion || null,
      id_cuenta,
      id_categoria,
    }),

     registrarAbonoAhorro: ({ monto, descripcion, id_cuenta, id_ahorro }) =>
    apiClient.post('/transacciones/ahorros', {
      monto,
      fecha: new Date().toISOString().split('T')[0],
      descripcion: descripcion || null,
      id_cuenta,
      id_ahorro,
    }),
};

