import React, { useEffect, useState } from 'react';

import { useDatosPersonales } from '../hooks/useDatosPersonales';
import { useCambiarPassword } from '../hooks/useCambiarPassword';

import { controlParentalService } from '../../controlParental/services/controlParentalServices';

import TarjetaResumenPerfil from '../components/TarjetaResumenPerfil';
import SeccionDatosPersonales from '../components/SeccionDatosPersonales';
import SeccionDesvincularPadre from '../components/SeccionDesvincularPadre';
import ModalCambiarPassword from '../components/ModalCambiarPassword';

import './PerfilPage.css';

const PerfilPage = () => {
  const datosPersonales = useDatosPersonales();
  const cambiarPassword = useCambiarPassword();

  const [
    relacionesParentales,
    setRelacionesParentales,
  ] = useState([]);

  useEffect(() => {
    const cargarRelacionesParentales = async () => {
      try {
        const relaciones =
          await controlParentalService.obtenerVinculaciones();

        setRelacionesParentales(
          Array.isArray(relaciones)
            ? relaciones
            : []
        );
      } catch (error) {
        console.error(
          'No se pudieron cargar las relaciones parentales:',
          error
        );

        setRelacionesParentales([]);
      }
    };

    cargarRelacionesParentales();
  }, []);

  const usuarioId = Number(
    datosPersonales.user?.id ||
      datosPersonales.user?.id_usuario ||
      datosPersonales.user?.usuario_id
  );

  const relacionActiva = (relacion) => {
    return (
      !relacion.estado ||
      relacion.estado === 'ACTIVO'
    );
  };

  const esPadre = relacionesParentales.some(
    (relacion) =>
      relacionActiva(relacion) &&
      Number(relacion.id_usuario_parental) === usuarioId
  );

  const esHijo = relacionesParentales.some(
    (relacion) =>
      relacionActiva(relacion) &&
      Number(relacion.id_usuario_dependiente) === usuarioId
  );

  const relacionComoHijo = relacionesParentales.find(
    (relacion) =>
      relacionActiva(relacion) &&
      Number(relacion.id_usuario_dependiente) === usuarioId
  );

  return (
    <div className="pagina-perfil">
      <div className="encabezado-perfil">
        <h1 className="titulo-perfil">
          Mi perfil
        </h1>

        <p className="subtitulo-perfil">
          Consulta y modifica la información de tu cuenta.
        </p>
      </div>

      <TarjetaResumenPerfil
        user={datosPersonales.user}
        relaciones={relacionesParentales}
      />


      <SeccionDatosPersonales
        user={datosPersonales.user}
        relaciones={relacionesParentales}
        esPadre={esPadre}
        esHijo={esHijo}
        editando={datosPersonales.editando}
        setEditando={datosPersonales.setEditando}
        formDatos={datosPersonales.formDatos}
        errorDatos={datosPersonales.errorDatos}
        exitoDatos={datosPersonales.exitoDatos}
        cargandoDatos={datosPersonales.cargandoDatos}
        onChange={datosPersonales.handleChangeDatos}
        onGuardar={datosPersonales.handleGuardarDatos}
        onCancelar={datosPersonales.handleCancelarEdicion}
      />

      <SeccionDesvincularPadre
        relacion={relacionComoHijo}
      />

      <div className="tarjeta-seccion-perfil">
        <div className="encabezado-seccion-perfil">
          <h3 className="titulo-seccion-perfil">
            Seguridad
          </h3>
        </div>

        <div className="fila-dato-perfil">
          <div>
            <span className="etiqueta-dato-perfil">
              Contraseña
            </span>

            <p className="descripcion-seguridad-perfil">
              Actualiza tu contraseña periódicamente para
              mantener tu cuenta segura.
            </p>
          </div>

          <button
            type="button"
            className="boton-secundario-perfil"
            onClick={() =>
              cambiarPassword.setModalPassword(true)
            }
          >
            Cambiar contraseña
          </button>
        </div>
      </div>

      <ModalCambiarPassword
        open={cambiarPassword.modalPassword}
        onClose={cambiarPassword.handleCerrarModalPassword}
        formPassword={cambiarPassword.formPassword}
        errorPassword={cambiarPassword.errorPassword}
        exitoPassword={cambiarPassword.exitoPassword}
        cargandoPassword={cambiarPassword.cargandoPassword}
        onChange={cambiarPassword.handleChangePassword}
        onGuardar={cambiarPassword.handleGuardarPassword}
      />
    </div>
  );
};

export default PerfilPage;
