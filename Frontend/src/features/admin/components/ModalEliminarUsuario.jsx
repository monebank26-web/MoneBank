import React from 'react';
import Modal from '../../../shared/components/Modal';

const ModalEliminarUsuario = ({ open, onClose, usuario, onConfirmar }) => {
  return (
    <Modal open={open} onClose={onClose} title="Eliminar usuario">
      <div className="formulario-modal">
        <p style={{ color: 'var(--color-text-soft)', marginBottom: '1rem', textAlign: 'center' }}>
          ¿Estás seguro de que quieres eliminar a <strong style={{ color: 'var(--color-text)' }}>{usuario?.nombre}</strong>?
          Esta acción no se puede deshacer.
        </p>
        <button className="boton-peligro" onClick={onConfirmar}>Sí, eliminar</button>
        <button className="boton-secundario" onClick={onClose} style={{ marginTop: '8px' }}>Cancelar</button>
      </div>
    </Modal>
  );
};

export default ModalEliminarUsuario;
