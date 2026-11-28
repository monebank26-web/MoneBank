import React from 'react';
import { Icon } from '@iconify/react';
import Modal from '../../../shared/components/Modal';

const ModalEditarUsuario = ({ open, onClose, formulario, setFormulario, onGuardar, error, guardando }) => (
  <Modal
    open={open}
    onClose={onClose}
    className="caja-modal--admin-editar"
    title={
      <>
        <span className="admin-editar__icono" aria-hidden="true">
          <Icon icon="mdi:account-outline" />
        </span>
        <span className="admin-editar__cabecera-texto">
          <span className="admin-editar__titulo">Editar usuario</span>
          <span className="admin-editar__subtitulo">
            Actualice los datos personales de la cuenta MoneBank
          </span>
        </span>
      </>
    }
  >
    <div className="formulario-modal">
      <div className="grupo-campo">
        <label className="etiqueta-campo" htmlFor="admin-editar-nombres">Nombres</label>
        <div className="admin-editar__control">
          <Icon icon="mdi:account-outline" className="admin-editar__prefijo" aria-hidden="true" />
          <input
            id="admin-editar-nombres"
            className="campo-entrada admin-editar__entrada"
            type="text"
            value={formulario.nombres || ''}
            onChange={(e) => setFormulario({ ...formulario, nombres: e.target.value })}
          />
        </div>
      </div>

      <div className="grupo-campo">
        <label className="etiqueta-campo" htmlFor="admin-editar-apellidos">Apellidos</label>
        <div className="admin-editar__control">
          <Icon icon="mdi:card-account-details-outline" className="admin-editar__prefijo" aria-hidden="true" />
          <input
            id="admin-editar-apellidos"
            className="campo-entrada admin-editar__entrada"
            type="text"
            value={formulario.apellidos || ''}
            onChange={(e) => setFormulario({ ...formulario, apellidos: e.target.value })}
          />
        </div>
      </div>

      <div className="grupo-campo">
        <label className="etiqueta-campo" htmlFor="admin-editar-correo">Correo electrónico</label>
        <div className="admin-editar__control">
          <Icon icon="mdi:email-outline" className="admin-editar__prefijo" aria-hidden="true" />
          <input
            id="admin-editar-correo"
            className="campo-entrada admin-editar__entrada"
            type="email"
            value={formulario.email || ''}
            onChange={(e) => setFormulario({ ...formulario, email: e.target.value })}
          />
        </div>
      </div>

      <p className="admin-editar__aviso">
        <Icon icon="mdi:shield-alert-outline" aria-hidden="true" />
        Los cambios se sincronizarán inmediatamente con las credenciales bancarias.
      </p>

      {error && <div className="error-formulario">{error}</div>}

      <button className="boton-principal admin-editar__guardar" onClick={onGuardar} disabled={guardando}>
        <Icon icon="mdi:check" aria-hidden="true" />
        {guardando ? 'Guardando...' : 'Guardar cambios'}
      </button>

      <button
        type="button"
        className="admin-editar__cancelar"
        onClick={onClose}
        disabled={guardando}
      >
        Cancelar
      </button>
    </div>
  </Modal>
);

export default ModalEditarUsuario;
