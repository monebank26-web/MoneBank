import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(Number(val) || 0);

const fechaHoy = () => new Date().toISOString().slice(0, 10);

const ModalAbonarMeta = ({ open, onClose, meta, onAbonar }) => {
  const [form, setForm] = useState({ monto: '', fecha: fechaHoy(), descripcion: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) {
      setForm({ monto: '', fecha: fechaHoy(), descripcion: '' });
      setError('');
    }
  }, [open]);

  const handleSubmit = async () => {
    const monto = parseFloat(form.monto);
    if (!monto || monto <= 0) { setError('Ingresa un monto válido mayor a 0.'); return; }
    if (!form.fecha) { setError('La fecha del abono es obligatoria.'); return; }
    if (form.descripcion.length > 255) { setError('La descripción no puede superar 255 caracteres.'); return; }

    setLoading(true);
    setError('');
    try {
      await onAbonar({
        id_ahorro: meta.id_ahorro,
        monto,
        fecha: form.fecha,
        descripcion: form.descripcion.trim(),
      });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Abonar a la meta">
      <div className="formulario-modal">
        {meta && (
          <div className="etiqueta-saldo-disponible">
            Meta: <strong>{meta.nombre}</strong> · Llevas {formatMoney(meta.saldo_actual)} de{' '}
            {formatMoney(meta.monto_objetivo)}
          </div>
        )}
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto a abonar (COP)</label>
          <input
            className="campo-entrada"
            type="number"
            placeholder="Ej: 50000"
            min="1"
            step="1000"
            value={form.monto}
            onChange={(e) => setForm({ ...form, monto: e.target.value })}
            autoFocus
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Fecha</label>
          <input
            className="campo-entrada"
            type="date"
            value={form.fecha}
            onChange={(e) => setForm({ ...form, fecha: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional)</label>
          <input
            className="campo-entrada"
            placeholder="Ej: Ahorro de la quincena"
            maxLength={255}
            value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
          />
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Abonando...' : 'Confirmar abono'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalAbonarMeta;
