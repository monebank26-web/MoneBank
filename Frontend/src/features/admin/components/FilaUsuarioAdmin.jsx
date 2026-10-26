import React from 'react';
import { Icon } from '@iconify/react';
import {
  claseEstadoAdmin,
  etiquetaEstadoAdmin,
  etiquetaRolAdmin,
  iconoEstadoAdmin,
} from '../utils/usuariosAdmin';

const FilaUsuarioAdmin = ({ usuario, onVerDetalle }) => {
  const estadoClase = String(usuario.estado || '').toLowerCase();
  const estaBloqueado = usuario.estado === 'BLOQUEADO';
  const nombre = usuario.nombre || usuario.email || 'usuario';

  return (
    <button
      type="button"
      className={`admin-fila${estadoClase ? ` admin-fila--${estadoClase}` : ''}`}
      onClick={() => onVerDetalle(usuario)}
      aria-label={`Abrir detalle de ${nombre}`}
    >
      <span className={`admin-avatar admin-avatar--${usuario.rol}`}>
        {(usuario.nombres || usuario.email || '?').charAt(0).toUpperCase()}
      </span>

      <span className="admin-fila__datos">
        <span className="admin-fila__nombre">{nombre}</span>
        <span className="admin-fila__correo">{usuario.email}</span>
        {estaBloqueado && usuario.motivo_bloqueo && (
          <span className="admin-fila__motivo">
            <Icon icon="mdi:lock-outline" />
            <span>{usuario.motivo_bloqueo}</span>
          </span>
        )}
      </span>

      <span className="admin-fila__etiquetas">
        <span className={`admin-etiqueta-rol admin-etiqueta-rol--${usuario.rol}`}>
          {etiquetaRolAdmin(usuario.rol)}
        </span>
        <span className={claseEstadoAdmin(usuario.estado)}>
          <Icon icon={iconoEstadoAdmin(usuario.estado)} />
          {etiquetaEstadoAdmin(usuario.estado)}
        </span>
      </span>

      <span className="admin-fila__chevron" aria-hidden="true">
        <Icon icon="mdi:chevron-right" />
      </span>
    </button>
  );
};

export default FilaUsuarioAdmin;
