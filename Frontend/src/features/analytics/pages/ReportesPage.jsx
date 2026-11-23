import React, { useState } from 'react';
import { useReporte } from '../hooks/useReporte';
import { ReporteResumen } from '../components/ReporteResumen';
import { ReporteDetalleCategoria } from '../components/ReporteDetalleCategoria';
import { ComparativoPeriodo } from '../components/ComparativoPeriodo';
import { analyticsService } from '../services/analyticsService';
import '../../../features/transacciones/components/FiltrosHistorial.css';
import '../styles/analytics-cards.css';
import '../styles/ReportesPage.css';

// DATOS DE PRUEBA (solo para validar lo visual de la HU-0081).
// Para ver el escenario 3 (sin datos), pon MOCK_ANTERIOR = null.
const MOCK_ACTUAL = { ingresos: 2500000, gastos: 1800000, balance: 700000 };
const MOCK_ANTERIOR = { ingresos: 2300000, gastos: 2100000, balance: 200000 };

const formatearFecha = (d) =>
  d.toISOString().slice(0, 10).split('-').reverse().join('/');

const calcularRangoAnterior = (inicio, fin) => {
  if (!inicio || !fin) return null;
  const DIA = 24 * 60 * 60 * 1000;
  const ini = new Date(inicio + 'T00:00:00Z');
  const f = new Date(fin + 'T00:00:00Z');
  const dias = Math.round((f - ini) / DIA) + 1;
  const finAnterior = new Date(ini.getTime() - DIA);
  const iniAnterior = new Date(finAnterior.getTime() - (dias - 1) * DIA);
  return {
    inicio: formatearFecha(iniAnterior),
    fin: formatearFecha(finAnterior),
  };
};

export const ReportesPage = () => {
  // Fechas que el usuario está escribiendo (borrador)
  const [inicioBorrador, setInicioBorrador] = useState('');
  const [finBorrador, setFinBorrador] = useState('');

  // Fechas ya aplicadas (las que usa el reporte)
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const [errorRango, setErrorRango] = useState('');

  const { data, loading, error, recargar } = useReporte(
    'mensual',
    fechaInicio || undefined,
    fechaFin || undefined
  );

  const aplicarRango = () => {
    if (inicioBorrador && finBorrador && inicioBorrador > finBorrador) {
      setErrorRango(
        'El rango no es válido: la fecha de inicio no puede ser posterior a la fecha de fin.'
      );
      return;
    }
    setErrorRango('');
    setFechaInicio(inicioBorrador);
    setFechaFin(finBorrador);
  };

  const limpiarFechas = () => {
    setInicioBorrador('');
    setFinBorrador('');
    setFechaInicio('');
    setFechaFin('');
    setErrorRango('');
  };

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

  const rangoAplicado = fechaInicio && fechaFin;
  const rangoAnterior = calcularRangoAnterior(fechaInicio, fechaFin);

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
            <span>Rango de análisis</span>
            <div className="grupo-rango">
              <input
                type="date"
                value={inicioBorrador}
                onChange={(e) => setInicioBorrador(e.target.value)}
                aria-label="Fecha inicio"
                aria-invalid={!!errorRango}
              />
              <span className="grupo-rango__conector">–</span>
              <input
                type="date"
                value={finBorrador}
                onChange={(e) => setFinBorrador(e.target.value)}
                aria-label="Fecha fin"
                aria-invalid={!!errorRango}
              />
            </div>
          </div>

          <button className="boton-principal-pequeno" onClick={aplicarRango}>
            Aplicar
          </button>
          <button className="filtros-historial__limpiar" onClick={limpiarFechas}>
            Limpiar
          </button>
        </div>

        {errorRango && (
          <p className="rango-error" role="alert">
            {errorRango}
          </p>
        )}
      </div>

      <ReporteResumen data={data} />

      {rangoAplicado && (
        <ComparativoPeriodo
          actual={MOCK_ACTUAL}
          anterior={MOCK_ANTERIOR}
          rangoAnterior={rangoAnterior}
        />
      )}

      <ReporteDetalleCategoria detalle={data?.detalle_por_categoria} />
    </div>
  );
};

export default ReportesPage;