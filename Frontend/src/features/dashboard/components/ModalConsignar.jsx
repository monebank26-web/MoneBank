import React from 'react';
import Modal from '../../../shared/components/Modal';
import { formatMoney } from '../../../core/utils/format';

const ModalConsignar = ({ open, onClose, saldoActual, monto, setMonto, error, onConsignar }) => {
  return (
    <Modal open={open} onClose={onClose} title="Consignar a Mi Cuenta">
      <div className="formulario-modal">
        <p style={{ color: 'var(--color-text-soft)', fontSize: '13px' }}>
          Saldo actual: <strong style={{ color: 'var(--color-accent)' }}>{formatMoney(saldoActual)}</strong>
        </p>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto a consignar (COP)</label>
          <input
            className="campo-entrada"
            type="number"
            placeholder="Ej: 300000"
            min="1000"
            step="1"
            value={monto}
            onChange={(e) => setMonto(e.target.value)}
          />
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={onConsignar}>
          Consignar
        </button>
      </div>
    </Modal>
  );
};

export default ModalConsignar;
