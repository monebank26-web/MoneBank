import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../core/context/AuthContext';
import { ROUTES, ROLES } from '../../core/constants';
import './MainLayout.css';

const MainLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };

  const esAdmin = user?.rol === ROLES.ADMIN;
  const esPadre = user?.rol === ROLES.PADRE;
  const esHijo = user?.rol === ROLES.HIJO;
  const tienControlParental = esPadre || esHijo;

  const elementosNav = [
    { to: ROUTES.DASHBOARD, label: 'Inicio', icono: '⊞', visible: true },
    { to: ROUTES.CHAT, label: 'Asesor IA', icono: '◈', visible: !esAdmin },
    { to: ROUTES.METAS, label: 'Metas', icono: '◆', visible: !esAdmin },
    { to: ROUTES.LIMITES, label: 'Límites', icono: '▲', visible: !esAdmin },
    { to: ROUTES.TRANSACCIONES, label: 'Movimientos', icono: '↕', visible: !esAdmin },
    {
      to: esPadre ? ROUTES.CONTROL_PARENTAL_PADRE : ROUTES.CONTROL_PARENTAL_HIJO,
      label: 'Control parental',
      icono: '👨‍👧',
      visible: tienControlParental,
    },
    { to: ROUTES.ADMIN, label: 'Administrador', icono: '👑', visible: esAdmin },
    { to: ROUTES.PERFIL, label: 'Mi perfil', icono: '⚙', visible: true },
  ].filter((e) => e.visible);

  const etiquetaRol = {
    administrador: '👑 Administrador',
    padre: '👨‍👧 Padre/Madre',
    hijo: '🧒 Hijo/Hija',
    normal: '',
  }[user?.rol] || '';

  return (
    <div className="raiz-estructura">
      {/* Sidebar */}
      <aside className={`barra-lateral ${menuOpen ? 'barra-lateral--abierta' : ''}`}>
        <div className="marca-barra-lateral">
          <span className="logo-barra-lateral">MB</span>
          <span className="nombre-barra-lateral">MoneBank</span>
        </div>

        <nav className="navegacion-barra-lateral">
          {elementosNav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `elemento-navegacion ${isActive ? 'elemento-navegacion--activo' : ''}`
              }
              onClick={() => setMenuOpen(false)}
            >
              <span className="icono-navegacion">{item.icono}</span>
              <span className="etiqueta-navegacion">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="pie-barra-lateral">
          <div className="usuario-barra-lateral">
            <div className="avatar-usuario">
              {user?.nombres?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="informacion-usuario">
              <p className="nombre-usuario">{user?.nombres} {user?.apellidos}</p>
              {etiquetaRol
                ? <p className="rol-usuario">{etiquetaRol}</p>
                : <p className="correo-usuario">{user?.email}</p>
              }
            </div>
          </div>
          <button className="boton-cerrar-sesion" onClick={handleLogout}>
            Cerrar sesión
          </button>
        </div>
      </aside>

      {/* Overlay móvil */}
      {menuOpen && (
        <div className="capa-fondo-movil" onClick={() => setMenuOpen(false)} />
      )}

      {/* Contenido */}
      <main className="contenido-principal">
        <header className="encabezado-movil">
          <button className="boton-menu-hamburguesa" onClick={() => setMenuOpen(!menuOpen)}>
            ☰
          </button>
          <span className="marca-encabezado-movil">MoneBank</span>
        </header>

        <div className="area-contenido">{children}</div>
      </main>
    </div>
  );
};

export default MainLayout;
