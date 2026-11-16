import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../../core/constants';
import CampoContrasena from '../../../shared/components/CampoContrasena';
import { useEnfriamientoCodigo } from '../hooks/useEnfriamientoCodigo';
import { authService } from '../services/authService';
import {
  AVISO_CODIGO_ADMINISTRADOR,
  MENSAJE_CODIGO_ENVIADO,
  MENSAJE_RECUPERACION_EXITOSA,
  SEGUNDOS_ENFRIAMIENTO_CODIGO,
  codigoRecuperacionValido,
  contrasenasCoinciden,
  mensajeErrorRecuperacion,
  normalizarCodigoRecuperacion,
  textoBotonReenvio,
} from '../utils/recuperacionPassword';
import './Auth.css';

const RecuperarPasswordPage = () => {
  const [paso, setPaso] = useState('solicitar');
  const [email, setEmail] = useState('');
  const [codigo, setCodigo] = useState('');
  const [nuevaContrasena, setNuevaContrasena] = useState('');
  const [confirmarContrasena, setConfirmarContrasena] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const {
    segundosRestantes,
    enfriamientoActivo,
    iniciarEnfriamiento,
  } = useEnfriamientoCodigo(SEGUNDOS_ENFRIAMIENTO_CODIGO);

  const irACodigoExistente = () => {
    setError('');
    setMensaje('');
    setPaso('confirmar');
  };

  const solicitarCodigo = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const correo = email.trim().toLowerCase();
      await authService.solicitarCodigoRecuperacion({ email: correo });
      setEmail(correo);
      setMensaje(MENSAJE_CODIGO_ENVIADO);
      iniciarEnfriamiento();
      setPaso('confirmar');
    } catch (err) {
      setError(mensajeErrorRecuperacion(err));
    } finally {
      setLoading(false);
    }
  };

  const confirmarCodigo = async (event) => {
    event.preventDefault();
    setError('');

    const correo = email.trim().toLowerCase();

    if (!correo) {
      setError('Escribe tu correo electrónico.');
      return;
    }

    if (!codigoRecuperacionValido(codigo)) {
      setError('Escribe el código de 6 dígitos.');
      return;
    }

    if (!contrasenasCoinciden(nuevaContrasena, confirmarContrasena)) {
      setError('Las contraseñas no coinciden.');
      return;
    }

    setLoading(true);

    try {
      await authService.confirmarCodigoRecuperacion({
        email: correo,
        codigo,
        nuevaContrasena,
      });
      setEmail(correo);
      setPaso('listo');
    } catch (err) {
      setError(mensajeErrorRecuperacion(err));
    } finally {
      setLoading(false);
    }
  };

  const reenviarCodigo = async () => {
    if (loading || enfriamientoActivo) return;

    const correo = email.trim().toLowerCase();

    if (!correo) {
      setError('Escribe tu correo electrónico.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await authService.solicitarCodigoRecuperacion({ email: correo });
      setEmail(correo);
      setMensaje(MENSAJE_CODIGO_ENVIADO);
      iniciarEnfriamiento();
    } catch (err) {
      setError(mensajeErrorRecuperacion(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="contenedor-autenticacion">
      <video id="video-fondo-pantalla" autoPlay muted loop>
        <source src="/video.mp4" type="video/mp4" />
      </video>

      <div className="capa-oscura-video" />

      <div className="tarjeta-autenticacion">
        <div className="marca-autenticacion">
          <img
            src="/logo.png"
            alt="MoneBank logo"
            className="imagen-logo-autenticacion"
          />

          <h1 className="titulo-autenticacion">MoneBank</h1>

          <p className="subtitulo-autenticacion">
            {paso === 'solicitar' && 'Recupera tu contraseña'}
            {paso === 'confirmar' && 'Escribe el código recibido'}
            {paso === 'listo' && 'Contraseña restablecida'}
          </p>
        </div>

        {paso === 'solicitar' && (
          <form
            onSubmit={solicitarCodigo}
            className="formulario-autenticacion"
          >
            <p className="recuperacion-nota">
              Ingresa tu correo y te enviaremos un código de 6 dígitos.
            </p>

            <p className="recuperacion-mensaje">
              {AVISO_CODIGO_ADMINISTRADOR}
            </p>

            <div className="grupo-campo">
              <label className="etiqueta-campo" htmlFor="recuperar-email">
                Correo electrónico
              </label>

              <input
                id="recuperar-email"
                className="campo-entrada"
                type="email"
                placeholder="tu@correo.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                autoComplete="email"
                required
              />
            </div>

            {error && (
              <p className="error-autenticacion" role="alert">
                {error}
              </p>
            )}

            <button
              className="boton-principal"
              type="submit"
              disabled={loading || enfriamientoActivo}
            >
              {loading ? 'Enviando...' : 'Enviarme un código'}
            </button>

            <button
              type="button"
              className="enlace-autenticacion recuperacion-enlace"
              onClick={irACodigoExistente}
            >
              Ya tengo un código
            </button>
          </form>
        )}

        {paso === 'confirmar' && (
          <form
            onSubmit={confirmarCodigo}
            className="formulario-autenticacion"
          >
            {mensaje && (
              <p className="recuperacion-mensaje" role="status" aria-live="polite">
                {mensaje}
              </p>
            )}

            <div className="grupo-campo">
              <label
                className="etiqueta-campo"
                htmlFor="recuperar-email-confirmar"
              >
                Correo electrónico
              </label>

              <input
                id="recuperar-email-confirmar"
                className="campo-entrada"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                autoComplete="email"
                required
              />
            </div>

            <div className="grupo-campo">
              <label className="etiqueta-campo" htmlFor="recuperar-codigo">
                Código de 6 dígitos
              </label>

              <input
                id="recuperar-codigo"
                className="campo-entrada recuperacion-codigo"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                placeholder="000000"
                value={codigo}
                onChange={(event) =>
                  setCodigo(normalizarCodigoRecuperacion(event.target.value))
                }
                pattern="\d{6}"
                required
              />
            </div>

            <div className="grupo-campo">
              <label className="etiqueta-campo" htmlFor="recuperar-password">
                Nueva contraseña
              </label>

              <CampoContrasena
                id="recuperar-password"
                name="nueva-contrasena"
                placeholder="••••••••"
                value={nuevaContrasena}
                onChange={(event) => setNuevaContrasena(event.target.value)}
                autoComplete="new-password"
                required
              />

              <small className="recuperacion-ayuda">
                Mínimo 8 caracteres, con mayúscula, minúscula, número y símbolo.
              </small>
            </div>

            <div className="grupo-campo">
              <label className="etiqueta-campo" htmlFor="recuperar-confirmar">
                Confirmar contraseña
              </label>

              <CampoContrasena
                id="recuperar-confirmar"
                name="confirmar-contrasena"
                placeholder="••••••••"
                value={confirmarContrasena}
                onChange={(event) =>
                  setConfirmarContrasena(event.target.value)
                }
                autoComplete="new-password"
                required
              />
            </div>

            {error && (
              <p className="error-autenticacion" role="alert">
                {error}
              </p>
            )}

            <button
              className="boton-principal"
              type="submit"
              disabled={loading}
            >
              {loading ? 'Restableciendo...' : 'Restablecer contraseña'}
            </button>

            <button
              type="button"
              className="boton-secundario"
              onClick={reenviarCodigo}
              disabled={loading || enfriamientoActivo}
            >
              {enfriamientoActivo
                ? textoBotonReenvio(segundosRestantes)
                : 'Reenviar código'}
            </button>
          </form>
        )}

        {paso === 'listo' && (
          <div className="recuperacion-exito" role="status" aria-live="polite">
            <p>{MENSAJE_RECUPERACION_EXITOSA}</p>

            <Link
              to={ROUTES.LOGIN}
              state={{ mensajeRecuperacion: MENSAJE_RECUPERACION_EXITOSA }}
              className="boton-principal recuperacion-volver"
            >
              Ir a iniciar sesión
            </Link>
          </div>
        )}

        {paso !== 'listo' && (
          <p className="texto-cambio-autenticacion">
            <Link to={ROUTES.LOGIN} className="enlace-autenticacion">
              Volver a iniciar sesión
            </Link>
          </p>
        )}
      </div>
    </div>
  );
};

export default RecuperarPasswordPage;
