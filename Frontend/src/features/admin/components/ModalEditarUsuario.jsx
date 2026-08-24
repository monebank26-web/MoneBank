import React from 'react';
import Modal from '../../../shared/components/Modal';
import { ROLES } from '../../../core/constants';

const ModalEditarUsuario = ({ open, onClose, formulario, setFormulario, onGuardar }) => {
  return (
    <Modal open={open} onClose={onClose} title="Editar usuario">
      <div className="formulario-modal">
        <div className="grupo-campo">
          <label className="etiqueta-campo">Nombre completo</label>
          <input className="campo-entrada" type="text" value={formulario.nombre || ''}
            onChange={(e) => setFormulario({ ...formulario, nombre: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Correo electrónico</label>
          <input className="campo-entrada" type="email" value={formulario.email || ''}
            onChange={(e) => setFormulario({ ...formulario, email: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Saldo en cuenta (COP)</label>
          <input className="campo-entrada" type="number" value={formulario.saldoCuenta || 0}
            onChange={(e) => setFormulario({ ...formulario, saldoCuenta: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Rol</label>
          <select className="campo-entrada" value={formulario.rol || ''}
            onChange={(e) => setFormulario({ ...formulario, rol: e.target.value })}>
            <option value={ROLES.NORMAL}>Normal</option>
            <option value={ROLES.PADRE}>Padre/Madre</option>
            <option value={ROLES.HIJO}>Hijo/Hija</option>
            <option value={ROLES.ADMIN}>Administrador</option>
          </select>
        </div>
        <button className="boton-principal" onClick={onGuardar}>Guardar cambios</button>
      </div>
    </Modal>
  );
};

export default ModalEditarUsuario;
