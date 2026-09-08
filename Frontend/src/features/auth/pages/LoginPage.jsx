import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm';
import './Auth.css';

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

const LoginPage = () => {
  const { submit, loading, error } =
    useAuthForm('login');

  const [form, setForm] = useState({
    email: '',
    password: '',
  });

  const [mostrarPassword, setMostrarPassword] =
    useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    submit({
      email: form.email.trim().toLowerCase(),
      password: form.password,
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
            Ingresa a tu cuenta
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="formulario-autenticacion"
        >
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
          </div>

          {error && (
            <p className="error-autenticacion">
              {error}
            </p>
          )}

          <button
            className="boton-principal"
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Ingresando...'
              : 'Ingresar'}
          </button>
        </form>

        <p className="texto-cambio-autenticacion">
          ¿No tienes cuenta?{' '}

          <Link
            to="/register"
            className="enlace-autenticacion"
          >
            Regístrate
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
