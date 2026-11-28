import React, { useEffect, useRef, useState } from 'react';
import { Icon } from '@iconify/react';
import {
  ACCION_REACTIVAR,
  accionCuentaAdmin,
  claseEstadoAdmin,
  etiquetaEstadoAdmin,
  etiquetaRolAdmin,
  iconoEstadoAdmin,
  puedeBloquearUsuario,
  puedeDesactivarUsuario,
  puedeRestablecerPassword,
  tieneBloqueoTemporalAdmin,
} from '../utils/usuariosAdmin';

const FilaUsuarioAdmin = ({ usuario, usuarioActual, onVerDetalle, onAccion }) => {
  const [menuAbierto, setMenuAbierto] = useState(false);
  const menuRef = useRef(null);

  const estadoClase = String(usuario.estado || '').toLowerCase();
  const estaBloqueado = usuario.estado === 'BLOQUEADO';
  const nombre = usuario.nombre || usuario.email || 'usuario';
  const idUsuario = usuario.id ?? usuario.id_usuario;
  const identificador = idUsuario ? `#MB-${String(idUsuario).padStart(5, '0')}` : '';
  const accion = accionCuentaAdmin(usuario);
  const idActual = usuarioActual?.id_usuario ?? usuarioActual?.id;
  const esMismoUsuario = Boolean(
    idUsuario && idActual && String(idUsuario) === String(idActual)
  );

  useEffect(() => {
    if (!menuAbierto) return undefined;

    const cerrarAlClicarFuera = (evento) => {
      if (menuRef.current && !menuRef.current.contains(evento.target)) {
        setMenuAbierto(false);
      }
    };
    const cerrarConEscape = (evento) => {
      if (evento.key === 'Escape') setMenuAbierto(false);
    };

    document.addEventListener('pointerdown', cerrarAlClicarFuera);
    document.addEventListener('keydown', cerrarConEscape);

    return () => {
      document.removeEventListener('pointerdown', cerrarAlClicarFuera);
      document.removeEventListener('keydown', cerrarConEscape);
    };
  }, [menuAbierto]);

  const acciones = [
    { clave: 'detalle', etiqueta: 'Ver detalles', icono: 'mdi:eye-outline' },
  ];

  if (!esMismoUsuario && usuario.estado !== 'INACTIVO') {
    acciones.push({ clave: 'editar', etiqueta: 'Editar datos', icono: 'mdi:pencil-outline' });
  }

  if (!esMismoUsuario && puedeBloquearUsuario(usuario.estado)) {
    acciones.push({
      clave: 'bloquear',
      etiqueta: 'Bloquear cuenta',
      icono: 'mdi:lock-outline',
      tono: 'peligro',
    });
  }

  if (!esMismoUsuario && accion) {
    acciones.push({
      clave: 'desbloquear',
      etiqueta: accion === ACCION_REACTIVAR ? 'Reactivar cuenta' : 'Desbloquear cuenta',
      icono:
        accion === ACCION_REACTIVAR
          ? 'mdi:account-check-outline'
          : 'mdi:lock-open-outline',
    });
  }

  if (puedeRestablecerPassword(usuario, usuarioActual)) {
    acciones.push({
      clave: 'restablecer',
      etiqueta: 'Restablecer contraseña',
      icono: 'mdi:restore',
    });
  }

  if (!esMismoUsuario && puedeDesactivarUsuario(usuario.estado)) {
    acciones.push({
      clave: 'desactivar',
      etiqueta: 'Desactivar cuenta',
      icono: 'mdi:prohibited',
      tono: 'peligro',
    });
  }

  const elegirAccion = (clave) => {
    setMenuAbierto(false);
    if (clave === 'detalle') onVerDetalle?.(usuario);
    else onAccion?.(clave, usuario);
  };

  return (
    <div className={`admin-fila${estadoClase ? ` admin-fila--${estadoClase}` : ''}`}>
      <button
        type="button"
        className="admin-fila__overlay"
        onClick={() => onVerDetalle?.(usuario)}
        aria-label={`Abrir detalle de ${nombre}`}
      />

      <span className="admin-fila__usuario">
        <span
          className={`admin-avatar admin-avatar--${usuario.rol}${
            estaBloqueado ? ' admin-avatar--bloqueado' : ''
          }`}
        >
          {(usuario.nombres || usuario.email || '?').charAt(0).toUpperCase()}
          <span
            className={`admin-avatar__estado admin-avatar__estado--${estadoClase}`}
            aria-hidden="true"
          />
        </span>
        <span className="admin-fila__datos">
          <span className="admin-fila__nombre">{nombre}</span>
          <span className="admin-fila__correo">{usuario.email}</span>
        </span>
      </span>

      <span className="admin-fila__id">
        <span className="admin-fila__id-etiqueta">ID:</span>{' '}
        <span className="admin-fila__id-valor">{identificador}</span>
      </span>

      <span className="admin-fila__rol">
        <span className={`admin-etiqueta-rol admin-etiqueta-rol--${usuario.rol}`}>
          {etiquetaRolAdmin(usuario.rol)}
        </span>
      </span>

      <span className="admin-fila__estado">
        <span className={claseEstadoAdmin(usuario.estado)}>
          {estaBloqueado ? (
            <span className="admin-fila__punto-estado" aria-hidden="true" />
          ) : (
            <Icon icon={iconoEstadoAdmin(usuario.estado)} aria-hidden="true" />
          )}
          {etiquetaEstadoAdmin(usuario.estado)}
        </span>

        {estaBloqueado && usuario.motivo_bloqueo && (
          <span className="admin-fila__motivo-badge">
            Motivo: {usuario.motivo_bloqueo}
          </span>
        )}

        {tieneBloqueoTemporalAdmin(usuario) && (
          <span className="admin-etiqueta-temporal">
            <Icon icon="mdi:clock-outline" aria-hidden="true" />
            Bloqueo temporal
          </span>
        )}
      </span>

      <span className="admin-fila__acciones" ref={menuRef}>
        <button
          type="button"
          className="admin-fila__icono"
          aria-label={`Ver detalle de ${nombre}`}
          title="Ver detalle"
          onClick={(evento) => {
            evento.stopPropagation();
            onVerDetalle?.(usuario);
          }}
        >
          <Icon icon="mdi:eye-outline" aria-hidden="true" />
        </button>

        <button
          type="button"
          className="admin-fila__icono"
          aria-label={`Acciones de ${nombre}`}
          aria-haspopup="menu"
          aria-expanded={menuAbierto}
          title="Acciones"
          onClick={(evento) => {
            evento.stopPropagation();
            setMenuAbierto((abierto) => !abierto);
          }}
        >
          <Icon icon="mdi:dots-vertical" aria-hidden="true" />
        </button>

        {menuAbierto && (
          <div className="admin-fila__menu" role="menu" aria-label={`Acciones de ${nombre}`}>
            {acciones.map((item) => (
              <button
                key={item.clave}
                type="button"
                role="menuitem"
                className={`admin-fila__menu-item${
                  item.tono === 'peligro' ? ' admin-fila__menu-item--peligro' : ''
                }`}
                onClick={(evento) => {
                  evento.stopPropagation();
                  elegirAccion(item.clave);
                }}
              >
                <Icon icon={item.icono} aria-hidden="true" />
                {item.etiqueta}
              </button>
            ))}
          </div>
        )}
      </span>
    </div>
  );
};

export default FilaUsuarioAdmin;
