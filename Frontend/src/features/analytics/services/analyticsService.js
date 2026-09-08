import { apiClient as api } from '../../../core/api/client';

export const analyticsService = {
  getGraficas: async () => {
    const response = await api.get('/analitica/graficas');
    return response;
  },

  getResumenSemanal: async (fechaInicio, fechaFin) => {
    const params = {};
    if (fechaInicio) params.fecha_inicio = fechaInicio;
    if (fechaFin) params.fecha_fin = fechaFin;
    const response = await api.get('/analitica/resumen-semanal', params);
    return response;
  },

  getReporte: async (periodo = 'mensual', fechaInicio, fechaFin) => {
    const params = { periodo };
    if (fechaInicio) params.fecha_inicio = fechaInicio;
    if (fechaFin) params.fecha_fin = fechaFin;
    const response = await api.get('/analitica/reportes', params);
    return response;
  },

  descargarReportePDF: async (periodo = 'mensual', fechaInicio, fechaFin) => {
    const params = { periodo };
    if (fechaInicio) params.fecha_inicio = fechaInicio;
    if (fechaFin) params.fecha_fin = fechaFin;
    return await api.getBlob('/analitica/reportes/pdf', params);
  }
};