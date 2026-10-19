import React from 'react';
import Modal from '../../../shared/components/Modal';

// HU-0037: se conserva el modal para cuando su backend quede disponible.
const ModalEliminarUsuario = ({ open, onClose, usuario, onConfirmar }) => (
  <Modal open={open} onClose={onClose} title="Eliminar usuario">
    <div className="formulario-modal">
      <p className="admin-texto-confirmacion">
        ¿Estás seguro de que quieres eliminar a <strong>{usuario?.nombre}</strong>?
        Esta acción no se puede deshacer.
      </p>
      <button type="button" className="admin-boton-peligro" onClick={onConfirmar}>
        Sí, eliminar
      </button>
      <button type="button" className="admin-boton-secundario" onClick={onClose}>
        Cancelar
      </button>
    </div>
  </Modal>
);

export default ModalEliminarUsuario;
