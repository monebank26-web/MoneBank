// features/bolsillos/pages/BolsillosPage.jsx
import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useBolsillos } from '../hooks/useBolsillos';
import Modal from '../../../shared/components/Modal';
import ModalEditarBolsillo from '../components/ModalEditarBolsillo';
import ModalDepositarBolsillo from '../components/ModalDepositarBolsillo';
import ModalTransferirBolsillo from '../components/ModalTransferirBolsillo';
import { COLORES_BOLSILLO } from '../../../core/constants';
import './BolsillosPage.css';
import { useAuth } from '../../../core/context/AuthContext';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

// ─── MENU TRES PUNTOS ───────────────────────────────────────────
const MenuOpciones = ({ onEditar, onEliminar, onDepositar, onTransferir }) => {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handleClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  return (
    <div className="menu-opciones-bolsillo" ref={ref}>
      <button className="boton-menu-opciones-bolsillo" onClick={() => setOpen(!open)}>⋮</button>
      {open && (
        <div className="desplegable-menu-opciones-bolsillo">
          <button onClick={() => { onDepositar(); setOpen(false); }}>Añadir dinero</button>
          <button onClick={() => { onTransferir(); setOpen(false); }}>Transferir</button>
          <button onClick={() => { onEditar(); setOpen(false); }}>Editar</button>
          <div className="separador-menu-opciones-bolsillo" />
          <button className="opcion-peligrosa" onClick={() => { onEliminar(); setOpen(false); }}>Eliminar</button>
        </div>
      )}
    </div>
  );
};

