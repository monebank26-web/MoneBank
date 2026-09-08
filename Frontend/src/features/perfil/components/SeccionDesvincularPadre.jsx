import React, { useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { controlParentalService } from '../../controlParental/services/controlParentalServices';

const SeccionDesvincularPadre = ({ relacion }) => {
  const { user } = useAuth();

  const [correoPadre, setCorreoPadre] = useState('');
  const [codigo, setCodigo] = useState('');
  const [codigoEnviado, setCodigoEnviado] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [mensaje, setMensaje] = useState('');
  const [error, setError] = useState('');

  const esHijo =
    relacion &&
    Number(relacion.id_usuario_dependiente) ===
      Number(user?.id);

  if (!esHijo) {
    return null;
  }

  const solicitarCodigo = async (event) => {
    event.preventDefault();

    setError('');
    setMensaje('');
    setCargando(true);

    try {
      await controlParentalService.solicitarDesvinculacion(
        correoPadre.trim()
      );

      setCodigoEnviado(true);

      setMensaje(
        'El código fue enviado al correo del padre. Ingrésalo aquí para confirmar la desvinculación.'
      );
    } catch (err) {
      setError(
        err.message ||
          'El correo no corresponde al padre vinculado.'
      );
    } finally {
      setCargando(false);
    }
  };

  const confirmarDesvinculacion = async (event) => {
    event.preventDefault();

    setError('');
    setMensaje('');
    setCargando(true);

    try {
      await controlParentalService.confirmarDesvinculacion(
        codigo
      );

      setCodigo('');
      setCorreoPadre('');
      setCodigoEnviado(false);

      setMensaje(
        'Tu cuenta fue desvinculada correctamente.'
      );
    } catch (err) {
      setError(
        err.message ||
          'El código es inválido o expiró.'
      );
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="tarjeta-seccion-perfil seccion-desvincular-padre">
      <div className="encabezado-seccion-perfil">
        <h3 className="titulo-seccion-perfil">
          Desvincular cuenta parental
        </h3>

        <p className="descripcion-seguridad-perfil">
          Esta opción solo está disponible para cuentas hijas.
        </p>
      </div>

      {!codigoEnviado ? (
        <form
          className="formulario-desvincular-padre"
          onSubmit={solicitarCodigo}
        >
          <label htmlFor="correo-padre-desvincular">
            Correo del padre o madre
          </label>

          <div className="fila-formulario-desvincular-padre">
            <input
              id="correo-padre-desvincular"
              type="email"
              value={correoPadre}
              onChange={(event) =>
                setCorreoPadre(event.target.value)
              }
              placeholder="padre@correo.com"
              required
            />

            <button type="submit" disabled={cargando}>
              {cargando
                ? 'Enviando...'
                : 'Enviar código'}
            </button>
          </div>
        </form>
      ) : (
        <form
          className="formulario-desvincular-padre"
          onSubmit={confirmarDesvinculacion}
        >
          <label htmlFor="codigo-desvincular">
            Código enviado al correo del padre
          </label>

          <div className="fila-formulario-desvincular-padre">
            <input
              id="codigo-desvincular"
              type="text"
              inputMode="numeric"
              maxLength="6"
              pattern="[0-9]{6}"
              value={codigo}
              onChange={(event) =>
                setCodigo(
                  event.target.value
                    .replace(/\D/g, '')
                    .slice(0, 6)
                )
              }
              placeholder="000000"
              required
            />

            <button
              type="submit"
              disabled={cargando || codigo.length !== 6}
            >
              {cargando
                ? 'Validando...'
                : 'Confirmar desvinculación'}
            </button>
          </div>

          <button
            type="button"
            className="boton-cambiar-correo-desvincular"
            onClick={() => {
              setCodigoEnviado(false);
              setCodigo('');
              setMensaje('');
              setError('');
            }}
          >
            Usar otro correo
          </button>
        </form>
      )}

      {mensaje && (
        <p className="mensaje-desvincular-padre mensaje-desvincular-padre--ok">
          {mensaje}
        </p>
      )}

      {error && (
        <p className="mensaje-desvincular-padre mensaje-desvincular-padre--error">
          {error}
        </p>
      )}
    </div>
  );
};

export default SeccionDesvincularPadre;
