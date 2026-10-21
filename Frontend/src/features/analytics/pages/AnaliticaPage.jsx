import React, { useState } from 'react';
import { useGraficas } from '../hooks/useGraficas';
import { useReporte } from '../hooks/useReporte';
import { analyticsService } from '../services/analyticsService';
import { useTheme } from '../../../core/context/ThemeContext';
import { GraficaIngresosGastos } from '../components/GraficaIngresosGastos';
import { GraficaCategoria } from '../components/GraficaCategoria';
import { ReporteResumen } from '../components/ReporteResumen';
import { ReporteDetalleCategoria } from '../components/ReporteDetalleCategoria';
import { GraficaGastosPorCategoria, GraficaMovimientos } from '../components/GraficaMovimientos';
import '../styles/AnaliticaPage.css';

const Estado = ({ loading, error, onRetry, children }) => {
  if (loading) return <p className="an-estado">Cargando datos…</p>;
  if (error) {
    return (
      <div className="an-estado an-error">
        <p>{error}</p>
        <button className="an-btn" onClick={onRetry}>Reintentar</button>
      </div>
    );
  }
  return children;
};

export const AnaliticaPage = () => {
  const { theme } = useTheme();
  const [vista, setVista] = useState('graficas'); // 'graficas' | 'reporte'
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const graficas = useGraficas();
  const reporte = useReporte('mensual', fechaInicio || undefined, fechaFin || undefined);

  const handleDescargarPDF = async () => {
    try {
      const blob = await analyticsService.descargarReportePDF(
        'mensual', fechaInicio || undefined, fechaFin || undefined
      );
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `reporte_${reporte.data?.periodo_inicio}_${reporte.data?.periodo_fin}.pdf`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('No se pudo descargar el reporte: ' + err.message);
    }
  };

  return (
    <section className={`an-page ${theme === 'dark' ? 'an-dark' : 'an-light'}`}>
      <header className="an-head">
        <div>
          <h1>Analítica y reportes</h1>
          <p className="an-muted">Seguimiento de ingresos, gastos y salud financiera por periodo.</p>
        </div>
        <div className="an-controls">
          <div className="an-tabs" role="tablist">
            <button role="tab" aria-selected={vista === 'graficas'} onClick={() => setVista('graficas')}>
              Gráficas financieras
            </button>
            <button role="tab" aria-selected={vista === 'reporte'} onClick={() => setVista('reporte')}>
              Reporte mensual
            </button>
          </div>
          {vista === 'reporte' && (
            <div className="an-range">
              <input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} aria-label="Fecha inicio" />
              <span>–</span>
              <input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} aria-label="Fecha fin" />
              <button className="an-btn an-btn--ghost" onClick={() => { setFechaInicio(''); setFechaFin(''); }}>Limpiar</button>
              <button className="an-btn" onClick={handleDescargarPDF}>Descargar PDF</button>
            </div>
          )}
        </div>
      </header>
        {vista === 'graficas' ? (
          <Estado loading={graficas.loading} error={graficas.error} onRetry={graficas.recargar}>
            <GraficaIngresosGastos data={graficas.data?.series} />
          <div className="an-grid2">
            <GraficaCategoria data={graficas.data?.totales_por_categoria} />
            <GraficaMovimientos data={graficas.data?.totales_por_categoria} />
          </div>
          </Estado>
        ) : (
        <Estado loading={reporte.loading} error={reporte.error} onRetry={reporte.recargar}>
          <ReporteResumen data={reporte.data} />
          <ReporteDetalleCategoria detalle={reporte.data?.detalle_por_categoria} />
        </Estado>
      )}
    </section>
  );
};

export default AnaliticaPage;
