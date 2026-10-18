import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';
import '../../../shared/styles/transacciones-modal.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(Number(val) || 0);

const aCadena = (d) =>
  `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

const fechaManana = () => {
  const d = new Date();
  d.setDate(d.getDate() + 1);
  return aCadena(d);
};

const FRECUENCIAS = [
  { valor: 'DIARIA', etiqueta: 'Diaria' },
  { valor: 'SEMANAL', etiqueta: 'Semanal' },
  { valor: 'QUINCENAL', etiqueta: 'Quincenal' },
  { valor: 'MENSUAL', etiqueta: 'Mensual' },
  { valor: 'TRIMESTRAL', etiqueta: 'Trimestral' },
  { valor: 'SEMESTRAL', etiqueta: 'Semestral' },
  { valor: 'ANUAL', etiqueta: 'Anual' },
];

const ModalProgramarAporte = ({ open, onClose, meta, onProgramar }) => {
  const [form, setForm] = useState({
    monto_periodico: '',
    frecuencia: 'MENSUAL',
    fecha_cobro: fechaManana(),
    fecha_fin: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) {
      setForm({
        monto_periodico: '',
        frecuencia: 'MENSUAL',
        fecha_cobro: fechaManana(),
        fecha_fin: '',
      });
      setError('');
    }
  }, [open]);

  const handleSubmit = async () => {
    const monto = parseFloat(form.monto_periodico);
    if (!monto || monto <= 0) { setError('Ingresa un monto válido mayor a 0.'); return; }
    if (!form.fecha_cobro) { setError('La fecha de cobro es obligatoria.'); return; }
    if (form.fecha_cobro < fechaManana()) { setError('La fecha de cobro debe ser posterior a hoy.'); return; }
    if (form.fecha_fin && form.fecha_fin < form.fecha_cobro) {
      setError('La fecha final debe ser mayor o igual a la fecha de cobro.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await onProgramar({
        id_ahorro: meta.id_ahorro,
        monto_periodico: monto,
        frecuencia: form.frecuencia,
        fecha_cobro: form.fecha_cobro,
        fecha_fin: form.fecha_fin || null,
      });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Programar aporte automático">
      <div className="formulario-modal">
        {meta && (
          <div className="etiqueta-saldo-disponible">
            Meta: <strong>{meta.nombre}</strong> · Llevas {formatMoney(meta.saldo_actual)} de{' '}
            {formatMoney(meta.monto_objetivo)}
          </div>
        )}
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto por periodo (COP)</label>
          <input
            className="campo-entrada"
            type="number"
            placeholder="Ej: 50000"
            min="1"
            step="1000"
            value={form.monto_periodico}
            onChange={(e) => setForm({ ...form, monto_periodico: e.target.value })}
            autoFocus
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Frecuencia</label>
          <select
            className="campo-entrada"
            value={form.frecuencia}
            onChange={(e) => setForm({ ...form, frecuencia: e.target.value })}
          >
            {FRECUENCIAS.map((frecuencia) => (
              <option key={frecuencia.valor} value={frecuencia.valor}>
                {frecuencia.etiqueta}
              </option>
            ))}
          </select>
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Primera fecha de cobro</label>
          <input
            className="campo-entrada campo-entrada--fecha"
            type="date"
            min={fechaManana()}
            value={form.fecha_cobro}
            onChange={(e) => setForm({ ...form, fecha_cobro: e.target.value })}
          />
          <p className="ayuda-campo-fecha">Debe ser posterior a hoy.</p>
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Fecha final (opcional)</label>
          <input
            className="campo-entrada campo-entrada--fecha"
            type="date"
            min={form.fecha_cobro || fechaManana()}
            value={form.fecha_fin}
            onChange={(e) => setForm({ ...form, fecha_fin: e.target.value })}
          />
          <p className="ayuda-campo-fecha">Si la dejas vacía, se mantiene hasta que la pauses.</p>
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Guardando...' : 'Guardar programación'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalProgramarAporte;