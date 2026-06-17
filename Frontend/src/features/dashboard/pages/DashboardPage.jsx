// features/dashboard/pages/DashboardPage.jsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../../core/context/AuthContext';
import { useBolsillos } from '../../bolsillos/hooks/useBolsillos';
import { bolsillosService } from '../../bolsillos/services/bolsillosService';
import { authService } from '../../auth/services/authService';
import Modal from '../../../shared/components/Modal';
import { ROUTES } from '../../../core/constants';
import './DashboardPage.css';
const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

const DashboardPage = () => {
  const { user, login } = useAuth();
  const { bolsillos, loading, totalSaldo } = useBolsillos();
  const [transacciones, setTransacciones] = useState([]);
  const [modalConsignar, setModalConsignar] = useState(false);
  const [montoConsignar, setMontoConsignar] = useState('');
  const [errorConsignar, setErrorConsignar] = useState('');


 const handleConsignar = () => {
  const m = parseInt(montoConsignar, 10);
  if (!m || m <= 0) { setErrorConsignar('Ingresa un monto válido.'); return; }
  const nuevoSaldo = (user.saldoCuenta || 0) + m;
  authService.actualizarSaldo(user.id, nuevoSaldo);
  login({ ...user, saldoCuenta: nuevoSaldo });
  setMontoConsignar('');
  setErrorConsignar('');
  setModalConsignar(false);
};

  useEffect(() => {
    if (user) {
      bolsillosService.historialTransacciones(user.id).then((data) => {
        setTransacciones(data.slice(0, 5));
      });
    }
  }, [user]);

  const hora = new Date().getHours();
  const saludo = hora < 12 ? 'Buenos días' : hora < 18 ? 'Buenas tardes' : 'Buenas noches';

  return (
    <div className="pagina-inicio">
      {/* Header saludo */}
      <div className="encabezado-inicio">
        <div>
          <p className="saludo-inicio">{saludo},</p>
          <h1 className="nombre-inicio">{user?.nombre}</h1>
        </div>
      </div>

      {/* Tarjetas de saldo */}
      <div className="tarjeta-saldos-row">
       {/* Mi Cuenta */}
        <div className="tarjeta-saldo tarjeta-saldo--cuenta-principal">
          <p className="etiqueta-saldo">Mi Cuenta</p>
          <h2 className="valor-saldo">{formatMoney(user?.saldoCuenta || 0)}</h2>
          <p className="subtexto-saldo">Saldo disponible para bolsillos</p>
        <div className="acciones-saldo">
        <button className="boton-saldo" onClick={() => setModalConsignar(true)}>
      + Consignar
      </button>
    </div>
  </div>

        {/* Bolsillos */}
        <div className="tarjeta-saldo tarjeta-saldo--bolsillos">
          <p className="etiqueta-saldo">En bolsillos</p>
          <h2 className="valor-saldo">{formatMoney(totalSaldo)}</h2>
          <p className="subtexto-saldo">{bolsillos.length} bolsillo{bolsillos.length !== 1 ? 's' : ''} activo{bolsillos.length !== 1 ? 's' : ''}</p>
          <div className="acciones-saldo">
            <Link to={ROUTES.BOLSILLOS} className="boton-saldo">Ver bolsillos →</Link>
          </div>
        </div>
      </div>

      {/* Bolsillos */}
      <section className="seccion-inicio">
        <div className="encabezado-seccion-inicio">
          <h3>Mis bolsillos</h3>
          <Link to={ROUTES.BOLSILLOS} className="enlace-ver-todos">Ver todos</Link>
        </div>

        {loading ? (
          <p className="cargando-inicio">Cargando...</p>
        ) : bolsillos.length === 0 ? (
          <div className="seccion-vacia-inicio">
            <p>Todavía no tienes bolsillos.</p>
            <Link to={ROUTES.BOLSILLOS} className="boton-llamada-accion">Crear mi primer bolsillo</Link>
          </div>
        ) : (
          <div className="cuadricula-bolsillos">
            {bolsillos.slice(0, 4).map((b) => (
              <div key={b.id} className="bolsillo-miniatura" style={{ '--color': b.color }}>
                <div className="punto-bolsillo-miniaturaatura" />
                <div>
                  <p className="nombre-bolsillo-miniaturaatura">{b.nombre}</p>
                  <p className="saldo-bolsillo-miniaturaatura">{formatMoney(b.saldo)}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Últimos movimientos */}
      <section className="seccion-inicio">
        <div className="encabezado-seccion-inicio">
          <h3>Últimos movimientos</h3>
          <Link to={ROUTES.TRANSACCIONES} className="enlace-ver-todos">Ver todos</Link>
        </div>

        {transacciones.length === 0 ? (
          <p className="seccion-vacia-inicio-text">Sin movimientos aún.</p>
        ) : (
          <div className="lista-movimientos">
            {transacciones.map((tx) => (
              <div key={tx.id} className="elemento-movimiento">
                <div className={`icono-movimiento icono-movimiento--${tx.tipo}`}>
                  {tx.tipo === 'transferencia' ? '↔' : '↓'}
                </div>
                <div className="informacion-movimiento">
                  <p className="descripcion-movimiento">
                    {tx.tipo === 'transferencia'
                      ? `${tx.origenNombre} → ${tx.destinoNombre}`
                      : `Depósito en ${tx.destinoNombre}`}
                  </p>
                  <p className="fecha-movimiento">{new Date(tx.fecha).toLocaleDateString('es-CO')}</p>
                </div>
                <p className={`monto-movimiento monto-movimiento--${tx.tipo}`}>
                  {tx.tipo === 'deposito' ? '+' : ''}{formatMoney(tx.monto)}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>
      <Modal open={modalConsignar} onClose={() => setModalConsignar(false)} title="Consignar a Mi Cuenta">
  <div className="formulario-modal">
    <p style={{ color: 'var(--color-text-soft)', fontSize: '13px' }}>
      Saldo actual: <strong style={{ color: 'var(--color-accent)' }}>{formatMoney(user?.saldoCuenta || 0)}</strong>
    </p>
    <div className="grupo-campo">
      <label className="etiqueta-campo">Monto a consignar (COP)</label>
      <input className="campo-entrada" type="number" placeholder="Ej: 300000" min="1000" step="1"value={montoConsignar} onChange={(e) => setMontoConsignar(e.target.value)} 
/>
    </div>
    {errorConsignar && <p className="error-formulario">{errorConsignar}</p>}
    <button className="boton-principal" onClick={handleConsignar}>
      Consignar
    </button>
  </div>
</Modal>
    </div>
  );
};

export default DashboardPage;