// shared/layouts/MainLayout.jsx
import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../core/context/AuthContext';
import { ROUTES } from '../../core/constants';
import './MainLayout.css';

const NAV_ITEMS = [
  { to: ROUTES.DASHBOARD, label: 'Inicio', icon: '⊞' },
  { to: ROUTES.BOLSILLOS, label: 'Bolsillos', icon: '◈' },
  { to: ROUTES.TRANSACCIONES, label: 'Movimientos', icon: '↕' },
];

const MainLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };

  return (
    <div className="raiz-estructura">
      {/* Sidebar */}
      <aside className={`barra-lateral ${menuOpen ? 'barra-lateral--abierta' : ''}`}>
        <div className="marca-barra-lateral">
          <span className="logo-barra-lateral">MB</span>
          <span className="nombre-barra-lateral">MoneBank</span>
        </div>

        <nav className="navegacion-barra-lateral">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `elemento-navegacion ${isActive ? 'elemento-navegacion--activo' : ''}`
              }
              onClick={() => setMenuOpen(false)}
            >
              <span className="icono-navegacion">{item.icon}</span>
              <span className="etiqueta-navegacion">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="pie-barra-lateral">
          <div className="usuario-barra-lateral">
            <div className="avatar-usuario">
              {user?.nombre?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="informacion-usuario">
              <p className="nombre-usuario">{user?.nombre}</p>
              <p className="correo-usuario">{user?.email}</p>
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
        {/* Header móvil */}
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
