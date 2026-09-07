import { apiClient } from '../../../core/api/client';

export const consejoIaService = {
  obtenerConsejoPrevio: (monto, idCategoria) =>
    apiClient.post('/analitica/consejo-previo', { monto, id_categoria: idCategoria }),
};
