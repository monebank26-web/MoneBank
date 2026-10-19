import React from 'react';
import { Icon } from '@iconify/react';
import { claseEstadoAdmin, etiquetaEstadoAdmin, etiquetaRolAdmin } from '../utils/usuariosAdmin';

const FilaUsuarioAdmin = ({ usuario, onVerDetalle, onEditar }) => (
  <div className="admin-fila">
    <div className={`admin-avatar admin-avatar--${usuario.rol}`}>
      {(usuario.nombres || usuario.email || '?').charAt(0).toUpperCase()}
    </div>

    <div className="admin-fila__datos">
      <p className="admin-fila__nombre">{usuario.nombre || usuario.email}</p>
      <p className="admin-fila__correo">{usuario.email}</p>
    </div>

    <div className="admin-fila__etiquetas">
      <span className={`admin-etiqueta-rol admin-etiqueta-rol--${usuario.rol}`}>
        {etiquetaRolAdmin(usuario.rol)}
      </span>
      <span className={claseEstadoAdmin(usuario.estado)}>
        {etiquetaEstadoAdmin(usuario.estado)}
      </span>
    </div>

    <div className="admin-fila__acciones">
      <button
        type="button"
        className="admin-boton-accion admin-boton-accion--ver"
        onClick={() => onVerDetalle(usuario)}
      >
        <Icon icon="mdi:eye-outline" />
        Ver
      </button>
      <button
        type="button"
        className="admin-boton-accion admin-boton-accion--editar"
        onClick={() => onEditar(usuario)}
      >
        <Icon icon="mdi:pencil-outline" />
        Editar
      </button>
    </div>
  </div>
);

export default FilaUsuarioAdmin;
