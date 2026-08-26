import React from 'react';
import { ROLES } from '../../../core/constants';
import { formatMoney } from '../../../core/utils/format';
import { etiquetaRol } from '../../../core/utils/roles';

const FilaUsuarioAdmin = ({ usuario, onVerDetalle, onEditar, onEliminar }) => {
  return (
    <div className="fila-usuario-admin">
      <div className="avatar-usuario-admin">
        {usuario.nombre.charAt(0).toUpperCase()}
      </div>
      <div className="informacion-usuario-admin">
        <p className="nombre-usuario-admin">{usuario.nombre}</p>
        <p className="correo-usuario-admin">{usuario.email}</p>
        <span className={`etiqueta-rol-admin etiqueta-rol-admin--${usuario.rol}`}>
          {etiquetaRol(usuario.rol)}
        </span>
      </div>
      <div className="saldo-usuario-admin">
        <p className="valor-saldo-admin">{formatMoney(usuario.saldoCuenta)}</p>
        <p className="etiqueta-saldo-admin">Saldo en cuenta</p>
      </div>
      <div className="acciones-usuario-admin">
        <button className="boton-accion-admin boton-accion-admin--ver" onClick={() => onVerDetalle(usuario)}>
          Ver
        </button>
        <button className="boton-accion-admin boton-accion-admin--editar" onClick={() => onEditar(usuario)}>
          Editar
        </button>
        {usuario.rol !== ROLES.ADMIN && (
          <button className="boton-accion-admin boton-accion-admin--eliminar" onClick={() => onEliminar(usuario)}>
            Eliminar
          </button>
        )}
      </div>
    </div>
  );
};

export default FilaUsuarioAdmin;
