import React, { useState, useEffect } from 'react';
import { authService } from '../../auth/services/authService';
import { ROLES } from '../../../core/constants';
import Modal from '../../../shared/components/Modal';
import './AdminPage.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val || 0);

const etiquetaRol = (rol) => {
  const etiquetas = {
    administrador: '👑 Administrador',
    padre: '👨‍👧 Padre/Madre',
    hijo: '🧒 Hijo/Hija',
    normal: '👤 Normal',
  };
  return etiquetas[rol] || rol;
};

const AdminPage = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [usuarioSeleccionado, setUsuarioSeleccionado] = useState(null);
  const [modalDetalle, setModalDetalle] = useState(false);
  const [modalEditar, setModalEditar] = useState(false);
  const [modalEliminar, setModalEliminar] = useState(false);
  const [formEditar, setFormEditar] = useState({});
  const [busqueda, setBusqueda] = useState('');
  const [filtroRol, setFiltroRol] = useState('todos');
  const [mensaje, setMensaje] = useState('');

  const cargarUsuarios = async () => {
    try {
      const todos = await authService.obtenerTodosLosUsuarios();
      setUsuarios(todos);
    } catch (err) {
      console.error('Error cargando usuarios:', err.message);
    }
  };

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const usuariosFiltrados = usuarios.filter((u) => {
    const coincideBusqueda =
      `${u.nombres} ${u.apellidos}`.toLowerCase().includes(busqueda.toLowerCase()) ||
      u.email.toLowerCase().includes(busqueda.toLowerCase());
    const coincideRol = filtroRol === 'todos' || u.rol === filtroRol;
    return coincideBusqueda && coincideRol;
  });

  const abrirDetalle = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setModalDetalle(true);
  };

  const abrirEditar = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setFormEditar({ nombres: usuario.nombres, apellidos: usuario.apellidos, email: usuario.email });
    setModalEditar(true);
  };

  const abrirEliminar = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setModalEliminar(true);
  };

  const handleGuardarEdicion = async () => {
    try {
      await authService.actualizarUsuario(usuarioSeleccionado.id, {
        nombres: formEditar.nombres,
        apellidos: formEditar.apellidos,
        email: formEditar.email,
      });
      setMensaje('✓ Usuario actualizado correctamente.');
      setModalEditar(false);
      await cargarUsuarios();
      setTimeout(() => setMensaje(''), 3000);
    } catch (err) {
      setMensaje('✗ ' + err.message);
      setTimeout(() => setMensaje(''), 3000);
    }
  };

  const handleEliminar = async () => {
    try {
      await authService.eliminarUsuario(usuarioSeleccionado.id);
      setMensaje('✓ Usuario eliminado correctamente.');
      setModalEliminar(false);
      await cargarUsuarios();
      setTimeout(() => setMensaje(''), 3000);
    } catch (err) {
      setMensaje('✗ ' + err.message);
      setTimeout(() => setMensaje(''), 3000);
    }
  };

  return (
    <div className="pagina-admin">
      <div className="encabezado-admin">
        <div>
          <h1 className="titulo-admin">Panel de administrador</h1>
          <p className="subtitulo-admin">{usuarios.length} usuarios registrados</p>
        </div>
        {mensaje && <div className="mensaje-exito-admin">{mensaje}</div>}
      </div>

      {/* Filtros */}
      <div className="barra-filtros-admin">
        <input
          className="campo-busqueda-admin"
          type="text"
          placeholder="Buscar por nombre o correo..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <div className="filtros-rol-admin">
          {['todos', ROLES.NORMAL, ROLES.ADMIN].map((rol) => (
            <button
              key={rol}
              className={`boton-filtro-admin ${filtroRol === rol ? 'boton-filtro-admin--activo' : ''}`}
              onClick={() => setFiltroRol(rol)}
            >
              {rol === 'todos' ? 'Todos' : etiquetaRol(rol)}
            </button>
          ))}
        </div>
      </div>

      {/* Tabla de usuarios */}
      {usuariosFiltrados.length === 0 ? (
        <div className="admin-sin-resultados">
          <p>No se encontraron usuarios con ese criterio.</p>
        </div>
      ) : (
        <div className="tabla-admin">
          {usuariosFiltrados.map((usuario) => (
            <div key={usuario.id} className="fila-usuario-admin">
              <div className="avatar-usuario-admin">
                {usuario.nombres?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="informacion-usuario-admin">
                <p className="nombre-usuario-admin">{usuario.nombres} {usuario.apellidos}</p>
                <p className="correo-usuario-admin">{usuario.email}</p>
                <span className={`etiqueta-rol-admin etiqueta-rol-admin--${usuario.rol}`}>
                  {etiquetaRol(usuario.rol)}
                </span>
              </div>
              <div className="acciones-usuario-admin">
                <button className="boton-accion-admin boton-accion-admin--ver" onClick={() => abrirDetalle(usuario)}>
                  Ver
                </button>
                <button className="boton-accion-admin boton-accion-admin--editar" onClick={() => abrirEditar(usuario)}>
                  Editar
                </button>
                {usuario.rol !== ROLES.ADMIN && (
                  <button className="boton-accion-admin boton-accion-admin--eliminar" onClick={() => abrirEliminar(usuario)}>
                    Eliminar
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal detalle */}
      <Modal open={modalDetalle} onClose={() => setModalDetalle(false)} title="Detalle del usuario">
        {usuarioSeleccionado && (
          <div className="detalle-usuario-admin">
            <div className="avatar-detalle-admin">
              {usuarioSeleccionado.nombres?.charAt(0).toUpperCase() || 'U'}
            </div>
            <h2 className="nombre-detalle-admin">{usuarioSeleccionado.nombres} {usuarioSeleccionado.apellidos}</h2>
            <p className="correo-detalle-admin">{usuarioSeleccionado.email}</p>
            <span className={`etiqueta-rol-admin etiqueta-rol-admin--${usuarioSeleccionado.rol}`}>
              {etiquetaRol(usuarioSeleccionado.rol)}
            </span>

            <div className="campos-detalle-admin">
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">Nombres</span>
                <span className="valor-campo-detalle">{usuarioSeleccionado.nombres}</span>
              </div>
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">Apellidos</span>
                <span className="valor-campo-detalle">{usuarioSeleccionado.apellidos}</span>
              </div>
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">Correo electrónico</span>
                <span className="valor-campo-detalle">{usuarioSeleccionado.email}</span>
              </div>
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">Saldo en cuenta</span>
                <span className="valor-campo-detalle">—</span>
              </div>
              <div className="campo-detalle-admin">
                <span className="etiqueta-campo-detalle">Miembro desde</span>
                <span className="valor-campo-detalle">—</span>
              </div>
            </div>
          </div>
        )}
      </Modal>

      {/* Modal editar */}
      <Modal open={modalEditar} onClose={() => setModalEditar(false)} title="Editar usuario">
        <div className="formulario-modal">
          <div className="grupo-campo">
            <label className="etiqueta-campo">Nombres</label>
            <input className="campo-entrada" type="text" value={formEditar.nombres || ''}
              onChange={(e) => setFormEditar({ ...formEditar, nombres: e.target.value })} />
          </div>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Apellidos</label>
            <input className="campo-entrada" type="text" value={formEditar.apellidos || ''}
              onChange={(e) => setFormEditar({ ...formEditar, apellidos: e.target.value })} />
          </div>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Correo electrónico</label>
            <input className="campo-entrada" type="email" value={formEditar.email || ''}
              onChange={(e) => setFormEditar({ ...formEditar, email: e.target.value })} />
          </div>
          <button className="boton-principal" onClick={handleGuardarEdicion}>Guardar cambios</button>
        </div>
      </Modal>

      {/* Modal eliminar */}
      <Modal open={modalEliminar} onClose={() => setModalEliminar(false)} title="Eliminar usuario">
        <div className="formulario-modal">
          <p style={{ color: 'var(--color-text-soft)', marginBottom: '1rem', textAlign: 'center' }}>
            ¿Estás seguro de que quieres eliminar a <strong style={{ color: 'var(--color-text)' }}>{usuarioSeleccionado?.nombres} {usuarioSeleccionado?.apellidos}</strong>?
            Esta acción no se puede deshacer.
          </p>
          <button className="boton-peligro" onClick={handleEliminar}>Sí, eliminar</button>
          <button className="boton-secundario" onClick={() => setModalEliminar(false)}
            style={{ marginTop: '8px' }}>Cancelar</button>
        </div>
      </Modal>
    </div>
  );
};

export default AdminPage;
