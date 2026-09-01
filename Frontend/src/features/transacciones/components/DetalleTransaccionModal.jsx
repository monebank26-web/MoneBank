import React, { useEffect, useState } from 'react';
import Modal from '../../../shared/components/Modal';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';
import { transaccionesService } from '../services/transaccionesService';
import './DetalleTransaccionModal.css';

const DetalleTransaccionModal = ({ open, transaccionId, onClose }) => {
  const [detalle, setDetalle] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!open || !transaccionId) return;
    setCargando(true);
    setError('');
    setDetalle(null);
    transaccionesService.obtenerDetalle(transaccionId)
      .then(setDetalle)
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }, [open, transaccionId]);

  const tipo = detalle?.tipo_transaccion;

  return (
    <Modal open={open} onClose={onClose} title="Detalle de transacción">
      {cargando && <p className="detalle-mensaje">Cargando...</p>}
      {error && <p className="detalle-mensaje detalle-mensaje--error">{error}</p>}
      {detalle && (
        <div className="detalle-transaccion">
          {/* Tipo + monto grande */}
          <div className={`detalle-transaccion__hero detalle-transaccion__hero--${tipo?.toLowerCase()}`}>
            <span className="detalle-transaccion__hero-icono">
              {tipo === 'GASTO' ? '↓' : tipo === 'INGRESO' ? '↑' : '→'}
            </span>
            <p className="detalle-transaccion__hero-tipo">
              {tipo === 'GASTO' ? 'Gasto' : tipo === 'INGRESO' ? 'Ingreso' : 'Ahorro'}
            </p>
            <p className="detalle-transaccion__hero-monto">{formatMoney(detalle.monto)}</p>
          </div>

          {/* Filas de detalle */}
          <div className="detalle-transaccion__filas">
            <div className="detalle-transaccion__fila">
              <span className="detalle-transaccion__fila-label">Fecha</span>
              <span className="detalle-transaccion__fila-valor">{formatFechaConHora(detalle.fecha)}</span>
            </div>
            <div className="detalle-transaccion__fila">
              <span className="detalle-transaccion__fila-label">Estado</span>
              <span className="detalle-transaccion__fila-valor">{detalle.estado_transaccion}</span>
            </div>
            <div className="detalle-transaccion__fila">
              <span className="detalle-transaccion__fila-label">Categoría</span>
              <span className="detalle-transaccion__fila-valor">{detalle.nombre_categoria}</span>
            </div>
            {detalle.descripcion && (
              <div className="detalle-transaccion__fila">
                <span className="detalle-transaccion__fila-label">Descripción</span>
                <span className="detalle-transaccion__fila-valor">{detalle.descripcion}</span>
              </div>
            )}
            {detalle.nombre_ahorro && (
              <div className="detalle-transaccion__fila">
                <span className="detalle-transaccion__fila-label">Ahorro asociado</span>
                <span className="detalle-transaccion__fila-valor">{detalle.nombre_ahorro}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
};

export default DetalleTransaccionModal;