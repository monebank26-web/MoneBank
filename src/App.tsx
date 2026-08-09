import { Component } from 'react';
import Usuarios from './pages/Usuarios';
import Productos from './pages/Productos';
import Login from './pages/Login';
import Registro from './pages/Registro';
import Transacciones from './pages/Transacciones';
import './styles/global.css';

/**
 * App.tsx
 * ---------------------------------------------------------
 * La restricción de la actividad prohíbe useState u otro HOOK.
 * Los hooks solo existen en componentes de FUNCIÓN, así que para
 * poder cambiar de vista (navegación entre los 5 módulos) sin usar
 * ningún hook, App se implementa como un COMPONENTE DE CLASE, que
 * maneja su propio this.state (no es un hook, es la forma clásica
 * de React previa a los hooks).
 *
 * Los 5 módulos (Usuarios, Productos, Login, Registro, Transacciones)
 * sí son componentes de función y NO usan hooks: solo reciben props
 * y devuelven funciones de callback hacia su propio hijo (CardAccion).
 */

type Vista = 'usuarios' | 'productos' | 'login' | 'registro' | 'transacciones';

interface AppState {
  vistaActual: Vista;
}

const MODULOS: { id: Vista; etiqueta: string }[] = [
  { id: 'usuarios', etiqueta: 'Usuarios (Perfil)' },
  { id: 'productos', etiqueta: 'Productos (Bolsillos)' },
  { id: 'login', etiqueta: 'Login' },
  { id: 'registro', etiqueta: 'Registro' },
  { id: 'transacciones', etiqueta: 'Transacciones' },
];

class App extends Component<Record<string, never>, AppState> {
  state: AppState = {
    vistaActual: 'usuarios',
  };

  cambiarVista = (vista: Vista) => {
    this.setState({ vistaActual: vista });
  };

  renderVista() {
    const { vistaActual } = this.state;

    switch (vistaActual) {
      case 'usuarios':
        return <Usuarios nombreUsuario="Camila Ríos" correo="camila@monebank.com" />;
      case 'productos':
        return (
          <Productos
            bolsillos={[
              { nombre: 'Vacaciones', saldo: 850000 },
              { nombre: 'Emergencias', saldo: 1200000 },
              { nombre: 'Estudio', saldo: 300000 },
            ]}
          />
        );
      case 'login':
        return <Login nombreModulo="Iniciar sesión" />;
      case 'registro':
        return <Registro nombreModulo="Crear cuenta" />;
      case 'transacciones':
        return (
          <Transacciones
            movimientos={[
              { descripcion: 'Depósito Vacaciones', monto: 150000 },
              { descripcion: 'Retiro Emergencias', monto: -50000 },
              { descripcion: 'Transferencia Estudio', monto: 100000 },
            ]}
          />
        );
      default:
        return null;
    }
  }

  render() {
    const { vistaActual } = this.state;

    return (
      <div className="app-shell">
        <header className="app-header">
          <h1>MoneBank · Actividad 3</h1>
          <p>Componentes padre e hijo con props, TypeScript y sin hooks</p>
        </header>

        <nav className="app-nav">
          {MODULOS.map((modulo) => (
            <button
              key={modulo.id}
              className={`nav-btn ${vistaActual === modulo.id ? 'active' : ''}`}
              onClick={() => this.cambiarVista(modulo.id)}
            >
              {modulo.etiqueta}
            </button>
          ))}
        </nav>

        <main className="app-main">{this.renderVista()}</main>
      </div>
    );
  }
}

export default App;
