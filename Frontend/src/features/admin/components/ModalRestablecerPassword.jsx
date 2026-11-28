import React from 'react';
import { Icon } from '@iconify/react';
import ModalConfirmacionAdmin from './ModalConfirmacionAdmin';
import { etiquetaRolAdmin } from '../utils/usuariosAdmin';

const ModalRestablecerPassword = ({
  open,
  onClose,
  usuario,
  onConfirmar,
  error,
  restableciendo,
}) => {
  const nombre = usuario?.nombre || usuario?.email || 'este usuario';
  const rol = etiquetaRolAdmin(usuario?.rol) || 'Usuario';

  return (
    <ModalConfirmacionAdmin
      open={open}
      onClose={onClose}
      onConfirm={onConfirmar}
      title="Restablecer contraseña"
      icono="mdi:lock-reset"
      variante="primario"
      iconoConfirmar="mdi:email-outline"
      textoConfirmar="Enviar código"
      textoEnviando="Enviando..."
      error={error}
      enviando={restableciendo}
      className="caja-modal--admin-restablecer"
    >
      <div className="admin-modal-usuario">
        <span className="admin-modal-usuario__avatar">
          {(usuario?.nombres || usuario?.email || '?').charAt(0).toUpperCase()}
        </span>
        <div className="admin-modal-usuario__datos">
          <div className="admin-modal-usuario__identidad">
            <strong>{nombre}</strong>
            <span className="admin-modal-usuario__rol">{rol}</span>
          </div>
          <span>{usuario?.email}</span>
        </div>
      </div>

      <p className="admin-modal-texto admin-modal-texto--restablecer">
        Se enviará un código de 6 dígitos al correo del usuario. Su contraseña
        actual seguirá funcionando hasta que lo use.
      </p>
      <p className="admin-modal-subtexto">
        Si la cuenta puede estar comprometida, bloquéala primero.
      </p>

      <p className="admin-modal-aviso">
        <Icon icon="mdi:information-outline" aria-hidden="true" />
        Esta acción no desbloquea ni reactiva la cuenta automáticamente.
      </p>
    </ModalConfirmacionAdmin>
  );
};

export default ModalRestablecerPassword;
