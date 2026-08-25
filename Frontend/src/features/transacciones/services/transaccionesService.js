import { apiClient } from '../../../core/api/client';

export const transaccionesService = {
  listarCategorias: () => apiClient.get('/transacciones/categorias'),

  registrarGasto: ({ monto, descripcion, id_cuenta, id_categoria }) =>
    apiClient.post('/transacciones/gastos', {
      monto,
      fecha: new Date().toISOString().split('T')[0],
      descripcion: descripcion || null,
      id_cuenta,
      id_categoria,
    }),
};
