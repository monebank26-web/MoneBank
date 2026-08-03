import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../../core/context/AuthContext';
import { useBolsillos } from '../hooks/useBolsillos';
import { bolsillosService } from '../services/bolsillosService';
import Modal from '../../../shared/components/Modal';
import ModalEditarBolsillo from '../components/ModalEditarBolsillo';
import ModalDepositarBolsillo from '../components/ModalDepositarBolsillo';
import ModalTransferirBolsillo from '../components/ModalTransferirBolsillo';
import { ROUTES } from '../../../core/constants';
import './BolsilloDetallePage.css';
import '../../transacciones/pages/TransaccionesPage.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val || 0);

const formatFecha = (iso) =>
  new Date(iso).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });

const BolsilloDetallePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { bolsillos, editar, depositar, transferir, eliminar } = useBolsillos();

  const [bolsillo, setBolsillo] = useState(null);
  const [movimientos, setMovimientos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [noEncontrado, setNoEncontrado] = useState(false);

  const [modalEditar, setModalEditar] = useState(false);
  const [modalDepositar, setModalDepositar] = useState(false);
  const [modalTransferir, setModalTransferir] = useState(false);
  const [confirmEliminar, setConfirmEliminar] = useState(false);

  const cargarDatos = useCallback(async () => {
    if (!user) return;
    setCargando(true);
    try {
      const encontrado = await bolsillosService.obtener(id, user.id);
      setBolsillo(encontrado);
      const historial = await bolsillosService.historialTransacciones(user.id, id);
      setMovimientos(historial);
      setNoEncontrado(false);
    } catch (e) {
      setNoEncontrado(true);
    } finally {
      setCargando(false);
    }
  }, [id, user]);

  useEffect(() => { cargarDatos(); }, [cargarDatos]);

  useEffect(() => {
    const actualizado = bolsillos.find((b) => b.id === id);
    if (actualizado) setBolsillo(actualizado);
  }, [bolsillos, id]);

  const handleEditar = async (bolsilloId, datos) => {
    await editar(bolsilloId, datos);
    await cargarDatos();
  };

  const handleDepositar = async (datos) => {
    const resultado = await depositar(datos);
    await cargarDatos();
    return resultado;
  };

  const handleTransferir = async (datos) => {
    const resultado = await transferir(datos);
    await cargarDatos();
    return resultado;
  };

  const handleEliminar = async () => {
    await eliminar(id);
    navigate(ROUTES.BOLSILLOS);
  };

  if (cargando) {
    return <p className="cargando-pagina">Cargando bolsillo...</p>;
  }

  if (noEncontrado || !bolsillo) {
    return (
      <div className="pagina-detalle-bolsillo">
        <Link to={ROUTES.BOLSILLOS} className="enlace-volver-detalle">← Volver a bolsillos</Link>
        <div className="detalle-sin-contenido">
          <div className="icono-sin-contenido">◈</div>
          <h3>No encontramos este bolsillo</h3>
          <p>Puede que haya sido eliminado o que el enlace no sea correcto.</p>
          <Link to={ROUTES.BOLSILLOS} className="boton-principal">Ver mis bolsillos</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="pagina-detalle-bolsillo">
      <Link to={ROUTES.BOLSILLOS} className="enlace-volver-detalle">← Volver a bolsillos</Link>

      <div className="tarjeta-cabecera-detalle" style={{ '--color': bolsillo.color }}>
        <div className="franja-color-detalle" />
        <div className="contenido-cabecera-detalle">
          <div className="titulo-cabecera-detalle">
            <span className="punto-color-detalle" />
            <h1 className="nombre-detalle-bolsillo">{bolsillo.nombre}</h1>
          </div>
          {bolsillo.descripcion && <p className="descripcion-detalle-bolsillo">{bolsillo.descripcion}</p>}
          <p className="saldo-detalle-bolsillo">{formatMoney(bolsillo.saldo)}</p>

          <div className="acciones-detalle-bolsillo">
            <button className="boton-tarjeta boton-tarjeta--agregar-dinero" onClick={() => setModalDepositar(true)}>
              + Añadir dinero
            </button>
            <button className="boton-tarjeta boton-tarjeta--transferir" onClick={() => setModalTransferir(true)}>
              ↔ Transferir
            </button>
            <button className="boton-secundario" onClick={() => setModalEditar(true)}>Editar</button>
            <button className="boton-secundario boton-secundario--peligro" onClick={() => setConfirmEliminar(true)}>
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <div className="seccion-detalle-bolsillo">
        <h3 className="titulo-seccion-detalle">Movimientos de este bolsillo</h3>
        {movimientos.length === 0 ? (
          <p className="sin-movimientos-parental">Aún no hay movimientos en este bolsillo.</p>
        ) : (
          <div className="lista-movimientos-completa">
            {movimientos.map((tx) => (
              <div key={tx.id} className="elemento-movimiento-completo">
                <div className={`icono-elemento-movimiento icono-movimiento--${tx.tipo}`}>
                  {tx.tipo === 'transferencia' ? '↔' : '↓'}
                </div>
                <div className="informacion-elemento-movimiento">
                  <p className="descripcion-elemento-movimiento">
                    {tx.tipo === 'transferencia'
                      ? `Transferencia: ${tx.origenNombre} → ${tx.destinoNombre}`
                      : `Depósito en ${tx.destinoNombre}`}
                  </p>
                  {tx.descripcion && <p className="nota-elemento-movimiento">"{tx.descripcion}"</p>}
                  <p className="fecha-movimiento">{formatFecha(tx.fecha)}</p>
                </div>
                <div className="columna-derecha-movimiento">
                  <p className={`monto-movimiento monto-movimiento--${tx.tipo}`}>
                    {tx.tipo === 'deposito' ? '+' : ''}{formatMoney(tx.monto)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <ModalEditarBolsillo open={modalEditar} onClose={() => setModalEditar(false)} bolsillo={bolsillo} onEditar={handleEditar} />
      <ModalDepositarBolsillo open={modalDepositar} onClose={() => setModalDepositar(false)} bolsillo={bolsillo} onDepositar={handleDepositar} />
      <ModalTransferirBolsillo
        open={modalTransferir}
        onClose={() => setModalTransferir(false)}
        bolsillos={bolsillos}
        bolsilloOrigen={bolsillo}
        onTransferir={handleTransferir}
      />

      <Modal open={confirmEliminar} onClose={() => setConfirmEliminar(false)} title="Eliminar bolsillo">
        <div className="formulario-modal">
          <p style={{ color: 'var(--color-text-soft)', fontSize: '14px', marginBottom: '20px' }}>
            ¿Estás seguro de eliminar <strong style={{ color: 'var(--color-text)' }}>{bolsillo.nombre}</strong>?
            {bolsillo.saldo > 0 && (
              <span style={{ color: 'var(--color-warning)', display: 'block', marginTop: '8px' }}>
                Este bolsillo tiene {formatMoney(bolsillo.saldo)} en saldo, que volverá a Mi Cuenta.
              </span>
            )}
          </p>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button className="boton-secundario" style={{ flex: 1 }} onClick={() => setConfirmEliminar(false)}>Cancelar</button>
            <button className="boton-peligro" style={{ flex: 1 }} onClick={handleEliminar}>Eliminar</button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default BolsilloDetallePage;
