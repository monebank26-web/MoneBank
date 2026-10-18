import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { fechaLocalHoy } from '../../../core/utils/fechaLocal';
import { transaccionesService } from '../services/transaccionesService';
import { useReporte } from '../../analytics/hooks/useReporte';
import { ReporteResumen } from '../../analytics/components/ReporteResumen';
import '../../analytics/styles/analytics-cards.css';
import TransaccionCard from '../components/TransaccionCard';
import DetalleTransaccionModal from '../components/DetalleTransaccionModal';
import FiltrosHistorial from '../components/FiltrosHistorial';
import Paginacion from '../components/Paginacion';
import './TransaccionesPage.css';

const TransaccionesPage = () => {
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [pagina, setPagina] = useState(1);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [loading, setLoading] = useState(true);
  const [filtros, setFiltros] = useState({
    pagina: 1, ordenar_por: 'fecha', orden: 'desc'
  });
  const [categorias, setCategorias] = useState([]);
  const [detalleId, setDetalleId] = useState(null);

  const hoy = fechaLocalHoy();
  const inicioMes = `${hoy.slice(0, 7)}-01`;
  const { data: reporte, loading: reporteLoading, error: reporteError, recargar: recargarReporte } = useReporte('mensual', inicioMes, hoy);

  // Cargar categorías una vez
  useEffect(() => {
    transaccionesService.listarCategorias().then(setCategorias).catch(() => {});
  }, []);

  // Cargar historial cada vez que cambian los filtros
  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const data = await transaccionesService.obtenerHistorial(filtros);
      setItems(data.items || []);
      setTotal(data.total || 0);
      setPagina(data.pagina || 1);
      setTotalPaginas(data.total_paginas || 1);
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [filtros]);

  useEffect(() => { cargar(); }, [cargar]);

  const handleFiltrar = (nuevosFiltros) => {
    setFiltros(nuevosFiltros);
  };

  const handlePagina = (nuevaPagina) => {
    setFiltros((prev) => ({ ...prev, pagina: nuevaPagina }));
  };

  const handleActualizado = () => {
    cargar();
    recargarReporte();
  };

  return (
    <div className="pagina-movimientos">
      <div className="encabezado-pagina-movimientos">
        <h1 className="titulo-pagina">Movimientos</h1>
        <span className="total-movimientos">{total} movimiento{total !== 1 ? 's' : ''}</span>
      </div>

      { reporteLoading ? (
        <p className="cargando-pagina">Cargando resumen del mes...</p>
      ) : reporteError ? (
        <p className="movimientos-sin-contenido">{reporteError}</p>
      ) : (
        <ReporteResumen data={reporte} titulo="Balance mensual" />
      )}

      <FiltrosHistorial onFiltrar={handleFiltrar} categorias={categorias} />

      {loading ? (
        <p className="cargando-pagina">Cargando movimientos...</p>
      ) : items.length === 0 ? (
        <div className="movimientos-sin-contenido">
          <p>No hay movimientos con estos filtros.</p>
        </div>
      ) : (
        <>
          <div className="lista-movimientos-completa">
            {items.map((tx) => (
              <TransaccionCard
                key={tx.id_transaccion}
                transaccion={tx}
                onDetalle={(t) => setDetalleId(t.id_transaccion)}
              />
            ))}
          </div>

          <Paginacion
            pagina={pagina}
            totalPaginas={totalPaginas}
            onChange={handlePagina}
          />
        </>
      )}

      <DetalleTransaccionModal
        open={detalleId !== null}
        transaccionId={detalleId}
        onClose={() => setDetalleId(null)}
        categorias={categorias}
        onActualizado={handleActualizado}
      />
    </div>
  );
};export default TransaccionesPage;
