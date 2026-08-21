import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthForm } from '../hooks/useAuthForm';
import { CORREO_ADMIN, ROLES } from '../../../core/constants';
import './Auth.css';

const RegisterPage = () => {
  const { submit, loading, error } = useAuthForm('register');
  const [form, setForm] = useState({
    nombres: '',
    apellidos: '',
    email: '',
    password: '',
    confirmar: '',
    saldoInicial: '',
  });
  const [localError, setLocalError] = useState('');
  const [paso, setPaso] = useState(1); // 1 = datos básicos, 2 = tipo de cuenta
  const [tipoCuenta, setTipoCuenta] = useState(null); // 'padre', 'hijo', 'normal'
  const [esMenor, setEsMenor] = useState(null);

  const esAdmin = form.email === CORREO_ADMIN;

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSiguiente = (e) => {
    e.preventDefault();
    setLocalError('');
    if (!form.nombres || !form.apellidos || !form.email || !form.password || !form.confirmar || !form.saldoInicial) {
      setLocalError('Por favor completa todos los campos.');
      return;
    }
    if (form.password !== form.confirmar) {
      setLocalError('Las contraseñas no coinciden.');
      return;
    }
    if (esAdmin) {
      // El admin no necesita elegir tipo de cuenta
      enviarRegistro(ROLES.ADMIN, false);
      return;
    }
    setPaso(2);
  };

  const enviarRegistro = (rol, menor) => {
    submit({
      nombres: form.nombres,
      apellidos: form.apellidos,
      email: form.email,
      password: form.password,
      saldoInicial: parseInt(form.saldoInicial, 10) || 0,
      rol: rol,
      esMenor: menor,
    });
  };

  const handleElegirTipo = (tipo) => {
    setTipoCuenta(tipo);
    if (tipo === 'normal') {
      enviarRegistro(ROLES.NORMAL, false);
    } else if (tipo === 'padre') {
      enviarRegistro(ROLES.PADRE, false);
    }
    // Si es hijo, preguntamos si es menor
  };

  const handleConfirmarHijo = () => {
    if (esMenor === null) {
      setLocalError('Por favor indica si eres menor de edad.');
      return;
    }
    enviarRegistro(ROLES.HIJO, esMenor);
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
          <p className="subtitulo-autenticacion">
            {paso === 1 ? 'Crea tu cuenta' : 'Tipo de cuenta'}
          </p>
        </div>

        {/* Paso 1: datos básicos */}
        {paso === 1 && (
          <form onSubmit={handleSiguiente} className="formulario-autenticacion">
            <div className="grupo-campo">
              <label className="etiqueta-campo">Nombres</label>
              <input className="campo-entrada" type="text" name="nombres"
                placeholder="Tus nombres" value={form.nombres} onChange={handleChange} required />
            </div>
            <div className="grupo-campo">
              <label className="etiqueta-campo">Apellidos</label>
              <input className="campo-entrada" type="text" name="apellidos"
                placeholder="Tus apellidos" value={form.apellidos} onChange={handleChange} required />
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
              {loading ? 'Creando cuenta...' : esAdmin ? 'Crear cuenta de administrador' : 'Siguiente'}
            </button>
          </form>
        )}

        {/* Paso 2: tipo de cuenta */}
        {paso === 2 && !tipoCuenta && (
          <div className="formulario-autenticacion">
            <p className="subtexto-tipo-cuenta">¿Cómo vas a usar tu cuenta?</p>
            <div className="opciones-tipo-cuenta">
              <button className="opcion-tipo-cuenta" onClick={() => handleElegirTipo('normal')}>
                <span className="icono-tipo-cuenta">👤</span>
                <span className="nombre-tipo-cuenta">Cuenta normal</span>
                <span className="descripcion-tipo-cuenta">Solo yo manejo mi dinero</span>
              </button>
              <button className="opcion-tipo-cuenta" onClick={() => handleElegirTipo('padre')}>
                <span className="icono-tipo-cuenta">👨‍👧</span>
                <span className="nombre-tipo-cuenta">Soy padre o madre</span>
                <span className="descripcion-tipo-cuenta">Quiero vincular la cuenta de mi hijo</span>
              </button>
              <button className="opcion-tipo-cuenta" onClick={() => setTipoCuenta('hijo')}>
                <span className="icono-tipo-cuenta">🧒</span>
                <span className="nombre-tipo-cuenta">Soy hijo o hija</span>
                <span className="descripcion-tipo-cuenta">Quiero vincularme a la cuenta de mis padres</span>
              </button>
            </div>
            {localError && <p className="error-autenticacion">{localError}</p>}
            <button className="boton-secundario" onClick={() => setPaso(1)}>← Volver</button>
          </div>
        )}

        {/* Paso 2b: si es hijo, preguntar edad */}
        {paso === 2 && tipoCuenta === 'hijo' && (
          <div className="formulario-autenticacion">
            <p className="subtexto-tipo-cuenta">¿Cuántos años tienes?</p>
            <div className="opciones-tipo-cuenta">
              <button
                className={`opcion-tipo-cuenta ${esMenor === true ? 'opcion-tipo-cuenta--seleccionada' : ''}`}
                onClick={() => setEsMenor(true)}
              >
                <span className="icono-tipo-cuenta">🔒</span>
                <span className="nombre-tipo-cuenta">Soy menor de 18 años</span>
                <span className="descripcion-tipo-cuenta">Mis padres tendrán acceso a mi cuenta</span>
              </button>
              <button
                className={`opcion-tipo-cuenta ${esMenor === false ? 'opcion-tipo-cuenta--seleccionada' : ''}`}
                onClick={() => setEsMenor(false)}
              >
                <span className="icono-tipo-cuenta">✅</span>
                <span className="nombre-tipo-cuenta">Tengo 18 años o más</span>
                <span className="descripcion-tipo-cuenta">Acepto vincularme voluntariamente</span>
              </button>
            </div>
            {localError && <p className="error-autenticacion">{localError}</p>}
            {error && <p className="error-autenticacion">{error}</p>}
            <button className="boton-principal" onClick={handleConfirmarHijo} disabled={loading}>
              {loading ? 'Creando cuenta...' : 'Crear cuenta'}
            </button>
            <button className="boton-secundario" onClick={() => setTipoCuenta(null)}>← Volver</button>
          </div>
        )}

        <p className="texto-cambio-autenticacion">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="enlace-autenticacion">Ingresar</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
