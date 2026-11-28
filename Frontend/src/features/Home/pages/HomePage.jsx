import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Icon } from '@iconify/react';
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
    descripcion: 'Ponte una meta, un plazo, y deja que MoneBank te muestre qué tan cerca estás de cumplirla.',
    imagen: imgMetasDeAhorro,
  },
  {
    titulo: 'Límites de gasto',
    descripcion: 'Define cuánto quieres gastar por categoría al mes, y te avisamos antes de que te pases.',
    imagen: imgLimitesDeGasto,
  },
  {
    titulo: 'Control parental',
    descripcion: 'Supervisa el dinero de tus hijos y aprueba sus gastos importantes, sin dejar de darles independencia.',
    imagen: imgControlParental,
  },
  {
    titulo: 'Movimientos claros',
    descripcion: 'Cada ingreso y cada gasto, ordenado y fácil de entender, sin hojas de cálculo.',
    imagen: imgMovimientosClaros,
  },
];

const pilares = [
  {
    icono: 'mdi:piggy-bank-outline',
    titulo: 'Ahorro y metas',
    texto: 'Registra tus ingresos y gastos, clasifícalos por categoría y sigue el avance de tus metas de ahorro con claridad.',
  },
  {
    icono: 'mdi:creation',
    titulo: 'Asesor inteligente',
    texto: 'Antes de gastar, tu asesor con IA te muestra cómo impactaría tu saldo y tus límites, para decidir con criterio.',
  },
  {
    icono: 'mdi:human-male-child',
    titulo: 'Control parental y familiar',
    texto: 'Vincula las cuentas de tus hijos, supervisa sus movimientos y enséñales a manejar su propio dinero.',
  },
];

