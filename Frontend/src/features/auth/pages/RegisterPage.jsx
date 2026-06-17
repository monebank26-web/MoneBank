/// features/auth/pages/RegisterPage.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm';
import './Auth.css';

const RegisterPage = () => {
  const { submit, loading, error } = useAuthForm('register');
  const [form, setForm] = useState({ nombre: '', email: '', password: '', confirmar: '', saldoInicial: '' });
  const [localError, setLocalError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLocalError('');
    if (form.password !== form.confirmar) {
      setLocalError('Las contraseñas no coinciden.');
      return;
    }
    submit({
      nombre: form.nombre,
      email: form.email,
      password: form.password,
      saldoInicial: parseInt(form.saldoInicial, 10) || 0,
    });
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
          <p className="subtitulo-autenticacion">Crea tu cuenta</p>
        </div>

        <form onSubmit={handleSubmit} className="formulario-autenticacion">
          <div className="grupo-campo">
            <label className="etiqueta-campo">Nombre completo</label>
            <input className="campo-entrada" type="text" name="nombre"
              placeholder="Tu nombre" value={form.nombre} onChange={handleChange} required />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">Correo electrónico</label>
            <input className="campo-entrada" type="email" name="email"
              placeholder="tu@correo.com" value={form.email} onChange={handleChange} required />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">Contraseña</label>
            <input className="campo-entrada" type="password" name="password"
              placeholder="••••••••" value={form.password} onChange={handleChange} required />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">Confirmar contraseña</label>
            <input className="campo-entrada" type="password" name="confirmar"
              placeholder="••••••••" value={form.confirmar} onChange={handleChange} required />
          </div>

          <div className="grupo-campo">
            <label className="etiqueta-campo">Saldo inicial de Mi Cuenta (COP)</label>
            <input className="campo-entrada" type="number" name="saldoInicial"
              placeholder="Ej: 500000" min="0" value={form.saldoInicial} onChange={handleChange} required />
          </div>

          {(error || localError) && <p className="error-autenticacion">{localError || error}</p>}

          <button className="boton-principal" type="submit" disabled={loading}>
            {loading ? 'Creando cuenta...' : 'Crear cuenta'}
          </button>
        </form>

        <p className="texto-cambio-autenticacion">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="enlace-autenticacion">Ingresar</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;