import React from 'react';
import { ROLES } from '../../../core/constants';
import { formatFecha } from '../../../core/utils/format';

const SeccionDatosPersonales = ({
  user,
  editando,
  setEditando,
  formDatos,
  errorDatos,
  exitoDatos,
  cargandoDatos,
  onChange,
  onGuardar,
  onCancelar,
}) => {
  const esAdministrador = user?.rol === ROLES.ADMIN;

  const nombreCompleto =
    user?.nombre ||
    `${user?.nombres || ''} ${user?.apellidos || ''}`.trim();

  const correo =
    user?.email ||
    user?.correo ||
    '';

  const fechaCreacion =
    user?.fecha_creacion ||
    user?.fechaCreacion ||
    user?.createdAt;

  return (
    <div className="tarjeta-seccion-perfil">
      <div className="encabezado-seccion-perfil">
        <h3 className="titulo-seccion-perfil">
          Datos personales
        </h3>

        {!editando && (
          <button
            type="button"
            className="boton-secundario-perfil"
            onClick={() => setEditando(true)}
          >
            Editar
          </button>
        )}
      </div>

      {!editando ? (
        <div className="lista-datos-perfil">
          <div className="fila-dato-perfil">
            <span className="etiqueta-dato-perfil">
              Nombre completo
            </span>

            <span className="valor-dato-perfil">
              {nombreCompleto || 'No disponible'}
            </span>
          </div>

          <div className="fila-dato-perfil">
            <span className="etiqueta-dato-perfil">
              Correo electrónico
            </span>

            <span className="valor-dato-perfil">
              {correo || 'No disponible'}
            </span>
          </div>

          {esAdministrador && (
            <div className="fila-dato-perfil">
              <span className="etiqueta-dato-perfil">
                Tipo de cuenta
              </span>

              <span className="valor-dato-perfil">
                Administrador
              </span>
            </div>
          )}

        <div className="fila-dato-perfil">
          <span className="etiqueta-dato-perfil">
           Cliente desde
          </span>

          <span className="valor-dato-perfil">
            {user?.fecha_creacion
              ? formatFecha(user.fecha_creacion)
              : 'No disponible'}
          </span>
        </div>


          {exitoDatos && (
            <p className="mensaje-exito-perfil">
              {exitoDatos}
            </p>
          )}
        </div>
      ) : (
        <form
          className="formulario-perfil"
          onSubmit={onGuardar}
        >
          <div className="grupo-campo">
            <label
              className="etiqueta-campo"
              htmlFor="nombre"
            >
              Nombre completo
            </label>

            <input
              id="nombre"
              className="campo-entrada"
              type="text"
              name="nombre"
              value={formDatos?.nombre || ''}
              onChange={onChange}
              required
            />
          </div>

          <div className="grupo-campo">
            <label
              className="etiqueta-campo"
              htmlFor="email"
            >
              Correo electrónico
            </label>

            <input
              id="email"
              className="campo-entrada"
              type="email"
              name="email"
              value={formDatos?.email || ''}
              onChange={onChange}
              required
            />
          </div>

          {errorDatos && (
            <p className="error-autenticacion">
              {errorDatos}
            </p>
          )}

          <div className="acciones-formulario-perfil">
            <button
              type="submit"
              className="boton-principal-perfil"
              disabled={cargandoDatos}
            >
              {cargandoDatos
              ? 'Guardando...'
              : 'Guardar cambios'}
            </button>

            <button
              type="button"
              className="boton-secundario-perfil"
              onClick={onCancelar}
            >
              Cancelar
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default SeccionDatosPersonales;
