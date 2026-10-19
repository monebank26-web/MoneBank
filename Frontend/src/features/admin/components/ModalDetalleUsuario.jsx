import React from 'react';
import Modal from '../../../shared/components/Modal';
import {
  claseEstadoAdmin,
  etiquetaEstadoAdmin,
  etiquetaRolAdmin,
  fechaCreacionLegible,
} from '../utils/usuariosAdmin';

const ModalDetalleUsuario = ({ open, onClose, usuario }) => (
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
            {etiquetaEstadoAdmin(usuario.estado)}
          </span>
        </div>

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
            <span className="admin-detalle__valor">{fechaCreacionLegible(usuario.fecha_creacion)}</span>
          </div>
        </div>
      </div>
    )}
  </Modal>
);

export default ModalDetalleUsuario;
