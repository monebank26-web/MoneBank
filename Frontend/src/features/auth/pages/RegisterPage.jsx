import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm';
import { CORREO_ADMIN, ROLES } from '../../../core/constants';
import './Auth.css';
import CampoContrasena from '../../../shared/components/CampoContrasena';

const evaluarSeguridadPassword = (password) => {
  if (!password) {
    return {
      nivel: '',
      texto: '',
      porcentaje: 0,
    };
  }

  let puntos = 0;

  if (password.length >= 8) puntos += 1;
  if (password.length >= 12) puntos += 1;
  if (/[A-Z]/.test(password)) puntos += 1;
  if (/[a-z]/.test(password)) puntos += 1;
  if (/[0-9]/.test(password)) puntos += 1;
  if (/[^A-Za-z0-9]/.test(password)) puntos += 1;

  if (puntos <= 2) {
    return {
      nivel: 'debil',
      texto: 'Contraseña débil',
      porcentaje: 25,
    };
  }

  if (puntos <= 4) {
    return {
      nivel: 'media',
      texto: 'Contraseña media',
      porcentaje: 55,
    };
  }

  if (puntos === 5) {
    return {
      nivel: 'fuerte',
      texto: 'Contraseña fuerte',
      porcentaje: 80,
    };
  }

  return {
    nivel: 'muy-fuerte',
    texto: 'Contraseña muy segura',
    porcentaje: 100,
  };
};

const IconoOjo = ({ cerrado = false }) => (
  <svg
    viewBox="0 0 24 24"
    aria-hidden="true"
    className="icono-ojo"
  >
    {cerrado ? (
      <>
        <path
          d="M3 3l18 18"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M10.6 10.6a2 2 0 0 0 2.8 2.8"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M9.9 5.2A10.8 10.8 0 0 1 12 5c5.2 0 8.8 5 9.5 7-.3.8-1.3 2.5-2.9 3.9M6.2 6.2C4.2 7.6 2.9 9.8 2.5 12c.7 2 4.3 7 9.5 7 1.1 0 2.1-.2 3-.6"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </>
    ) : (
      <>
        <path
          d="M2.5 12S6.3 5 12 5s9.5 7 9.5 7-3.8 7-9.5 7-9.5-7-9.5-7Z"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinejoin="round"
        />
        <circle
          cx="12"
          cy="12"
          r="2.8"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        />
      </>
    )}
  </svg>
);

