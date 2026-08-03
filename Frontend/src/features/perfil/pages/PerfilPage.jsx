import React, { useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';
import Modal from '../../../shared/components/Modal';
import { ROLES } from '../../../core/constants';
import './PerfilPage.css';

const formatFecha = (iso) => {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString('es-CO', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
};

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val || 0);

const etiquetaRol = {
  administrador: '👑 Administrador',
  padre: '👨‍👧 Padre/Madre',
  hijo: '🧒 Hijo/Hija',
  normal: '👤 Cuenta normal',
};

const PerfilPage = () => {
  const { user, login } = useAuth();

  // ── Edición de datos básicos ──
  const [editando, setEditando] = useState(false);
  const [formDatos, setFormDatos] = useState({ nombre: user?.nombre || '', email: user?.email || '' });
  const [errorDatos, setErrorDatos] = useState('');
  const [exitoDatos, setExitoDatos] = useState('');

  // ── Cambio de contraseña ──
  const [modalPassword, setModalPassword] = useState(false);
  const [formPassword, setFormPassword] = useState({ actual: '', nueva: '', confirmar: '' });
  const [errorPassword, setErrorPassword] = useState('');
  const [exitoPassword, setExitoPassword] = useState('');
  const [cargandoPassword, setCargandoPassword] = useState(false);

  const iniciales = user?.nombre?.charAt(0).toUpperCase() || 'U';

  const handleChangeDatos = (e) => {
    setFormDatos({ ...formDatos, [e.target.name]: e.target.value });
    setExitoDatos('');
  };

  const handleGuardarDatos = (e) => {
    e.preventDefault();
    setErrorDatos('');
    setExitoDatos('');

    if (!formDatos.nombre.trim() || !formDatos.email.trim()) {
      setErrorDatos('El nombre y el correo no pueden quedar vacíos.');
      return;
    }

    // Si cambia el correo, verificar que no esté en uso por otra cuenta
    if (formDatos.email !== user.email) {
      const existente = authService.obtenerUsuarioPorCorreo(formDatos.email);
      if (existente && existente.id !== user.id) {
        setErrorDatos('Ese correo ya está en uso por otra cuenta.');
        return;
      }
    }

    authService.actualizarUsuario(user.id, {
      nombre: formDatos.nombre.trim(),
      email: formDatos.email.trim(),
    });
    login({ ...user, nombre: formDatos.nombre.trim(), email: formDatos.email.trim() });
    setEditando(false);
    setExitoDatos('Tus datos se actualizaron correctamente.');
  };

  const handleCancelarEdicion = () => {
    setFormDatos({ nombre: user?.nombre || '', email: user?.email || '' });
    setErrorDatos('');
    setEditando(false);
  };

  const handleChangePassword = (e) => {
    setFormPassword({ ...formPassword, [e.target.name]: e.target.value });
  };

  const handleCerrarModalPassword = () => {
    setModalPassword(false);
    setFormPassword({ actual: '', nueva: '', confirmar: '' });
    setErrorPassword('');
  };

  const handleGuardarPassword = async (e) => {
    e.preventDefault();
    setErrorPassword('');

    if (!formPassword.actual || !formPassword.nueva || !formPassword.confirmar) {
      setErrorPassword('Completa todos los campos.');
      return;
    }
    if (formPassword.nueva.length < 4) {
      setErrorPassword('La nueva contraseña debe tener al menos 4 caracteres.');
      return;
    }
    if (formPassword.nueva !== formPassword.confirmar) {
      setErrorPassword('Las contraseñas nuevas no coinciden.');
      return;
    }

    setCargandoPassword(true);
    try {
      authService.cambiarPassword(user.id, formPassword.actual, formPassword.nueva);
      setExitoPassword('Contraseña actualizada correctamente.');
      setTimeout(() => {
        handleCerrarModalPassword();
        setExitoPassword('');
      }, 1200);
    } catch (err) {
      setErrorPassword(err.message);
    } finally {
      setCargandoPassword(false);
    }
  };

  return (
    <div className="pagina-perfil">
      <div className="encabezado-perfil">
        <h1 className="titulo-perfil">Mi perfil</h1>
        <p className="subtitulo-perfil">Consulta y modifica la información de tu cuenta.</p>
      </div>

      {/* Tarjeta de resumen */}
      <div className="tarjeta-resumen-perfil">
        <div className="avatar-perfil">{iniciales}</div>
        <div className="info-resumen-perfil">
          <h2 className="nombre-resumen-perfil">{user?.nombre}</h2>
          <p className="correo-resumen-perfil">{user?.email}</p>
          <span className="chip-rol-perfil">{etiquetaRol[user?.rol] || user?.rol}</span>
        </div>
        {user?.rol !== ROLES.ADMIN && (
          <div className="saldo-resumen-perfil">
            <p className="etiqueta-saldo-perfil">Saldo en Mi Cuenta</p>
            <p className="valor-saldo-perfil">{formatMoney(user?.saldoCuenta)}</p>
          </div>
        )}
      </div>

      {/* Datos personales */}
      <div className="tarjeta-seccion-perfil">
        <div className="encabezado-seccion-perfil">
          <h3 className="titulo-seccion-perfil">Datos personales</h3>
          {!editando && (
            <button className="boton-secundario-perfil" onClick={() => setEditando(true)}>
              Editar
            </button>
          )}
        </div>

        {!editando ? (
          <div className="lista-datos-perfil">
            <div className="fila-dato-perfil">
              <span className="etiqueta-dato-perfil">Nombre completo</span>
              <span className="valor-dato-perfil">{user?.nombre}</span>
            </div>
            <div className="fila-dato-perfil">
              <span className="etiqueta-dato-perfil">Correo electrónico</span>
              <span className="valor-dato-perfil">{user?.email}</span>
            </div>
            <div className="fila-dato-perfil">
              <span className="etiqueta-dato-perfil">Tipo de cuenta</span>
              <span className="valor-dato-perfil">{etiquetaRol[user?.rol] || user?.rol}</span>
            </div>
            <div className="fila-dato-perfil">
              <span className="etiqueta-dato-perfil">Cliente desde</span>
              <span className="valor-dato-perfil">{formatFecha(user?.createdAt)}</span>
            </div>
            {exitoDatos && <p className="mensaje-exito-perfil">{exitoDatos}</p>}
          </div>
        ) : (
          <form className="formulario-perfil" onSubmit={handleGuardarDatos}>
            <div className="grupo-campo">
              <label className="etiqueta-campo">Nombre completo</label>
              <input
                className="campo-entrada"
                type="text"
                name="nombre"
                value={formDatos.nombre}
                onChange={handleChangeDatos}
                required
              />
            </div>
            <div className="grupo-campo">
              <label className="etiqueta-campo">Correo electrónico</label>
              <input
                className="campo-entrada"
                type="email"
                name="email"
                value={formDatos.email}
                onChange={handleChangeDatos}
                required
              />
            </div>
            {errorDatos && <p className="error-autenticacion">{errorDatos}</p>}
            <div className="acciones-formulario-perfil">
              <button type="submit" className="boton-principal-perfil">Guardar cambios</button>
              <button type="button" className="boton-secundario-perfil" onClick={handleCancelarEdicion}>
                Cancelar
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Seguridad */}
      <div className="tarjeta-seccion-perfil">
        <div className="encabezado-seccion-perfil">
          <h3 className="titulo-seccion-perfil">Seguridad</h3>
        </div>
        <div className="fila-dato-perfil">
          <div>
            <span className="etiqueta-dato-perfil">Contraseña</span>
            <p className="descripcion-seguridad-perfil">Actualiza tu contraseña periódicamente para mantener tu cuenta segura.</p>
          </div>
          <button className="boton-secundario-perfil" onClick={() => setModalPassword(true)}>
            Cambiar contraseña
          </button>
        </div>
      </div>

      {/* Modal cambiar contraseña */}
      <Modal open={modalPassword} onClose={handleCerrarModalPassword} title="Cambiar contraseña">
        <form className="formulario-perfil" onSubmit={handleGuardarPassword}>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Contraseña actual</label>
            <input
              className="campo-entrada"
              type="password"
              name="actual"
              placeholder="••••••••"
              value={formPassword.actual}
              onChange={handleChangePassword}
              required
            />
          </div>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Nueva contraseña</label>
            <input
              className="campo-entrada"
              type="password"
              name="nueva"
              placeholder="••••••••"
              value={formPassword.nueva}
              onChange={handleChangePassword}
              required
            />
          </div>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Confirmar nueva contraseña</label>
            <input
              className="campo-entrada"
              type="password"
              name="confirmar"
              placeholder="••••••••"
              value={formPassword.confirmar}
              onChange={handleChangePassword}
              required
            />
          </div>
          {errorPassword && <p className="error-autenticacion">{errorPassword}</p>}
          {exitoPassword && <p className="mensaje-exito-perfil">{exitoPassword}</p>}
          <div className="acciones-formulario-perfil">
            <button type="submit" className="boton-principal-perfil" disabled={cargandoPassword}>
              {cargandoPassword ? 'Guardando...' : 'Actualizar contraseña'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default PerfilPage;
