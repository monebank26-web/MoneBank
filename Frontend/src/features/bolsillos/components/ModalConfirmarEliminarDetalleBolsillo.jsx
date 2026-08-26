import React from 'react';
import Modal from '../../../shared/components/Modal';
import { formatMoney } from '../../../core/utils/format';

const ModalConfirmarEliminarDetalleBolsillo = ({ open, onClose, bolsillo, onConfirmar }) => {
  return (
    <Modal open={open} onClose={onClose} title="Eliminar bolsillo">
      <div className="formulario-modal">
        <p style={{ color: 'var(--color-text-soft)', fontSize: '14px', marginBottom: '20px' }}>
          ¿Estás seguro de eliminar <strong style={{ color: 'var(--color-text)' }}>{bolsillo.nombre}</strong>?
          {bolsillo.saldo > 0 && (
            <span style={{ color: 'var(--color-warning)', display: 'block', marginTop: '8px' }}>
              Este bolsillo tiene {formatMoney(bolsillo.saldo)} en saldo, que volverá a Mi Cuenta.
            </span>
          )}
        </p>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="boton-secundario" style={{ flex: 1 }} onClick={onClose}>Cancelar</button>
          <button className="boton-peligro" style={{ flex: 1 }} onClick={onConfirmar}>Eliminar</button>
        </div>
      </div>
    </Modal>
  );
};

export default ModalConfirmarEliminarDetalleBolsillo;
