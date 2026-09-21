import React, { useState } from 'react';
import { useReporte } from '../hooks/useReporte';
import { ReporteResumen } from '../components/ReporteResumen';
import { ReporteDetalleCategoria } from '../components/ReporteDetalleCategoria';
import { analyticsService } from '../services/analyticsService';
import '../../../features/transacciones/components/FiltrosHistorial.css';
import '../styles/analytics-cards.css';
import '../styles/ReportesPage.css';

export const ReportesPage = () => {
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const { data, loading, error, recargar } = useReporte(
    'mensual',
    fechaInicio || undefined,
    fechaFin || undefined
  );

  const handleDescargarPDF = async () => {
    try {
      const blob = await analyticsService.descargarReportePDF(
        'mensual',
        fechaInicio || undefined,
        fechaFin || undefined
      );
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `reporte_${data?.periodo_inicio}_${data?.periodo_fin}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('No se pudo descargar el reporte: ' + err.message);
    }
  };

  const limpiarFechas = () => {
    setFechaInicio('');
    setFechaFin('');
  };

  if (loading) {
    return <p className="cargando-pagina">Generando reporte...</p>;
  }

  if (error) {
    return (
      <div className="reportes-error">
        <p>{error}</p>
        <button className="boton-principal-pequeno" onClick={recargar}>
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="pagina-reportes">
      <div className="encabezado-pagina-reportes">
        <h1 className="titulo-pagina">Reporte Financiero</h1>
        <button className="boton-principal-pequeno" onClick={handleDescargarPDF}>
          Descargar PDF
        </button>
      </div>

      <div className="filtros-historial">
        <div className="filtros-historial__grid">
          <div className="filtros-historial__campo">
            <span>Fecha</span>
            <div className="grupo-rango">
              <input
                type="date"
                value={fechaInicio}
                onChange={(e) => setFechaInicio(e.target.value)}
                aria-label="Fecha inicio"
              />
              <span className="grupo-rango__conector">–</span>
              <input
                type="date"
                value={fechaFin}
                onChange={(e) => setFechaFin(e.target.value)}
                aria-label="Fecha fin"
              />
            </div>
          </div>

          <button className="filtros-historial__limpiar" onClick={limpiarFechas}>
            Limpiar
          </button>
        </div>
      </div>

      <ReporteResumen data={data} />
      <ReporteDetalleCategoria detalle={data?.detalle_por_categoria} />
    </div>
  );
};

export default ReportesPage;