import React from 'react';
import { Icon } from '@iconify/react';
import ModalConfirmacionAdmin from './ModalConfirmacionAdmin';

const ModalRestablecerPassword = ({
  open,
  onClose,
  usuario,
  onConfirmar,
  error,
  restableciendo,
}) => {
  const nombre = usuario?.nombre || usuario?.email || 'este usuario';
  const cuentaSinAcceso = ['BLOQUEADO', 'INACTIVO'].includes(usuario?.estado);

  return (
    <ModalConfirmacionAdmin
      open={open}
      onClose={onClose}
      onConfirm={onConfirmar}
      title="Restablecer contraseña"
      icono="mdi:lock-reset"
      variante="primario"
      iconoConfirmar="mdi:email-fast-outline"
      textoConfirmar="Enviar código"
      textoEnviando="Enviando..."
      error={error}
      enviando={restableciendo}
    >
      <div className="admin-modal-usuario">
        <span className="admin-modal-usuario__avatar">
          {(usuario?.nombres || usuario?.email || '?').charAt(0).toUpperCase()}
        </span>
        <div className="admin-modal-usuario__datos">
          <strong>{nombre}</strong>
          <span>{usuario?.email}</span>
        </div>
      </div>

      <p className="admin-modal-texto">
        Se enviará un código de 6 dígitos al correo del usuario. Su contraseña
        actual seguirá funcionando hasta que lo use. Si la cuenta puede estar
        comprometida, bloquéala primero.
      </p>

      {cuentaSinAcceso && (
        <p className="admin-modal-aviso">
          <Icon icon="mdi:information-outline" aria-hidden="true" />
          Esta acción no desbloquea ni reactiva la cuenta.
        </p>
      )}
    </ModalConfirmacionAdmin>
  );
};

export default ModalRestablecerPassword;
