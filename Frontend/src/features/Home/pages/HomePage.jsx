import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../core/context/AuthContext';
import { ROUTES } from '../../../core/constants';
import logoMonebank from '../../../shared/assets/logo-monebank.png';
import CarruselServicios from '../components/CarruselServicios';
import DrawerAcciones from '../components/DrawerAcciones';
import ToggleTema from '../components/ToggleTema';
import './HomePage.css';

import imgMetasDeAhorro from '../../../shared/assets/metas-de-ahorro.png';
import imgLimitesDeGasto from '../../../shared/assets/limites-de-gasto.png';
import imgControlParental from '../../../shared/assets/control-parental.png';
import imgMovimientosClaros from '../../../shared/assets/movimientos-claros.png';

const servicios = [
  
  {
    titulo: 'Metas de ahorro',
    descripcion: 'Ponte una meta, un plazo, y deja que MoneBank te muestre qué tan cerca estás.',
    icono: '◆',
    imagen: imgMetasDeAhorro,
  },
  {
    titulo: 'Límites de gasto',
    descripcion: 'Define cuánto quieres gastar por categoría al mes, y te avisamos antes de que te pases.',
    icono: '▲',
    imagen: imgLimitesDeGasto,
  },
  {
    titulo: 'Control parental',
    descripcion: 'Supervisa el dinero de tus hijos y aprueba sus gastos importantes, sin dejar de darles independencia.',
    icono: '👨‍👧',
    imagen: imgControlParental,
  },
  {
    titulo: 'Movimientos claros',
    descripcion: 'Cada ingreso y cada gasto, ordenado y fácil de entender, sin hojas de cálculo.',
    icono: '↕',
    imagen: imgMovimientosClaros,
  },
];

const HomePage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();
  const [menuAbierto, setMenuAbierto] = useState(false);

  const handleLogout = () => {
    logout();
    navigate(ROUTES.LOGIN);
  };

  const irA = (ruta) => {
    setMenuAbierto(false);
    navigate(ruta);
  };

  return (
    <div className="pagina-principal">
      <header className="encabezado-inicio">
        <div className="marca-inicio">
          <img src={logoMonebank} alt="MoneBank" className="logo-inicio" />
          <span className="nombre-inicio">MoneBank</span>
        </div>

        <button
          className="boton-menu-inicio"
          onClick={() => setMenuAbierto(true)}
          aria-label="Abrir menú"
        >
          ☰
        </button>

        <DrawerAcciones open={menuAbierto} onClose={() => setMenuAbierto(false)}>
          <div className="drawer-inicio__tema">
            <span>Modo claro / oscuro</span>
            <ToggleTema />
          </div>

          <span className="drawer-inicio__separador" />

          {isAuthenticated ? (
            <button
              className="drawer-inicio__opcion drawer-inicio__opcion--primaria"
              onClick={() => irA(ROUTES.DASHBOARD)}
            >
              Ir a mi panel
            </button>
          ) : (
            <>
              <button
                className="drawer-inicio__opcion drawer-inicio__opcion--secundaria"
                onClick={() => irA(ROUTES.LOGIN)}
              >
                Iniciar sesión
              </button>
              <button
                className="drawer-inicio__opcion drawer-inicio__opcion--primaria"
                onClick={() => irA(ROUTES.REGISTER)}
              >
                Crear cuenta
              </button>
            </>
          )}

          {isAuthenticated && (
            <button className="drawer-inicio__logout" onClick={handleLogout}>
              Cerrar sesión
            </button>
          )}
        </DrawerAcciones>
      </header>

      <section className="seccion-hero">
        <p className="ojo-hero">Finanzas personales y familiares</p>
        <h1 className="titulo-hero">
          Buen criterio para administrar tu dinero.
        </h1>
        <p className="subtitulo-hero">
          MoneBank te ayuda a organizar tus ingresos, ponerte metas realistas y
          enseñarles a los más jóvenes de la casa a manejar su propio dinero,
          sin perder de vista ni un peso.
        </p>
        {!isAuthenticated && (
          <div className="cta-hero">
            <button className="boton-inicio boton-inicio--primario boton-inicio--grande" onClick={() => navigate(ROUTES.REGISTER)}>
              Crear mi cuenta gratis
            </button>
          </div>
        )}
      </section>

      <section className="seccion-quienes-somos">
        <div className="contenido-quienes-somos">
          <h2 className="titulo-seccion">Qué hacemos</h2>
          <p className="texto-quienes-somos">
            Somos una aplicación de finanzas pensada tanto para quien vive
            solo como para quien administra el dinero de toda la familia.
            De un lado, herramientas para ahorrar con intención y gastar con
            cabeza. Del otro, control parental de verdad, para que los hijos
            aprendan a manejar su dinero con la supervisión de sus padres,
            no a ciegas.
          </p>
        </div>
      </section>

      <section className="seccion-servicios">
        <h2 className="titulo-seccion titulo-seccion--centrado">Lo que puedes hacer con MoneBank</h2>
        <CarruselServicios servicios={servicios} />
      </section>

      <footer className="pie-inicio">
        <p>© {new Date().getFullYear()} MoneBank. Tu dinero, con clase.</p>
      </footer>
    </div>
  );
};

export default HomePage;