// ─── MODAL CREAR ────────────────────────────────────────────────
const ModalCrear = ({ open, onClose, onCreate, saldoDisponible }) => {
  const [form, setForm] = useState({ nombre: '', descripcion: '', color: COLORES_BOLSILLO[0], montoInicial: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const formatMoney = (val) =>
    new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

  const handleSubmit = async () => {
    if (!form.nombre.trim()) { setError('El nombre es obligatorio.'); return; }
    setLoading(true);
    setError('');
    try {
      await onCreate(form);
      setForm({ nombre: '', descripcion: '', color: COLORES_BOLSILLO[0], montoInicial: '' });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Nuevo bolsillo">
      <div className="formulario-modal">
        <div className="etiqueta-saldo-disponible">
          Disponible en Mi Cuenta: <strong>{formatMoney(saldoDisponible)}</strong>
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Nombre del bolsillo</label>
          <input className="campo-entrada" placeholder="Ej: Vacaciones, Ahorro..." value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto inicial (COP)</label>
          <input className="campo-entrada" type="number" placeholder="0" min="0"
            value={form.montoInicial} onChange={(e) => setForm({ ...form, montoInicial: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional)</label>
          <input className="campo-entrada" placeholder="Para qué es este bolsillo..." value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Color</label>
          <div className="selector-color">
            {COLORES_BOLSILLO.map((c) => (
              <button key={c} className={`circulo-color ${form.color === c ? 'circulo-color--activo' : ''}`}
                style={{ background: c }} onClick={() => setForm({ ...form, color: c })} />
            ))}
          </div>
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Creando...' : 'Crear bolsillo'}
        </button>
      </div>
    </Modal>
  );
};

// ─── PÁGINA PRINCIPAL ───────────────────────────────────────────
const BolsillosPage = () => {
  const { bolsillos, loading, totalSaldo, crear, eliminar, transferir, depositar, editar } = useBolsillos();
  const { user } = useAuth();
  const [modalCrear, setModalCrear] = useState(false);
  const [modalDepositar, setModalDepositar] = useState(null);
  const [modalTransferir, setModalTransferir] = useState(false);
  const [modalEditar, setModalEditar] = useState(null);
  const [bolsilloOrigen, setBolsilloOrigen] = useState(null);
  const [confirmEliminar, setConfirmEliminar] = useState(null);

  const handleEliminar = async (id) => {
    await eliminar(id);
    setConfirmEliminar(null);
  };

  const abrirTransferir = (bolsillo = null) => {
    setBolsilloOrigen(bolsillo);
    setModalTransferir(true);
  };

  return (
    <div className="pagina-bolsillos">
      <div className="encabezado-bolsillos">
        <div>
          <h1 className="titulo-pagina">Mis bolsillos</h1>
          <p className="subtitulo-pagina">Total acumulado: <strong>{formatMoney(totalSaldo)}</strong></p>
        </div>
        <div className="acciones-bolsillos">
          <button className="boton-secundario" onClick={() => abrirTransferir()}>Transferir</button>
          <button className="boton-principal-pequeno" onClick={() => setModalCrear(true)}>+ Nuevo bolsillo</button>
        </div>
      </div>

      {loading ? (
        <p className="cargando-pagina">Cargando bolsillos...</p>
      ) : bolsillos.length === 0 ? (
        <div className="bolsillos-sin-contenido">
          <div className="icono-sin-contenido">◈</div>
          <h3>No tienes bolsillos aún</h3>
          <p>Crea tu primer bolsillo para empezar a organizar tu dinero.</p>
          <button className="boton-principal" onClick={() => setModalCrear(true)}>Crear bolsillo</button>
        </div>
      ) : (
        <div className="lista-bolsillos">
          {bolsillos.map((b) => (
            <div key={b.id} className="tarjeta-bolsillo" style={{ '--color': b.color }}>
              <div className="parte-superior-tarjeta-bolsillo">
                <div className="indicador-color-bolsillo" />
                <Link to={`/bolsillos/${b.id}`} className="informacion-tarjeta-bolsillo">
                  <h3 className="nombre-tarjeta-bolsillo">{b.nombre}</h3>
                  {b.descripcion && <p className="descripcion-tarjeta-bolsillo">{b.descripcion}</p>}
                </Link>
                <MenuOpciones
                  onDepositar={() => setModalDepositar(b)}
                  onTransferir={() => abrirTransferir(b)}
                  onEditar={() => setModalEditar(b)}
                  onEliminar={() => setConfirmEliminar(b)}
                />
              </div>
              <Link to={`/bolsillos/${b.id}`} className="saldo-tarjeta-bolsillo saldo-tarjeta-bolsillo--enlace">
                {formatMoney(b.saldo)}
              </Link>
            </div>
          ))}
        </div>
      )}

      <ModalCrear open={modalCrear} onClose={() => setModalCrear(false)} onCreate={crear}saldoDisponible={user?.saldoCuenta || 0}/>
      <ModalEditarBolsillo open={!!modalEditar} onClose={() => setModalEditar(null)} bolsillo={modalEditar} onEditar={editar} />
      <ModalDepositarBolsillo open={!!modalDepositar} onClose={() => setModalDepositar(null)} bolsillo={modalDepositar} onDepositar={depositar} />
      <ModalTransferirBolsillo open={modalTransferir} onClose={() => { setModalTransferir(false); setBolsilloOrigen(null); }}
        bolsillos={bolsillos} bolsilloOrigen={bolsilloOrigen} onTransferir={transferir} />

      <Modal open={!!confirmEliminar} onClose={() => setConfirmEliminar(null)} title="Eliminar bolsillo">
        <div className="formulario-modal">
          <p style={{ color: 'var(--color-text-soft)', fontSize: '14px', marginBottom: '20px' }}>
            ¿Estás seguro de eliminar <strong style={{ color: 'var(--color-text)' }}>{confirmEliminar?.nombre}</strong>?
            {confirmEliminar?.saldo > 0 && (
              <span style={{ color: 'var(--color-warning)', display: 'block', marginTop: '8px' }}>
                Este bolsillo tiene {formatMoney(confirmEliminar?.saldo)} en saldo.
              </span>
            )}
          </p>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button className="boton-secundario" style={{ flex: 1 }} onClick={() => setConfirmEliminar(null)}>Cancelar</button>
            <button className="boton-peligro" style={{ flex: 1 }} onClick={() => handleEliminar(confirmEliminar.id)}>Eliminar</button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default BolsillosPage;