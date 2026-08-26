import React from 'react';
import Modal from '../../../shared/components/Modal';
import { ROLES } from '../../../core/constants';
import { formatMoney } from '../../../core/utils/format';
import { etiquetaRol } from '../../../core/utils/roles';

const ModalDetalleUsuario = ({ open, onClose, usuario, usuarioVinculado }) => {
  return (
    <Modal open={open} onClose={onClose} title="Detalle del usuario">
      {usuario && (
        <div className="detalle-usuario-admin">
          <div className="avatar-detalle-admin">
            {usuario.nombre.charAt(0).toUpperCase()}
          </div>
          <h2 className="nombre-detalle-admin">{usuario.nombre}</h2>
          <p className="correo-detalle-admin">{usuario.email}</p>
          <span className={`etiqueta-rol-admin etiqueta-rol-admin--${usuario.rol}`}>
            {etiquetaRol(usuario.rol)}
          </span>

          <div className="campos-detalle-admin">
            <div className="campo-detalle-admin">
              <span className="etiqueta-campo-detalle">Saldo en cuenta</span>
              <span className="valor-campo-detalle">{formatMoney(usuario.saldoCuenta)}</span>
            </div>
            <div className="campo-detalle-admin">
              <span className="etiqueta-campo-detalle">Miembro desde</span>
              <span className="valor-campo-detalle">
                {new Date(usuario.createdAt).toLocaleDateString('es-CO', { day: '2-digit', month: 'long', year: 'numeric' })}
              </span>
            </div>
            {usuario.esMenor && (
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">Menor de edad</span>
                <span className="valor-campo-detalle">Sí</span>
              </div>
            )}
            {usuarioVinculado && (
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">
                  {usuario.rol === ROLES.PADRE ? 'Hijo/Hija vinculado' : 'Padre/Madre vinculado'}
                </span>
                <span className="valor-campo-detalle">{usuarioVinculado.nombre}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
};

export default ModalDetalleUsuario;
