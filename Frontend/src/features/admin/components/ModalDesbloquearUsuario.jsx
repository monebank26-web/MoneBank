import React from 'react';
import ModalConfirmacionAdmin from './ModalConfirmacionAdmin';
import {
  ACCION_REACTIVAR,
  accionCuentaAdmin,
  textoConfirmacionDesbloqueo,
} from '../utils/usuariosAdmin';

const ModalDesbloquearUsuario = ({
  open,
  onClose,
  usuario,
  onConfirmar,
  error,
  desbloqueando,
}) => {
  const accion = accionCuentaAdmin(usuario);
  const esReactivar = accion === ACCION_REACTIVAR;
  const icono = esReactivar ? 'mdi:account-check-outline' : 'mdi:lock-open-outline';

  return (
    <ModalConfirmacionAdmin
      open={open}
      onClose={onClose}
      onConfirm={onConfirmar}
      title={esReactivar ? 'Reactivar cuenta' : 'Desbloquear cuenta'}
      icono={icono}
      variante="primario"
      iconoConfirmar={icono}
      textoConfirmar={esReactivar ? 'Reactivar' : 'Desbloquear'}
      textoEnviando={esReactivar ? 'Reactivando...' : 'Desbloqueando...'}
      error={error}
      enviando={desbloqueando}
    >
      <p className="admin-modal-texto">{textoConfirmacionDesbloqueo(usuario)}</p>
    </ModalConfirmacionAdmin>
  );
};

export default ModalDesbloquearUsuario;
