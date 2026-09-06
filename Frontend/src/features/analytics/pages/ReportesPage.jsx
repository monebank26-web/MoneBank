import React from 'react';
import { useReporte } from '../hooks/useReporte';
import { ReporteResumen } from '../components/ReporteResumen';
import { ReporteDetalleCategoria } from '../components/ReporteDetalleCategoria';
import { analyticsService } from '../services/analyticsService';
import '../styles/analytics-cards.css';

export const ReportesPage = () => {
  const { data, loading, error, recargar } = useReporte('mensual');

  const handleDescargarPDF = async () => {
    try {
      const blob = await analyticsService.descargarReportePDF('mensual');
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

  if (loading) {
    return <div style={{ padding: '24px', textAlign: 'center', color: 'var(--color-text)' }}>Generando reporte...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: '24px', color: 'var(--color-danger)' }}>
        <p>{error}</p>
        <button
          onClick={recargar}
          style={{
            marginTop: '12px',
            padding: '8px 16px',
            backgroundColor: 'var(--color-accent)',
            color: '#080808',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            fontWeight: 600,
          }}
        >
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '760px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.75rem', color: 'var(--color-text)' }}>
          Reporte Mensual
        </h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={handleDescargarPDF}
            style={{
              padding: '8px 16px',
              backgroundColor: 'var(--color-accent)',
              color: '#080808',
              border: 'none',
              borderRadius: 'var(--radius-sm)',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Descargar PDF
          </button>
          <button
            onClick={recargar}
            style={{
              padding: '8px 16px',
              backgroundColor: 'var(--color-surface-2)',
              color: 'var(--color-text)',
              border: '1px solid var(--color-border)',
              borderRadius: 'var(--radius-sm)',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Actualizar
          </button>
        </div>
      </div>

      <ReporteResumen data={data} />
      <ReporteDetalleCategoria detalle={data?.detalle_por_categoria} />
    </div>
  );
};

export default ReportesPage;