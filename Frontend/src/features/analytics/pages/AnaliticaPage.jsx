import React, { useState } from 'react';
import { useGraficas } from '../hooks/useGraficas';
import { useReporte } from '../hooks/useReporte';
import { analyticsService } from '../services/analyticsService';
import { useTheme } from '../../../core/context/ThemeContext';
import { GraficaIngresosGastos } from '../components/GraficaIngresosGastos';
import { GraficaCategoria } from '../components/GraficaCategoria';
import { ReporteResumen } from '../components/ReporteResumen';
import { ReporteDetalleCategoria } from '../components/ReporteDetalleCategoria';
import { GraficaMovimientos } from '../components/GraficaMovimientos';
import { ComparativoPeriodo } from '../components/ComparativoPeriodo';
import '../styles/AnaliticaPage.css';
import '../components/ComparativoPeriodo.css';

// SIMULACIÓN DEL PERIODO ANTERIOR (solo para validar lo visual de la HU-0081).
// 'con_datos' -> escenario 1 (comparativo normal)
// 'sin_datos' -> escenario 3 (aviso "no hay datos para comparar")
// Cuando el backend entregue el periodo anterior, se elimina esto.
const SIMULAR_ANTERIOR = 'con_datos';

const simularAnterior = (actual) => {
  if (SIMULAR_ANTERIOR === 'sin_datos') return null;
  return {
    ingresos: actual.ingresos * 0.9,
    gastos: actual.gastos * 1.1,
    balance: actual.balance * 0.8,
  };
};

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

  // Fechas que el usuario está escribiendo (borrador)
  const [inicioBorrador, setInicioBorrador] = useState('');
  const [finBorrador, setFinBorrador] = useState('');

  // Fechas ya aplicadas (las que usa el reporte)
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const [errorRango, setErrorRango] = useState('');

  const graficas = useGraficas();
  const reporte = useReporte('mensual', fechaInicio || undefined, fechaFin || undefined);

  const aplicarRango = () => {
    // Rango incompleto: solo una de las dos fechas
    if ((inicioBorrador && !finBorrador) || (!inicioBorrador && finBorrador)) {
      setErrorRango('Selecciona la fecha de inicio y la fecha de fin para aplicar el rango.');
      return;
    }

    // Rango inválido: inicio posterior a fin
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

  // Periodo actual: sale del mismo reporte que ya muestra ReporteResumen
  const actual = reporte.data
    ? {
        ingresos: Number(reporte.data.total_ingresos) || 0,
        gastos: Number(reporte.data.total_gastos) || 0,
        balance: Number(reporte.data.balance) || 0,
      }
    : null;

  const anterior = actual ? simularAnterior(actual) : null;
  const rangoAplicado = fechaInicio && fechaFin;
  const rangoAnterior = calcularRangoAnterior(fechaInicio, fechaFin);

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
              <input
                type="date"
                value={inicioBorrador}
                onChange={(e) => setInicioBorrador(e.target.value)}
                aria-label="Fecha inicio"
                aria-invalid={!!errorRango}
              />
              <span>–</span>
              <input
                type="date"
                value={finBorrador}
                onChange={(e) => setFinBorrador(e.target.value)}
                aria-label="Fecha fin"
                aria-invalid={!!errorRango}
              />
              <button className="an-btn" onClick={aplicarRango}>Aplicar</button>
              <button className="an-btn an-btn--ghost" onClick={limpiarFechas}>Limpiar</button>
              <button className="an-btn" onClick={handleDescargarPDF}>Descargar PDF</button>
            </div>
          )}
        </div>
      </header>

      {vista === 'reporte' && errorRango && (
        <p className="cmp-error" role="alert">{errorRango}</p>
      )}

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
          {rangoAplicado && actual && (
            <ComparativoPeriodo
              actual={actual}
              anterior={anterior}
              rangoAnterior={rangoAnterior}
            />
          )}
          <ReporteDetalleCategoria detalle={reporte.data?.detalle_por_categoria} />
        </Estado>
      )}
    </section>
  );
};

export default AnaliticaPage;