import React from 'react';
import { useDatosPersonales } from '../hooks/useDatosPersonales';
import { useCambiarPassword } from '../hooks/useCambiarPassword';
import TarjetaResumenPerfil from '../components/TarjetaResumenPerfil';
import SeccionDatosPersonales from '../components/SeccionDatosPersonales';
import ModalCambiarPassword from '../components/ModalCambiarPassword';
import './PerfilPage.css';

const PerfilPage = () => {
  const datosPersonales = useDatosPersonales();
  const cambiarPassword = useCambiarPassword();

  return (
    <div className="pagina-perfil">
      <div className="encabezado-perfil">
        <h1 className="titulo-perfil">Mi perfil</h1>
        <p className="subtitulo-perfil">Consulta y modifica la información de tu cuenta.</p>
      </div>

      <TarjetaResumenPerfil user={datosPersonales.user} />

      <SeccionDatosPersonales
        user={datosPersonales.user}
        editando={datosPersonales.editando}
        setEditando={datosPersonales.setEditando}
        formDatos={datosPersonales.formDatos}
        errorDatos={datosPersonales.errorDatos}
        exitoDatos={datosPersonales.exitoDatos}
        onChange={datosPersonales.handleChangeDatos}
        onGuardar={datosPersonales.handleGuardarDatos}
        onCancelar={datosPersonales.handleCancelarEdicion}
      />

      <div className="tarjeta-seccion-perfil">
        <div className="encabezado-seccion-perfil">
          <h3 className="titulo-seccion-perfil">Seguridad</h3>
        </div>
        <div className="fila-dato-perfil">
          <div>
            <span className="etiqueta-dato-perfil">Contraseña</span>
            <p className="descripcion-seguridad-perfil">Actualiza tu contraseña periódicamente para mantener tu cuenta segura.</p>
          </div>
          <button className="boton-secundario-perfil" onClick={() => cambiarPassword.setModalPassword(true)}>
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
