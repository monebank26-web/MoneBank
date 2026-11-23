import React from 'react';
import { Icon } from '@iconify/react';
import Modal from '../../../shared/components/Modal';

const ModalConfirmacionAdmin = ({
  open,
  onClose,
  onConfirm,
  title,
  icono,
  variante = 'peligro',
  iconoConfirmar = 'mdi:check-circle-outline',
  textoConfirmar,
  textoEnviando,
  error,
  enviando = false,
  children,
}) => {
  const claseBoton =
    variante === 'primario' ? 'admin-boton-primario' : 'admin-boton-peligro';
  const cerrar = enviando ? () => {} : onClose;

  const confirmar = (event) => {
    event.preventDefault();
    if (!enviando) onConfirm?.();
  };

  return (
    <Modal open={open} onClose={cerrar} title={title}>
      <form className="formulario-modal admin-confirmacion" onSubmit={confirmar}>
        <div
          className={`admin-modal-icono admin-modal-icono--${variante}`}
          aria-hidden="true"
        >
          <Icon icon={icono} aria-hidden="true" />
        </div>

        {children}

        {error && (
          <div className="error-formulario" role="alert">
            {error}
          </div>
        )}

        <button
          type="submit"
          className={`${claseBoton} admin-boton-confirmar`}
          disabled={enviando}
          aria-busy={enviando}
        >
          <Icon
            icon={enviando ? 'mdi:loading' : iconoConfirmar}
            aria-hidden="true"
          />
          {enviando ? textoEnviando : textoConfirmar}
        </button>

        <button
          type="button"
          className="admin-boton-secundario"
          onClick={onClose}
          disabled={enviando}
        >
          Cancelar
        </button>
      </form>
    </Modal>
  );
};

export default ModalConfirmacionAdmin;
