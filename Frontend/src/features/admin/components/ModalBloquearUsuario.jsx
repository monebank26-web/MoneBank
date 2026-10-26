import React from 'react';
import { Icon } from '@iconify/react';
import Modal from '../../../shared/components/Modal';
import {
  LONGITUD_MAXIMA_MOTIVO_BLOQUEO,
  LONGITUD_MINIMA_MOTIVO_BLOQUEO,
} from '../utils/usuariosAdmin';

const ModalBloquearUsuario = ({
  open,
  onClose,
  usuario,
  motivoBloqueo,
  onCambiarMotivo,
  onConfirmar,
  error,
  bloqueando,
}) => {
  const texto = String(motivoBloqueo || '');
  const motivoCorto =
    texto.length > 0 && texto.trim().length < LONGITUD_MINIMA_MOTIVO_BLOQUEO;
  const nombre = usuario?.nombre || usuario?.email || 'este usuario';

  return (
    <Modal open={open} onClose={onClose} title="Bloquear cuenta">
      <div className="formulario-modal">
        <div className="admin-modal-icono admin-modal-icono--bloqueo">
          <Icon icon="mdi:shield-lock-outline" />
        </div>

        <div className="admin-modal-usuario">
          <span className="admin-modal-usuario__avatar">
            {(usuario?.nombres || usuario?.email || '?').charAt(0).toUpperCase()}
          </span>
          <span className="admin-modal-usuario__datos">
            <strong>{nombre}</strong>
            <span>{usuario?.email}</span>
          </span>
        </div>

        <p className="admin-modal-texto">
          La cuenta no podrá iniciar sesión mientras permanezca bloqueada.
        </p>

        <div className="grupo-campo">
          <label className="etiqueta-campo" htmlFor="admin-motivo-bloqueo">
            Motivo del bloqueo
          </label>
          <textarea
            id="admin-motivo-bloqueo"
            className={`campo-entrada admin-textarea${motivoCorto ? ' admin-textarea--invalido' : ''}`}
            value={texto}
            onChange={(e) => onCambiarMotivo(e.target.value)}
            placeholder="Explica brevemente por qué se bloquea esta cuenta."
            maxLength={LONGITUD_MAXIMA_MOTIVO_BLOQUEO}
            rows={4}
            autoFocus
            aria-invalid={motivoCorto || Boolean(error)}
            aria-describedby="admin-motivo-ayuda admin-motivo-contador"
          />
          <div className="admin-contador" id="admin-motivo-ayuda">
            <span className={motivoCorto ? 'admin-contador__minimo--error' : ''}>
              Mínimo {LONGITUD_MINIMA_MOTIVO_BLOQUEO} caracteres.
            </span>
            <span id="admin-motivo-contador">
              {texto.length}/{LONGITUD_MAXIMA_MOTIVO_BLOQUEO}
            </span>
          </div>
        </div>

        <p className="admin-modal-aviso">
          <Icon icon="mdi:information-outline" />
          El motivo quedará registrado para auditoría. No incluyas datos sensibles.
        </p>

        {error && (
          <div className="error-formulario" role="alert">
            {error}
          </div>
        )}

        <button
          type="button"
          className="admin-boton-peligro"
          onClick={onConfirmar}
          disabled={bloqueando}
        >
          <Icon icon={bloqueando ? 'mdi:loading' : 'mdi:lock-outline'} />
          {bloqueando ? 'Bloqueando...' : 'Bloquear cuenta'}
        </button>

        <button
          type="button"
          className="admin-boton-secundario"
          onClick={onClose}
          disabled={bloqueando}
        >
          Cancelar
        </button>
      </div>
    </Modal>
  );
};

export default ModalBloquearUsuario;
