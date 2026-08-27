import { apiClient } from '../../../core/api/client';
import { authService } from '../../auth/services/authService';
import { transaccionesService } from '../../transacciones/services/transaccionesService';

export const metasService = {
  listar: () => apiClient.get('/ahorros/metas'),

  crear: ({ nombre, monto_objetivo, saldo_inicial, fecha_objetivo, id_categoria }) => {
    const datos = {
      nombre,
      monto_objetivo,
      fecha_objetivo,
      id_categoria,
    };
    if (saldo_inicial !== undefined && saldo_inicial !== null && saldo_inicial !== '') {
      datos.saldo_inicial = saldo_inicial;
    }
    return apiClient.post('/ahorros/metas', datos);
  },

  abonar: async ({ id_ahorro, monto, fecha, descripcion }) => {
    const { id_cuenta } = await authService.obtenerSaldo();
    return apiClient.post('/transacciones/ahorros', {
      monto,
      fecha,
      descripcion: descripcion || null,
      id_cuenta,
      id_ahorro,
    });
  },

  listarCategoriasAhorro: async () => {
    const categorias = await transaccionesService.listarCategorias();
    return categorias.filter((c) => c.tipo_categoria === 'AHORRO');
  },
};
