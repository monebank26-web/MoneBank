import React from 'react';
import { Icon } from '@iconify/react';
import Modal from '../../../shared/components/Modal';

// HU-0037: la interfaz habla de desactivar, aunque el servicio conserve
// el nombre `eliminarUsuario` para no romper la API existente.
const ModalEliminarUsuario = ({
  open,
  onClose,
  usuario,
  onConfirmar,
  error,
  desactivando,
}) => {
  const nombre = usuario?.nombre || usuario?.email || 'este usuario';

  return (
    <Modal open={open} onClose={onClose} title="Desactivar usuario">
      <div className="formulario-modal">
        <div className="admin-modal-icono admin-modal-icono--peligro">
          <Icon icon="mdi:account-off-outline" />
        </div>

        <p className="admin-texto-confirmacion">
          La cuenta de <strong>{nombre}</strong> pasará a estado{' '}
          <strong>Inactivo</strong> y no podrá iniciar sesión. Sus datos no se eliminarán.
        </p>

        {usuario?.estado === 'BLOQUEADO' && (
          <p className="admin-modal-nota">
            <Icon icon="mdi:information-outline" />
            La cuenta está bloqueada; al desactivarla quedará inactiva.
          </p>
        )}

        {error && (
          <div className="error-formulario" role="alert">
            {error}
          </div>
        )}

        <button
          type="button"
          className="admin-boton-peligro"
          onClick={onConfirmar}
          disabled={desactivando}
        >
          <Icon icon={desactivando ? 'mdi:loading' : 'mdi:account-off-outline'} />
          {desactivando ? 'Desactivando...' : 'Desactivar cuenta'}
        </button>

        <button
          type="button"
          className="admin-boton-secundario"
          onClick={onClose}
          disabled={desactivando}
        >
          Cancelar
        </button>
      </div>
    </Modal>
  );
};

export default ModalEliminarUsuario;