const RegisterPage = () => {
  const { submit, loading, error } =
    useAuthForm('register');

  const [form, setForm] = useState({
    nombres: '',
    apellidos: '',
    email: '',
    password: '',
    confirmar: '',
  });

  const [mostrarPassword, setMostrarPassword] =
    useState(false);

  const [
    mostrarConfirmar,
    setMostrarConfirmar,
  ] = useState(false);

  const [localError, setLocalError] =
    useState('');

  const esAdmin = form.email === CORREO_ADMIN;

  const seguridadPassword =
    evaluarSeguridadPassword(form.password);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleRegistro = (e) => {
    e.preventDefault();
    setLocalError('');

    if (
      !form.nombres.trim() ||
      !form.apellidos.trim() ||
      !form.email.trim() ||
      !form.password ||
      !form.confirmar
    ) {
      setLocalError(
        'Por favor completa todos los campos.'
      );
      return;
    }

    if (form.password !== form.confirmar) {
      setLocalError(
        'Las contraseñas no coinciden.'
      );
      return;
    }

    submit({
      nombres: form.nombres.trim(),
      apellidos: form.apellidos.trim(),
      email: form.email.trim().toLowerCase(),
      password: form.password,
      rol: esAdmin
        ? ROLES.ADMIN
        : ROLES.INDEPENDIENTE,
      esMenor: false,
    });
  };

  return (
    <div className="contenedor-autenticacion">
      <video
        id="video-fondo-pantalla"
        autoPlay
        muted
        loop
      >
        <source
          src="/video.mp4"
          type="video/mp4"
        />
      </video>

      <div className="capa-oscura-video" />

      <div className="tarjeta-autenticacion">
        <div className="marca-autenticacion">
          <img
            src="/logo.png"
            alt="MoneBank logo"
            className="imagen-logo-autenticacion"
          />

          <h1 className="titulo-autenticacion">
            MoneBank
          </h1>

          <p className="subtitulo-autenticacion">
            Crea tu cuenta
          </p>
        </div>

        <form
          onSubmit={handleRegistro}
          className="formulario-autenticacion"
        >
          <div className="grupo-campo">
            <label className="etiqueta-campo">
              Nombres
            </label>

            <input
              className="campo-entrada"
              type="text"
              name="nombres"
              placeholder="Tus nombres"
              value={form.nombres}
              onChange={handleChange}
              required
            />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">
              Apellidos
            </label>

            <input
              className="campo-entrada"
              type="text"
              name="apellidos"
              placeholder="Tus apellidos"
              value={form.apellidos}
              onChange={handleChange}
              required
            />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">
              Correo electrónico
            </label>

            <input
              className="campo-entrada"
              type="email"
              name="email"
              placeholder="tu@correo.com"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">
              Contraseña
            </label>

            <div className="campo-password-wrapper">
              <input
                className="campo-entrada campo-password"
                type={
                  mostrarPassword
                    ? 'text'
                    : 'password'
                }
                name="password"
                placeholder="••••••••"
                value={form.password}
                onChange={handleChange}
                required
              />

              <button
                type="button"
                className="boton-mostrar-password"
                onClick={() =>
                  setMostrarPassword(
                    (visible) => !visible
                  )
                }
                aria-label={
                  mostrarPassword
                    ? 'Ocultar contraseña'
                    : 'Mostrar contraseña'
                }
                title={
                  mostrarPassword
                    ? 'Ocultar contraseña'
                    : 'Mostrar contraseña'
                }
              >
                <IconoOjo
                  cerrado={!mostrarPassword}
                />
              </button>
            </div>

            {form.password && (
              <div
                className="indicador-password"
                aria-live="polite"
              >
                <div className="termometro-password">
                  <span
                    className={`termometro-password-fill ${seguridadPassword.nivel}`}
                    style={{
                      width: `${seguridadPassword.porcentaje}%`,
                    }}
                  />
                </div>

                <span
                  className={`texto-seguridad-password ${seguridadPassword.nivel}`}
                >
                  {seguridadPassword.texto}
                </span>

                <ul className="requisitos-password">
                  <li
                    className={
                      form.password.length >= 8
                        ? 'cumplido'
                        : ''
                    }
                  >
                    Mínimo 8 caracteres
                  </li>

                  <li
                    className={
                      /[A-Z]/.test(form.password)
                        ? 'cumplido'
                        : ''
                    }
                  >
                    Una letra mayúscula
                  </li>

                  <li
                    className={
                      /[a-z]/.test(form.password)
                        ? 'cumplido'
                        : ''
                    }
                  >
                    Una letra minúscula
                  </li>

                  <li
                    className={
                      /[0-9]/.test(form.password)
                        ? 'cumplido'
                        : ''
                    }
                  >
                    Un número
                  </li>

                  <li
                    className={
                      /[^A-Za-z0-9]/.test(
                        form.password
                      )
                        ? 'cumplido'
                        : ''
                    }
                  >
                    Un símbolo
                  </li>
                </ul>
              </div>
            )}
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">
              Confirmar contraseña
            </label>

            <div className="campo-password-wrapper">
              <input
                className="campo-entrada campo-password"
                type={
                  mostrarConfirmar
                    ? 'text'
                    : 'password'
                }
                name="confirmar"
                placeholder="••••••••"
                value={form.confirmar}
                onChange={handleChange}
                required
              />

              <button
                type="button"
                className="boton-mostrar-password"
                onClick={() =>
                  setMostrarConfirmar(
                    (visible) => !visible
                  )
                }
                aria-label={
                  mostrarConfirmar
                    ? 'Ocultar confirmación'
                    : 'Mostrar confirmación'
                }
                title={
                  mostrarConfirmar
                    ? 'Ocultar confirmación'
                    : 'Mostrar confirmación'
                }
              >
                <IconoOjo
                  cerrado={!mostrarConfirmar}
                />
              </button>
            </div>

            {form.confirmar &&
              form.password !== form.confirmar && (
                <small className="mensaje-password-no-coincide">
                  Las contraseñas no coinciden.
                </small>
              )}
          </div>

          {(error || localError) && (
            <p className="error-autenticacion">
              {localError || error}
            </p>
          )}

          <button
            className="boton-principal"
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Creando cuenta...'
              : esAdmin
                ? 'Crear cuenta de administrador'
                : 'Crear cuenta'}
          </button>
        </form>

        <p className="texto-cambio-autenticacion">
          ¿Ya tienes cuenta?{' '}
          <Link
            to="/login"
            className="enlace-autenticacion"
          >
            Ingresar
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
