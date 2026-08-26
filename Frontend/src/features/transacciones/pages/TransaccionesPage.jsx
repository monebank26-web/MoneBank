import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { transaccionesService } from '../services/transaccionesService';
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

  return (
    <div className="pagina-movimientos">
      <div className="encabezado-pagina-movimientos">
        <h1 className="titulo-pagina">Movimientos</h1>
        <span className="total-movimientos">{total} movimiento{total !== 1 ? 's' : ''}</span>
      </div>

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
      />
    </div>
  );
};export default TransaccionesPage;
