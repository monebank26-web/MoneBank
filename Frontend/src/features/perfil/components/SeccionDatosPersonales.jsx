import React from 'react';
import { formatFecha } from '../../../core/utils/format';
import { etiquetaRol } from '../../../core/utils/roles';

const SeccionDatosPersonales = ({
  user,
  editando,
  setEditando,
  formDatos,
  errorDatos,
  exitoDatos,
  onChange,
  onGuardar,
  onCancelar,
}) => {
  return (
    <div className="tarjeta-seccion-perfil">
      <div className="encabezado-seccion-perfil">
        <h3 className="titulo-seccion-perfil">Datos personales</h3>
        {!editando && (
          <button className="boton-secundario-perfil" onClick={() => setEditando(true)}>
            Editar
          </button>
        )}
      </div>

      {!editando ? (
        <div className="lista-datos-perfil">
          <div className="fila-dato-perfil">
            <span className="etiqueta-dato-perfil">Nombre completo</span>
            <span className="valor-dato-perfil">{user?.nombre}</span>
          </div>
          <div className="fila-dato-perfil">
            <span className="etiqueta-dato-perfil">Correo electrónico</span>
            <span className="valor-dato-perfil">{user?.email}</span>
          </div>
          <div className="fila-dato-perfil">
            <span className="etiqueta-dato-perfil">Tipo de cuenta</span>
            <span className="valor-dato-perfil">{etiquetaRol(user?.rol)}</span>
          </div>
          <div className="fila-dato-perfil">
            <span className="etiqueta-dato-perfil">Cliente desde</span>
            <span className="valor-dato-perfil">{formatFecha(user?.createdAt)}</span>
          </div>
          {exitoDatos && <p className="mensaje-exito-perfil">{exitoDatos}</p>}
        </div>
      ) : (
        <form className="formulario-perfil" onSubmit={onGuardar}>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Nombre completo</label>
            <input
              className="campo-entrada"
              type="text"
              name="nombre"
              value={formDatos.nombre}
              onChange={onChange}
              required
            />
          </div>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Correo electrónico</label>
            <input
              className="campo-entrada"
              type="email"
              name="email"
              value={formDatos.email}
              onChange={onChange}
              required
            />
          </div>
          {errorDatos && <p className="error-autenticacion">{errorDatos}</p>}
          <div className="acciones-formulario-perfil">
            <button type="submit" className="boton-principal-perfil">Guardar cambios</button>
            <button type="button" className="boton-secundario-perfil" onClick={onCancelar}>
              Cancelar
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default SeccionDatosPersonales;
