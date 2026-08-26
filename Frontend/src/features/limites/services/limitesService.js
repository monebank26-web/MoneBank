import { apiClient } from '../../../core/api/client';
import { transaccionesService } from '../../transacciones/services/transaccionesService';

export const limitesService = {
  listar: () => apiClient.get('/ahorros/limites'),

  crear: ({ nombre, monto_limite, periodo, id_categoria }) => {
    const datos = {
      monto_limite,
      periodo,
      id_categoria,
    };
    if (nombre && nombre.trim()) {
      datos.nombre = nombre.trim();
    }
    return apiClient.post('/ahorros/limites', datos);
  },

  alertas: () => apiClient.get('/ahorros/limites/alertas'),

  listarCategoriasGasto: async () => {
    const categorias = await transaccionesService.listarCategorias();
    return categorias.filter((c) => c.tipo_categoria === 'GASTO');
  },
};
