import React from 'react';
import { Icon } from '@iconify/react';
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
  const esBloqueado = usuario?.estado === 'BLOQUEADO';
  const titulo = esReactivar ? 'Reactivar cuenta' : 'Desbloquear cuenta';
  const icono = esReactivar ? 'mdi:account-check-outline' : 'mdi:lock-open-outline';
  const textoOriginal = textoConfirmacionDesbloqueo(usuario);
  const texto = esBloqueado
    ? 'La cuenta podrá reanudar sus operaciones e iniciar sesión de inmediato. Se levantará la restricción vigente.'
    : textoOriginal.replace(' La acción quedará registrada.', '');

  return (
    <ModalConfirmacionAdmin
      open={open}
      onClose={onClose}
      onConfirm={onConfirmar}
      title={titulo}
      icono={icono}
      variante="primario"
      iconoConfirmar={icono}
      textoConfirmar={esReactivar ? 'Reactivar' : 'Desbloquear'}
      textoEnviando={esReactivar ? 'Reactivando...' : 'Desbloqueando...'}
      error={error}
      enviando={desbloqueando}
      className="caja-modal--admin-desbloquear"
    >
      <h3 className="admin-modal-titulo">{titulo}</h3>
      <p className="admin-modal-texto admin-modal-texto--desbloqueo">{texto}</p>
      <span className="admin-auditoria">
        <Icon icon="mdi:shield-check-outline" aria-hidden="true" />
        La acción quedará registrada en auditoría
      </span>
    </ModalConfirmacionAdmin>
  );
};

export default ModalDesbloquearUsuario;
