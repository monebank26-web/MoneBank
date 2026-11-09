import React from 'react';
import { Icon } from '@iconify/react';
import Modal from '../../../shared/components/Modal';
import {
  ACCION_REACTIVAR,
  accionCuentaAdmin,
  claseEstadoAdmin,
  etiquetaEstadoAdmin,
  etiquetaRolAdmin,
  fechaBloqueoLegible,
  fechaCreacionLegible,
  iconoEstadoAdmin,
  puedeBloquearUsuario,
  puedeDesactivarUsuario,
  tieneBloqueoTemporalAdmin,
} from '../utils/usuariosAdmin';

const ModalDetalleUsuario = ({
  open,
  onClose,
  usuario,
  onEditar,
  onBloquear,
  onEliminar,
  onDesbloquear,
}) => {
  const accion = accionCuentaAdmin(usuario);
  const esReactivar = accion === ACCION_REACTIVAR;

  return (
    <Modal open={open} onClose={onClose} title="Detalle del usuario">
      {usuario && (
        <div className="admin-detalle">
          <div className="admin-detalle__avatar">
            {(usuario.nombres || usuario.email || '?').charAt(0).toUpperCase()}
          </div>
          <h2 className="admin-detalle__nombre">{usuario.nombre || usuario.email}</h2>
          <p className="admin-detalle__correo">{usuario.email}</p>

          <div className="admin-detalle__etiquetas">
            <span className={`admin-etiqueta-rol admin-etiqueta-rol--${usuario.rol}`}>
              {etiquetaRolAdmin(usuario.rol)}
            </span>
            <span className={claseEstadoAdmin(usuario.estado)}>
              <Icon icon={iconoEstadoAdmin(usuario.estado)} />
              {etiquetaEstadoAdmin(usuario.estado)}
            </span>
            {tieneBloqueoTemporalAdmin(usuario) && (
              <span className="admin-etiqueta-temporal">
                <Icon icon="mdi:clock-outline" aria-hidden="true" />
                Bloqueo temporal
              </span>
            )}
          </div>

          {usuario.estado === 'BLOQUEADO' && (
            <div className="admin-detalle__bloqueo">
              <div className="admin-detalle__bloqueo-cabecera">
                <Icon icon="mdi:shield-lock-outline" />
                <span>Cuenta bloqueada</span>
              </div>
              <p className="admin-detalle__bloqueo-motivo">
                {usuario.motivo_bloqueo || 'Sin motivo registrado.'}
              </p>
              {usuario.fecha_bloqueo && (
                <span className="admin-detalle__bloqueo-fecha">
                  <Icon icon="mdi:calendar-clock-outline" />
                  Desde el {fechaBloqueoLegible(usuario.fecha_bloqueo)}
                </span>
              )}
            </div>
          )}

          <div className="admin-detalle__campos">
            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Correo electrónico</span>
              <span className="admin-detalle__valor">{usuario.email}</span>
            </div>
            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Rol</span>
              <span className="admin-detalle__valor">{etiquetaRolAdmin(usuario.rol)}</span>
            </div>
            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Estado</span>
              <span className="admin-detalle__valor">{etiquetaEstadoAdmin(usuario.estado)}</span>
            </div>
            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Miembro desde</span>
              <span className="admin-detalle__valor">
                {fechaCreacionLegible(usuario.fecha_creacion)}
              </span>
            </div>
            {usuario.fecha_desbloqueo && (
              <div className="admin-detalle__campo">
                <span className="admin-detalle__etiqueta">Último desbloqueo</span>
                <span className="admin-detalle__valor">
                  {fechaBloqueoLegible(usuario.fecha_desbloqueo)}
                </span>
              </div>
            )}
          </div>

          <div className="admin-detalle__acciones">
            <span className="admin-detalle__acciones-titulo">Acciones de la cuenta</span>

            <div className="admin-detalle__acciones-botones">
              {usuario.estado !== 'INACTIVO' && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--editar"
                  onClick={() => onEditar?.(usuario)}
                >
                  <Icon icon="mdi:pencil-outline" />
                  Editar datos
                </button>
              )}

              {accion && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--desbloquear"
                  onClick={() => onDesbloquear?.(usuario)}
                >
                  <Icon
                    icon={
                      esReactivar
                        ? 'mdi:account-check-outline'
                        : 'mdi:lock-open-outline'
                    }
                    aria-hidden="true"
                  />
                  {esReactivar ? 'Reactivar cuenta' : 'Desbloquear cuenta'}
                </button>
              )}

              {puedeBloquearUsuario(usuario.estado) && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--bloquear"
                  onClick={() => onBloquear?.(usuario)}
                >
                  <Icon icon="mdi:lock-outline" />
                  Bloquear cuenta
                </button>
              )}

              {puedeDesactivarUsuario(usuario.estado) && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--desactivar"
                  onClick={() => onEliminar?.(usuario)}
                >
                  <Icon icon="mdi:account-off-outline" />
                  Desactivar cuenta
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </Modal>
  );
};

export default ModalDetalleUsuario;
