import React from 'react';
import Modal from '../../../shared/components/Modal';

const ModalCambiarPassword = ({
  open,
  onClose,
  formPassword,
  errorPassword,
  exitoPassword,
  cargandoPassword,
  onChange,
  onGuardar,
}) => {
  return (
    <Modal open={open} onClose={onClose} title="Cambiar contraseña">
      <form className="formulario-perfil" onSubmit={onGuardar}>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Contraseña actual</label>
          <input
            className="campo-entrada"
            type="password"
            name="actual"
            placeholder="••••••••"
            value={formPassword.actual}
            onChange={onChange}
            required
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Nueva contraseña</label>
          <input
            className="campo-entrada"
            type="password"
            name="nueva"
            placeholder="••••••••"
            value={formPassword.nueva}
            onChange={onChange}
            required
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Confirmar nueva contraseña</label>
          <input
            className="campo-entrada"
            type="password"
            name="confirmar"
            placeholder="••••••••"
            value={formPassword.confirmar}
            onChange={onChange}
            required
          />
        </div>
        {errorPassword && <p className="error-autenticacion">{errorPassword}</p>}
        {exitoPassword && <p className="mensaje-exito-perfil">{exitoPassword}</p>}
        <div className="acciones-formulario-perfil">
          <button type="submit" className="boton-principal-perfil" disabled={cargandoPassword}>
            {cargandoPassword ? 'Guardando...' : 'Actualizar contraseña'}
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default ModalCambiarPassword;
