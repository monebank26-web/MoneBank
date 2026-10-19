import React from 'react';
import Modal from '../../../shared/components/Modal';

const ModalEditarUsuario = ({ open, onClose, formulario, setFormulario, onGuardar, error, guardando }) => (
  <Modal open={open} onClose={onClose} title="Editar usuario">
    <div className="formulario-modal">
      <div className="grupo-campo">
        <label className="etiqueta-campo" htmlFor="admin-editar-nombres">Nombres</label>
        <input
          id="admin-editar-nombres"
          className="campo-entrada"
          type="text"
          value={formulario.nombres || ''}
          onChange={(e) => setFormulario({ ...formulario, nombres: e.target.value })}
        />
      </div>

      <div className="grupo-campo">
        <label className="etiqueta-campo" htmlFor="admin-editar-apellidos">Apellidos</label>
        <input
          id="admin-editar-apellidos"
          className="campo-entrada"
          type="text"
          value={formulario.apellidos || ''}
          onChange={(e) => setFormulario({ ...formulario, apellidos: e.target.value })}
        />
      </div>

      <div className="grupo-campo">
        <label className="etiqueta-campo" htmlFor="admin-editar-correo">Correo electrónico</label>
        <input
          id="admin-editar-correo"
          className="campo-entrada"
          type="email"
          value={formulario.email || ''}
          onChange={(e) => setFormulario({ ...formulario, email: e.target.value })}
        />
      </div>

      {error && <div className="error-formulario">{error}</div>}

      <button className="boton-principal" onClick={onGuardar} disabled={guardando}>
        {guardando ? 'Guardando...' : 'Guardar cambios'}
      </button>
    </div>
  </Modal>
);

export default ModalEditarUsuario;
