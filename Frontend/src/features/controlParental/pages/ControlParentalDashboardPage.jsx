import React, { useEffect, useState } from 'react';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';
import { controlParentalDashboardService as service } from '../services/controlParentalDashboardService';
import './ControlParentalDashboardPage.css';
import ControlParentalPage from './ControlParentalPage';
import MesadaPanel from '../components/MesadaPanel';


const PERMISOS_ETIQUETAS = {
  CONSULTAR_PERFIL: 'Consultar perfil',
  CONSULTAR_SALDO: 'Consultar saldo',
  CONSULTAR_TRANSACCIONES: 'Consultar transacciones',
  CONSULTAR_AHORROS: 'Consultar ahorros',
  GESTIONAR_BOLSILLOS: 'Gestionar bolsillos',
  GESTIONAR_METAS: 'Gestionar metas',
  ASIGNAR_MESADA: 'Asignar mesada',
  ASIGNAR_RECOMPENSAS: 'Asignar recompensas',
  BLOQUEAR_GASTOS: 'Bloquear gastos',
};


const ControlParentalDashboardPage = () => {
  const [mostrarVinculacion, setMostrarVinculacion] = useState(false);
  const [hijos, setHijos] = useState([]);
  const [hijoSeleccionado, setHijoSeleccionado] = useState(null);
  const [resumen, setResumen] = useState(null);
  const [transacciones, setTransacciones] = useState([]);
  const [permisos, setPermisos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');
  const cerrarPanelHijo = () => {
    setHijoSeleccionado(null);
    setResumen(null);
    setTransacciones([]);
    setPermisos([]);
    setError('');
    setMensaje('');
  };

  

  useEffect(() => {
    const cargar = async () => {
      try {
        const data = await service.listarHijos();
        setHijos(Array.isArray(data) ? data : []);
      } catch (e) {
        setError(e.message || 'No se pudieron cargar los hijos vinculados.');
      } finally {
        setCargando(false);
      }
    };
    cargar();
  }, []);

  const seleccionarHijo = async (hijo) => {
    setHijoSeleccionado(hijo);
    setError('');
    setMensaje('');
    try {
      const [dataResumen, dataTransacciones, dataPermisos] = await Promise.all([
        service.obtenerResumen(hijo.id_usuario),
        service.obtenerTransacciones(hijo.id_usuario),
        service.obtenerPermisos(hijo.id_usuario),
      ]);
      setResumen(dataResumen);
      setTransacciones(Array.isArray(dataTransacciones) ? dataTransacciones : []);
      setPermisos(Array.isArray(dataPermisos) ? dataPermisos : []);
    } catch (e) {
      setError(e.message || 'No se pudo cargar el panel del hijo.');
    }
  };

  const cambiarPermiso = (nombre, permitido) => {
    setPermisos((actuales) => actuales.map((permiso) => (
      permiso.nombre_permiso === nombre ? { ...permiso, permitido } : permiso
    )));
  };

  const guardarPermisos = async () => {
    if (!hijoSeleccionado) return;
    setGuardando(true);
    setError('');
    setMensaje('');
    try {
      const payload = Object.fromEntries(
        permisos.map((permiso) => [permiso.nombre_permiso, permiso.permitido])
      );
      const actualizados = await service.actualizarPermisos(
        hijoSeleccionado.id_usuario,
        payload
      );
      setPermisos(actualizados);
      setMensaje('Los permisos se actualizaron correctamente.');
    } catch (e) {
      setError(e.message || 'No se pudieron actualizar los permisos.');
    } finally {
      setGuardando(false);
    }
  };

  if (cargando) return <div className="cp-dashboard"><p>Cargando control parental...</p></div>;

  return (
    <div className="cp-dashboard">
      <header className="cp-header">
        <div className="cp-dashboard-actions">
         <button
          type="button"
          className="cp-button-primary"
          onClick={() =>
            setMostrarVinculacion((visible) => !visible)
          }
        >
          {mostrarVinculacion
            ? 'Volver a mis hijos'
            : 'Vincular otra cuenta'}
        </button>
      </div>

        <div>
          <p className="cp-kicker">CONTROL PARENTAL</p>
  
          <h1>Mis cuentas dependientes</h1>
          <p>Consulta y configura los permisos de tus hijos vinculados.</p>
        </div>
      </header>

      {error && <div className="cp-alert cp-alert-error">{error}</div>}
      {mostrarVinculacion && (<section className="cp-link-section"><ControlParentalPage /></section>)}
      {mensaje && <div className="cp-alert cp-alert-ok">{mensaje}</div>}

      {!hijos.length ? (
        <section className="cp-empty">
          <h2>Aún no tienes hijos vinculados</h2>
          <p>Usa la opción de vinculación para agregar una cuenta dependiente.</p>
        </section>
      ) : (
        <div className="cp-layout">
          <aside className="cp-children-list">
            <h2>Hijos vinculados</h2>
            {hijos.map((hijo) => (
              <button
                type="button"
                key={hijo.id_usuario}
                className={`cp-child-card ${hijoSeleccionado?.id_usuario === hijo.id_usuario ? 'is-selected' : ''}`}
                onClick={() => seleccionarHijo(hijo)}
              >
                <span className="cp-avatar">
                  {(hijo.nombres || 'U').charAt(0).toUpperCase()}
                </span>
                <span className="cp-child-info">
                  <strong>{hijo.nombres} {hijo.apellidos}</strong>
                  <small>{hijo.correo}</small>
                  <small>{formatMoney(hijo.saldo || 0)}</small>
                </span>
              </button>
            ))}
          </aside>

          <main className="cp-detail">
            {!hijoSeleccionado ? (
              <section className="cp-empty cp-empty-detail">
                <h2>Selecciona una cuenta</h2>
                <p>Elige un hijo para consultar su resumen y configurar permisos.</p>
              </section>
            ) : (
              <>
                <section className="cp-detail-header">
                  <div className="cp-detail-title">
                    <button
                      type="button"
                      className="cp-back-button"
                      onClick={cerrarPanelHijo}
                    >
                      ← Volver a mis hijos
                    </button>

                    <p className="cp-kicker">
                      CUENTA DEPENDIENTE
                    </p>

                    <h2>
                      {hijoSeleccionado.nombres}
                      {' '}
                      {hijoSeleccionado.apellidos}
                    </h2>

                    <p>{hijoSeleccionado.correo}</p>
                  </div>

                  <div className="cp-balance">
                    <small>Saldo actual</small>

                    <strong>
                      {formatMoney(
                        resumen?.saldo ||
                        hijoSeleccionado.saldo ||
                        0
                      )}
                    </strong>
                  </div>
                </section>

                {/*<section className="cp-section">
                  <div className="cp-section-title">
                    <div><h3>Permisos parentales</h3><p>El backend valida estos permisos en cada operación.</p></div>
                    <button type="button" onClick={guardarPermisos} disabled={guardando}>
                      {guardando ? 'Guardando...' : 'Guardar permisos'}
                    </button>
                  </div>
                  <div className="cp-permissions-grid">
                    {permisos.map((permiso) => (
                      <label className="cp-permission" key={permiso.nombre_permiso}>
                        <span>
                          <strong>{PERMISOS_ETIQUETAS[permiso.nombre_permiso] || permiso.nombre_permiso}</strong>
                          <small>{permiso.permitido ? 'Permitido' : 'Bloqueado'}</small>
                        </span>
                        <input
                          type="checkbox"
                          checked={Boolean(permiso.permitido)}
                          onChange={(e) => cambiarPermiso(permiso.nombre_permiso, e.target.checked)}
                        />
                      </label>
                    ))}
                  </div>
                </section>*/}
                <MesadaPanel idHijo={hijoSeleccionado.id_usuario} />

                <section className="cp-section">
                  <div className="cp-section-title"><div><h3>Últimas transacciones</h3><p>Solo lectura en esta fase.</p></div></div>
                  {!transacciones.length ? <p className="cp-muted">No hay transacciones registradas.</p> : (
                    <div className="cp-transactions">
                      {transacciones.map((transaccion) => (
                        <div className="cp-transaction" key={transaccion.id_transaccion}>
                          <div><strong>{transaccion.descripcion || 'Movimiento financiero'}</strong><small>{formatFechaConHora(transaccion.fecha)}</small></div>
                          <strong>{formatMoney(transaccion.monto)}</strong>
                        </div>
                      ))}
                    </div>
                  )}
                </section>
              </>
            )}
          </main>
        </div>
      )}
    </div>
  );
};

export default ControlParentalDashboardPage;
