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
  puedeRestablecerPassword,
  tieneBloqueoTemporalAdmin,
} from '../utils/usuariosAdmin';

const ModalDetalleUsuario = ({
  open,
  onClose,
  usuario,
  usuarioActual,
  onEditar,
  onBloquear,
  onEliminar,
  onDesbloquear,
  onRestablecer,
}) => {
  const accion = accionCuentaAdmin(usuario);
  const esReactivar = accion === ACCION_REACTIVAR;
  const esBloqueado = usuario?.estado === 'BLOQUEADO';
  const idUsuario = usuario?.id ?? usuario?.id_usuario;
  const identificador = idUsuario
    ? `#MB-${String(idUsuario).padStart(5, '0')}`
    : '';

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Detalle del usuario"
      className="caja-modal--admin-detalle"
    >
      {usuario && (
        <div className="admin-detalle">
          <div className="admin-detalle__avatar">
            {(usuario.nombres || usuario.email || '?').charAt(0).toUpperCase()}
            {esBloqueado && (
              <span className="admin-detalle__avatar-badge" aria-hidden="true">
                <Icon icon="mdi:lock" />
              </span>
            )}
          </div>
          <h2 className="admin-detalle__nombre">{usuario.nombre || usuario.email}</h2>
          <p className="admin-detalle__correo">{usuario.email}</p>

          <div className="admin-detalle__etiquetas">
            <span className={`admin-etiqueta-rol admin-etiqueta-rol--${usuario.rol}`}>
              {etiquetaRolAdmin(usuario.rol)}
            </span>
            <span className={claseEstadoAdmin(usuario.estado)}>
              {esBloqueado ? (
                <span className="admin-detalle__punto-estado" aria-hidden="true" />
              ) : (
                <Icon icon={iconoEstadoAdmin(usuario.estado)} />
              )}
              {etiquetaEstadoAdmin(usuario.estado)}
            </span>
            {tieneBloqueoTemporalAdmin(usuario) && (
              <span className="admin-etiqueta-temporal">
                <Icon icon="mdi:clock-outline" aria-hidden="true" />
                Bloqueo temporal
              </span>
            )}
          </div>

          {esBloqueado && (
            <div className="admin-detalle__bloqueo">
              <div className="admin-detalle__bloqueo-cabecera">
                <span className="admin-detalle__bloqueo-icono" aria-hidden="true">
                  <Icon icon="mdi:alert-outline" />
                </span>
                <span>Acceso de cuenta bloqueado</span>
              </div>
              <p className="admin-detalle__bloqueo-motivo">
                <span className="admin-detalle__bloqueo-motivo-texto">
                  Motivo: {usuario.motivo_bloqueo || 'Sin motivo registrado.'}
                </span>
              </p>
              {usuario.fecha_bloqueo && (
                <span className="admin-detalle__bloqueo-fecha">
                  <Icon icon="mdi:calendar-outline" aria-hidden="true" />
                  Bloqueado el {fechaBloqueoLegible(usuario.fecha_bloqueo)}
                </span>
              )}
            </div>
          )}

          <div className="admin-detalle__campos">
            <div className="admin-detalle__ficha-cabecera">
              <span className="admin-detalle__ficha-titulo">Ficha de usuario</span>
              {identificador && (
                <span className="admin-detalle__ficha-id">ID: {identificador}</span>
              )}
            </div>

            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Correo electrónico</span>
              <span className="admin-detalle__valor admin-detalle__valor--correo">
                {usuario.email}
              </span>
            </div>
            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Rol</span>
              <span className="admin-detalle__valor">{etiquetaRolAdmin(usuario.rol)}</span>
            </div>
            <div className="admin-detalle__campo">
              <span className="admin-detalle__etiqueta">Estado del sistema</span>
              <span
                className={`admin-detalle__valor${
                  esBloqueado ? ' admin-detalle__valor--bloqueado' : ''
                }`}
              >
                {esBloqueado && (
                  <span className="admin-detalle__punto-estado" aria-hidden="true" />
                )}
                {etiquetaEstadoAdmin(usuario.estado)}
              </span>
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
            <div className="admin-detalle__acciones-cabecera">
              <span className="admin-detalle__acciones-titulo">Acciones de la cuenta</span>
              {usuario.rol === 'administrador' && (
                <span className="admin-detalle__privilegios">Privilegios Admin</span>
              )}
            </div>

            <div className="admin-detalle__acciones-botones">
              {accion && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--desbloquear admin-detalle__boton--principal"
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

              {!accion && puedeBloquearUsuario(usuario.estado) && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--bloquear admin-detalle__boton--principal"
                  onClick={() => onBloquear?.(usuario)}
                >
                  <Icon icon="mdi:lock-outline" aria-hidden="true" />
                  Bloquear cuenta
                </button>
              )}

              <div className="admin-detalle__acciones-secundarias">
                {usuario.estado !== 'INACTIVO' && (
                  <button
                    type="button"
                    className="admin-detalle__boton admin-detalle__boton--editar admin-detalle__boton--secundario"
                    onClick={() => onEditar?.(usuario)}
                  >
                    <Icon icon="mdi:pencil-outline" aria-hidden="true" />
                    Editar datos
                  </button>
                )}

                {puedeRestablecerPassword(usuario, usuarioActual) && (
                  <button
                    type="button"
                    className="admin-detalle__boton admin-detalle__boton--restablecer admin-detalle__boton--secundario"
                    title="Restablecer contraseña"
                    aria-label="Restablecer contraseña"
                    onClick={() => onRestablecer?.(usuario)}
                  >
                    <Icon icon="mdi:restore" aria-hidden="true" />
                    Restablecer Contraseña
                  </button>
                )}
              </div>

              {accion && puedeBloquearUsuario(usuario.estado) && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--bloquear admin-detalle__boton--texto"
                  onClick={() => onBloquear?.(usuario)}
                >
                  <Icon icon="mdi:lock-outline" aria-hidden="true" />
                  Bloquear cuenta
                </button>
              )}

              {puedeDesactivarUsuario(usuario.estado) && (
                <button
                  type="button"
                  className="admin-detalle__boton admin-detalle__boton--desactivar admin-detalle__boton--texto"
                  onClick={() => onEliminar?.(usuario)}
                >
                  <Icon icon="mdi:prohibited" aria-hidden="true" />
                  Desactivar cuenta permanentemente
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
