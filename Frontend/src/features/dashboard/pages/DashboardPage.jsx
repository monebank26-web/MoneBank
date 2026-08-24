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
  const { user } = useAuth();
  const { bolsillos, loading, totalSaldo } = useBolsillos();
  const [transacciones, setTransacciones] = useState([]);
  const [saldoCuenta, setSaldoCuenta] = useState(0);
  const [cuentaId, setCuentaId] = useState(null);

  const [modalGasto, setModalGasto] = useState(false);
  const [montoGasto, setMontoGasto] = useState('');
  const [descripcionGasto, setDescripcionGasto] = useState('');
  const [errorGasto, setErrorGasto] = useState('');

  const handleIngreso = () => {
    alert('Pendiente: el ingreso aún no está disponible en el backend.');
  };

  const handleGasto = async () => {
    const m = parseFloat(montoGasto);
    if (!m || m <= 0) { setErrorGasto('Ingresa un monto válido.'); return; }
    if (!cuentaId) { setErrorGasto('No se encontró tu cuenta.'); return; }
    try {
      await authService.registrarGasto({
        monto: m,
        descripcion: descripcionGasto.trim() || null,
        id_cuenta: cuentaId,
      });
      const { saldo } = await authService.obtenerSaldo();
      setSaldoCuenta(saldo);
      setMontoGasto('');
      setDescripcionGasto('');
      setErrorGasto('');
      setModalGasto(false);
    } catch (err) {
      setErrorGasto(err.message);
    }
  };

  useEffect(() => {
    authService.obtenerSaldo().then(({ saldo, id_cuenta }) => {
      setSaldoCuenta(saldo);
      setCuentaId(id_cuenta);
    }).catch(() => {});
    if (user) {
      bolsillosService.historialTransacciones(user.id).then((data) => {
        setTransacciones(data.slice(0, 5));
      });
    }
  }, [user]);

  const hora = new Date().getHours();
  const saludo = hora < 12 ? 'Buenos días' : hora < 18 ? 'Buenas tardes': 'Buenas noches';

  return (
    <div className="pagina-inicio">
      {/* Header saludo */}
      <div className="encabezado-inicio">
        <div>
          <p className="saludo-inicio">{saludo},</p>
          <h1 className="nombre-inicio">{user?.nombres}</h1>
        </div>
      </div>

      {/* Tarjetas de saldo */}
      <div className="tarjeta-saldos-row">
        <div className="tarjeta-saldo tarjeta-saldo--cuenta-principal">
          <p className="etiqueta-saldo">Mi Cuenta</p>
          <h2 className="valor-saldo">{formatMoney(saldoCuenta)}</h2>
          <p className="subtexto-saldo">Saldo disponible</p>
          <div className="acciones-saldo">
            <button className="boton-saldo" onClick={handleIngreso}>
              + Ingreso
            </button>
            <button className="boton-saldo" onClick={() => setModalGasto(true)}>
              − Gasto
            </button>
          </div>
        </div>

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

      {/* Modal Gasto */}
      <Modal open={modalGasto} onClose={() => setModalGasto(false)} title="Registrar gasto">
        <div className="formulario-modal">
          <p style={{ color: 'var(--color-text-soft)', fontSize: '13px' }}>
            Saldo actual: <strong style={{ color: 'var(--color-accent)' }}>{formatMoney(saldoCuenta)}</strong>
          </p>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Monto (COP)</label>
            <input className="campo-entrada" type="number" placeholder="Ej: 50000"
              min="1" step="1" value={montoGasto}
              onChange={(e) => setMontoGasto(e.target.value)} />
          </div>
          <div className="grupo-campo">
            <label className="etiqueta-campo">Descripción (opcional, máx. 255)</label>
            <input className="campo-entrada" type="text" placeholder="Ej: Almuerzo"
              maxLength={255} value={descripcionGasto}
              onChange={(e) => setDescripcionGasto(e.target.value)} />
          </div>
          {errorGasto && <p className="error-formulario">{errorGasto}</p>}
          <button className="boton-principal" onClick={handleGasto}>Registrar gasto</button>
        </div>
      </Modal>
    </div>
  );
};

export default DashboardPage;
