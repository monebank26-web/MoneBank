// features/auth/pages/LoginPage.jsx
// features/auth/pages/LoginPage.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm';
import './Auth.css';

const LoginPage = () => {
  const { submit, loading, error } = useAuthForm('login');
  const [form, setForm] = useState({ email: '', password: '' });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submit(form);
  };

return (
  <div className="contenedor-autenticacion">
    <video id="video-fondo-pantalla" autoPlay muted loop>
      <source src="/video.mp4" type="video/mp4" />
    </video>
    <div className="capa-oscura-video" />
      <div className="tarjeta-autenticacion">
        <div className="marca-autenticacion">
          <img src="/logo.png" alt="MoneBank logo" className="imagen-logo-autenticacion" />
          <h1 className="titulo-autenticacion">MoneBank</h1>
          <p className="subtitulo-autenticacion">Ingresa a tu cuenta</p>
        </div>

        <form onSubmit={handleSubmit} className="formulario-autenticacion">
          <div className="grupo-campo">
            <label className="etiqueta-campo">Correo electrónico</label>
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
            <label className="etiqueta-campo">Contraseña</label>
            <input
              className="campo-entrada"
              type="password"
              name="password"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              required
            />
          </div>

          {error && <p className="error-autenticacion">{error}</p>}

          <button className="boton-principal" type="submit" disabled={loading}>
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>

        <p className="texto-cambio-autenticacion">
          ¿No tienes cuenta?{' '}
          <Link to="/register" className="enlace-autenticacion">
            Regístrate
          </Link>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;