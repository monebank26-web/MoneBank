// features/transacciones/pages/TransaccionesPage.jsx
import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { bolsillosService } from '../../bolsillos/services/bolsillosService';
import './TransaccionesPage.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

const formatFecha = (iso) => {
  const d = new Date(iso);
  return d.toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
};

const TransaccionesPage = () => {
  const { user } = useAuth();
  const [transacciones, setTransacciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState('todos');

  const cargar = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      const data = await bolsillosService.historialTransacciones(user.id);
      setTransacciones(data);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => { cargar(); }, [cargar]);

  const filtradas = transacciones.filter((t) => filtro === 'todos' || t.tipo === filtro);

  return (
    <div className="pagina-movimientos">
      <div className="encabezado-pagina-movimientos">
        <h1 className="titulo-pagina">Movimientos</h1>
        <div className="filtros-movimientos">
          {['todos', 'transferencia', 'deposito'].map((f) => (
            <button key={f} className={`boton-filtro ${filtro === f ? 'boton-filtro--activo' : ''}`}
              onClick={() => setFiltro(f)}>
              {f === 'todos' ? 'Todos' : f === 'transferencia' ? 'Transferencias' : 'Depósitos'}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="cargando-pagina">Cargando movimientos...</p>
      ) : filtradas.length === 0 ? (
        <div className="movimientos-sin-contenido">
          <p>No hay movimientos{filtro !== 'todos' ? ' de este tipo' : ''} aún.</p>
        </div>
      ) : (
        <div className="lista-movimientos-completa">
          {filtradas.map((tx) => (
            <div key={tx.id} className="elemento-movimiento-completo">
              <div className={`icono-elemento-movimiento icono-movimiento--${tx.tipo}`}>
                {tx.tipo === 'transferencia' ? '↔' : '↓'}
              </div>
              <div className="informacion-elemento-movimiento">
                <p className="descripcion-elemento-movimiento">
                  {tx.tipo === 'transferencia'
                    ? `Transferencia: ${tx.origenNombre} → ${tx.destinoNombre}`
                    : `Depósito en ${tx.destinoNombre}`}
                </p>
                {tx.descripcion && <p className="nota-elemento-movimiento">"{tx.descripcion}"</p>}
                <p className="fecha-movimiento">{formatFecha(tx.fecha)}</p>
              </div>
              <div className="columna-derecha-movimiento">
                <p className={`monto-movimiento monto-movimiento--${tx.tipo}`}>
                  {tx.tipo === 'deposito' ? '+' : ''}{formatMoney(tx.monto)}
                </p>
                <span className={`etiqueta-tipo-movimiento etiqueta-tipo-movimiento--${tx.tipo}`}>
                  {tx.tipo === 'transferencia' ? 'Transferencia' : 'Depósito'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TransaccionesPage;
