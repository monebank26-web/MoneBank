import React, { useEffect, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

import { useAuth } from '../../core/context/AuthContext';
import { ROUTES, ROLES } from '../../core/constants';
import { controlParentalService } from '../../features/controlParental/services/controlParentalServices';

import './MainLayout.css';

const MainLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);
  const [relacionesParentales, setRelacionesParentales] = useState([]);

  const esAdmin = user?.rol === ROLES.ADMIN;

  useEffect(() => {
    const cargarRelacionesParentales = async () => {
      if (!user || esAdmin) {
        setRelacionesParentales([]);
        return;
      }

      try {
        const relaciones =
          await controlParentalService.obtenerVinculaciones();

        setRelacionesParentales(
          Array.isArray(relaciones) ? relaciones : []
        );
      } catch (error) {
        console.error(
          'No se pudieron cargar las relaciones parentales:',
          error
        );

        setRelacionesParentales([]);
      }
    };

    cargarRelacionesParentales();
  }, [user, esAdmin]);

  
  const esHijoVinculado = relacionesParentales.some(
    (relacion) =>
      Number(relacion.id_usuario_dependiente) ===
      Number(user?.id)
  );

  const puedeVerControlParental =
    !esAdmin && !esHijoVinculado;

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };

  const elementosNav = [
    {
      to: ROUTES.DASHBOARD,
      label: 'Inicio',
      icono: '⊞',
      visible: true,
    },

    {
      to: ROUTES.BOLSILLOS,
      label: 'Bolsillos',
      icono: '◈',
      visible: !esAdmin,
    },

    {
      to: ROUTES.METAS,
      label: 'Metas',
      icono: '◆',
      visible: !esAdmin,
    },

    {
      to: ROUTES.LIMITES,
      label: 'Límites',
      icono: '▲',
      visible: !esAdmin,
    },

    {
      to: ROUTES.TRANSACCIONES,
      label: 'Movimientos',
      icono: '↕',
      visible: !esAdmin,
    },

    {
      to: ROUTES.CONTROL_PARENTAL,
      label: 'Control parental',
      icono: '𖥤',
      visible: puedeVerControlParental,
    },

    {
      to: ROUTES.ADMIN,
      label: 'Administrador',
      icono: '👑',
      visible: esAdmin,
    },

    {
      to: ROUTES.PERFIL,
      label: 'Mi perfil',
      icono: '⚙',
      visible: true,
    },
  ].filter((elemento) => elemento.visible);

  const etiquetaRol = {
    administrador: 'Administrador',
    padre: 'Padre/Madre',
    hijo: 'Hijo/Hija',
    normal: '',
  }[user?.rol] || '';

  return (
    <div className="raiz-estructura">
      <aside
        className={`barra-lateral ${
          menuOpen ? 'barra-lateral--abierta' : ''
        }`}
      >
        <div className="marca-barra-lateral">
          <span className="logo-barra-lateral">
            MB
          </span>

          <span className="nombre-barra-lateral">
            MoneBank
          </span>
        </div>

        <nav className="navegacion-barra-lateral">
          {elementosNav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `elemento-navegacion ${
                  isActive
                    ? 'elemento-navegacion--activo'
                    : ''
                }`
              }
              onClick={() => setMenuOpen(false)}
            >
              <span className="icono-navegacion">
                {item.icono}
              </span>

              <span className="etiqueta-navegacion">
                {item.label}
              </span>
            </NavLink>
          ))}
        </nav>

        <div className="pie-barra-lateral">
          <div className="usuario-barra-lateral">
            <div className="avatar-usuario">
              {user?.nombres?.charAt(0).toUpperCase() || 'U'}
            </div>

            <div className="informacion-usuario">
              <p className="nombre-usuario">
                {user?.nombres} {user?.apellidos}
              </p>

              {etiquetaRol ? (
                <p className="rol-usuario">
                  {etiquetaRol}
                </p>
              ) : (
                <p className="correo-usuario">
                  {user?.email}
                </p>
              )}
            </div>
          </div>

          <button
            className="boton-cerrar-sesion"
            onClick={handleLogout}
          >
            Cerrar sesión
          </button>
        </div>
      </aside>

      {menuOpen && (
        <div
          className="capa-fondo-movil"
          onClick={() => setMenuOpen(false)}
        />
      )}

      <main className="contenido-principal">
        <header className="encabezado-movil">
          <button
            className="boton-menu-hamburguesa"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            ☰
          </button>

          <span className="marca-encabezado-movil">
            MoneBank
          </span>
        </header>

        <div className="area-contenido">
          {children}
        </div>
      </main>
    </div>
  );
};

export default MainLayout;
