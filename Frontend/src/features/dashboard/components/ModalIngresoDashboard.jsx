import React, { useEffect, useState } from 'react';
import Modal from '../../../shared/components/Modal';
import { transaccionesService } from '../../transacciones/services/transaccionesService';
import '../../../shared/styles/transacciones-modal.css';
import './ModalTransaccion.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

const ModalIngresoDashboard = ({ open, onClose, saldoCuenta }) => {
  const [montoIngreso, setMontoIngreso] = useState('');
  const [descripcionIngreso, setDescripcionIngreso] = useState('');
  const [errorIngreso, setErrorIngreso] = useState('');
  const [categoriasIngreso, setCategoriasIngreso] = useState([]);
  const [idCategoriaIngreso, setIdCategoriaIngreso] = useState('');
  const [cuentaId, setCuentaId] = useState(null);
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    if (!open || categoriasIngreso.length > 0) return;
    transaccionesService.listarCategorias()
      .then((data) => setCategoriasIngreso(
        (Array.isArray(data) ? data : []).filter((c) => c.tipo_categoria === 'INGRESO')
      ))
      .catch(() => {});
  }, [open, categoriasIngreso.length]);

  useEffect(() => {
    if (!open) return;
    import('../../auth/services/authService').then(({ authService }) =>
      authService.obtenerSaldo().then(({ id_cuenta }) => setCuentaId(id_cuenta)).catch(() => {})
    );
  }, [open]);

  const handleIngreso = async () => {
    const m = parseFloat(montoIngreso);
    if (!m || m <= 0) { setErrorIngreso('Ingresa un monto válido.'); return; }
    if (!idCategoriaIngreso) { setErrorIngreso('Selecciona una categoría.'); return; }
    if (!cuentaId) { setErrorIngreso('No se encontró tu cuenta.'); return; }
    setGuardando(true);
    try {
      await transaccionesService.registrarIngreso({
        monto: m,
        descripcion: descripcionIngreso.trim() || null,
        id_cuenta: cuentaId,
        id_categoria: parseInt(idCategoriaIngreso, 10),
      });
      const { authService } = await import('../../auth/services/authService');
      const { saldo } = await authService.obtenerSaldo();
      setMontoIngreso('');
      setDescripcionIngreso('');
      setIdCategoriaIngreso('');
      setErrorIngreso('');
      onClose(saldo);
    } catch (err) {
      setErrorIngreso(err.message);
    } finally {
      setGuardando(false);
    }
  };

  const handleClose = () => {
    setMontoIngreso('');
    setDescripcionIngreso('');
    setIdCategoriaIngreso('');
    setErrorIngreso('');
    onClose();
  };

  return (
    <Modal open={open} onClose={handleClose} title="Registrar ingreso">
      <div className="formulario-modal">
        <p style={{ color: 'var(--color-text-soft)', fontSize: '13px' }}>
          Saldo actual: <strong style={{ color: 'var(--color-accent)' }}>{formatMoney(saldoCuenta)}</strong>
        </p>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto (COP)</label>
          <input className="campo-entrada" type="number" placeholder="Ej: 50000"
            min="1" step="1" value={montoIngreso}
            onChange={(e) => setMontoIngreso(e.target.value)} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Categoría</label>
          {categoriasIngreso.length === 0 ? (
            <select className="campo-entrada campo-seleccion" disabled>
              <option>Cargando categorías...</option>
            </select>
          ) : (
            <select
              className="campo-entrada campo-seleccion"
              value={idCategoriaIngreso}
              onChange={(e) => setIdCategoriaIngreso(e.target.value)}
            >
              <option value="">Selecciona una categoría...</option>
              {categoriasIngreso.map((c) => (
                <option key={c.id_categoria} value={c.id_categoria}>
                  {c.nombre_categoria}
                </option>
              ))}
            </select>
          )}
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional, máx. 255)</label>
          <input className="campo-entrada" type="text" placeholder="Ej: Salario"
            maxLength={255} value={descripcionIngreso}
            onChange={(e) => setDescripcionIngreso(e.target.value)} />
        </div>
        {errorIngreso && <p className="error-formulario">{errorIngreso}</p>}
        <button
          className="boton-principal"
          onClick={handleIngreso}
          disabled={guardando}
        >
          {guardando ? 'Registrando...' : 'Registrar ingreso'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalIngresoDashboard;