const garantias = [
  { icono: 'mdi:shield-lock-outline', texto: 'Contraseñas cifradas' },
  { icono: 'mdi:school-outline', texto: 'Entorno simulado para aprender' },
  { icono: 'mdi:chart-timeline-variant', texto: 'Control en tiempo real' },
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

  const irASeccion = (id) => {
    setMenuAbierto(false);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="pagina-principal">
      <header className="barra-superior-inicio">
        <div className="barra-superior-inicio__contenido">
          <button className="marca-inicio" onClick={() => irASeccion('inicio')}>
            <img src={logoMonebank} alt="MoneBank" className="logo-inicio" />
            <span className="nombre-marca-inicio">
              Mone<span>Bank</span>
            </span>
          </button>

          <nav className="enlaces-inicio">
            <button onClick={() => irASeccion('que-hacemos')}>Qué hacemos</button>
            <button onClick={() => irASeccion('funcionalidades')}>Funcionalidades</button>
          </nav>

          <div className="acciones-inicio">
            <ToggleTema />
            {isAuthenticated ? (
              <button
                className="boton-inicio boton-inicio--primario"
                onClick={() => navigate(ROUTES.DASHBOARD)}
              >
                Ir a mi panel
                <Icon icon="mdi:arrow-right" />
              </button>
            ) : (
              <>
                <button
                  className="boton-inicio boton-inicio--texto"
                  onClick={() => navigate(ROUTES.LOGIN)}
                >
                  Iniciar sesión
                </button>
                <button
                  className="boton-inicio boton-inicio--primario"
                  onClick={() => navigate(ROUTES.REGISTER)}
                >
                  Crear cuenta
                </button>
              </>
            )}
          </div>

          <button
            className="boton-menu-inicio"
            onClick={() => setMenuAbierto(true)}
            aria-label="Abrir menú"
          >
            <Icon icon="mdi:menu" />
          </button>
        </div>

        <DrawerAcciones open={menuAbierto} onClose={() => setMenuAbierto(false)}>
          <div className="drawer-inicio__tema">
            <span>Modo claro / oscuro</span>
            <ToggleTema />
          </div>

          <span className="drawer-inicio__separador" />

          <button
            className="drawer-inicio__opcion drawer-inicio__opcion--secundaria"
            onClick={() => irASeccion('que-hacemos')}
          >
            Qué hacemos
          </button>
          <button
            className="drawer-inicio__opcion drawer-inicio__opcion--secundaria"
            onClick={() => irASeccion('funcionalidades')}
          >
            Funcionalidades
          </button>

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

      <section className="seccion-hero" id="inicio">
        <span className="chip-hero">
          <span className="chip-hero__punto" />
          Finanzas personales y familiares
        </span>

        <h1 className="titulo-hero">
          Buen criterio para
          <span> administrar tu dinero.</span>
        </h1>

        <p className="subtitulo-hero">
          MoneBank te ayuda a organizar tus ingresos, ponerte metas realistas y
          enseñarles a los más jóvenes de la casa a manejar su propio dinero,
          con claridad y sin fricción.
        </p>

        <div className="cta-hero">
          <button
            className="boton-inicio boton-inicio--primario boton-inicio--grande"
            onClick={() => navigate(isAuthenticated ? ROUTES.DASHBOARD : ROUTES.REGISTER)}
          >
            {isAuthenticated ? 'Ir a mi panel' : 'Comenzar ahora'}
            <Icon icon="mdi:arrow-right" />
          </button>
          <button
            className="boton-inicio boton-inicio--contorno boton-inicio--grande"
            onClick={() => irASeccion('funcionalidades')}
          >
            <Icon icon="mdi:play-circle-outline" />
            Ver funcionalidades
          </button>
        </div>

        <ul className="garantias-hero">
          {garantias.map((garantia) => (
            <li key={garantia.texto}>
              <Icon icon={garantia.icono} />
              {garantia.texto}
            </li>
          ))}
        </ul>

        <div className="vista-previa">
          <div className="vista-previa__barra">
            <span className="vista-previa__puntos">
              <i />
              <i />
              <i />
            </span>
            <span className="vista-previa__titulo">Vista previa de ejemplo</span>
            <span className="vista-previa__estado">
              <i />
              En vivo
            </span>
          </div>

          <div className="vista-previa__cuadricula">
            <div className="vista-previa__tarjeta">
              <p className="vista-previa__etiqueta">Saldo disponible</p>
              <p className="vista-previa__valor">
                $ 2.437.000 <span>COP</span>
              </p>
              <p className="vista-previa__delta">
                <Icon icon="mdi:trending-up" />
                +14,8% este mes
              </p>
            </div>

            <div className="vista-previa__tarjeta">
              <p className="vista-previa__etiqueta">Meta: Vacaciones</p>
              <div className="vista-previa__fila">
                <p className="vista-previa__monto">$ 3.900.000</p>
                <p className="vista-previa__porcentaje">97%</p>
              </div>
              <div className="vista-previa__barra-progreso">
                <span style={{ width: '97%' }} />
              </div>
            </div>

            <div className="vista-previa__tarjeta">
              <p className="vista-previa__etiqueta">Supervisión familiar</p>
              <div className="vista-previa__fila">
                <p className="vista-previa__monto">2 hijos vinculados</p>
                <span className="vista-previa__sello">Al día</span>
              </div>
              <p className="vista-previa__nota">Mesada semanal bajo control</p>
            </div>
          </div>
        </div>
      </section>

      <section className="seccion-que-hacemos" id="que-hacemos">
        <h2 className="titulo-seccion">
          Qué hacemos en <span>MoneBank</span>
        </h2>
        <p className="subtitulo-seccion">
          Una solución pensada tanto para tus finanzas individuales como para la
          economía familiar. Sencilla, intuitiva y sin complicaciones.
        </p>

        <div className="cuadricula-pilares">
          {pilares.map((pilar) => (
            <article className="tarjeta-pilar" key={pilar.titulo}>
              <span className="tarjeta-pilar__icono">
                <Icon icon={pilar.icono} />
              </span>
              <h3>{pilar.titulo}</h3>
              <p>{pilar.texto}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="seccion-servicios" id="funcionalidades">
        <h2 className="titulo-seccion">
          Lo que puedes hacer con <span>MoneBank</span>
        </h2>
        <p className="subtitulo-seccion">
          Herramientas diseñadas para darte paz mental y control sobre tu dinero.
        </p>
        <CarruselServicios servicios={servicios} />
      </section>

      <section className="seccion-llamada">
        <div className="tarjeta-llamada">
          <h2>
            Toma el control de tus <span>finanzas.</span>
          </h2>
          <p>
            Comienza en minutos, activa la gestión familiar y mantén la
            tranquilidad sobre tu dinero.
          </p>
          <button
            className="boton-inicio boton-inicio--primario boton-inicio--grande"
            onClick={() => navigate(isAuthenticated ? ROUTES.DASHBOARD : ROUTES.REGISTER)}
          >
            {isAuthenticated ? 'Ir a mi panel' : 'Crear cuenta gratis'}
            <Icon icon="mdi:arrow-right" />
          </button>
          <small>Gratis y sin tarjeta de crédito</small>
        </div>
      </section>

      <footer className="pie-inicio">
        <div className="pie-inicio__marca">
          <span className="nombre-marca-inicio">
            Mone<span>Bank</span>
          </span>
          <p>© {new Date().getFullYear()} MoneBank. Tu dinero, con clase.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;