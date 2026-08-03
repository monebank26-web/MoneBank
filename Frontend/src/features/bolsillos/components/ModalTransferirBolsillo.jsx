import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

const ModalTransferirBolsillo = ({ open, onClose, bolsillos, bolsilloOrigen, onTransferir }) => {
  const [form, setForm] = useState({ origenId: '', destinoId: '', monto: '', descripcion: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (bolsilloOrigen) setForm((f) => ({ ...f, origenId: bolsilloOrigen.id }));
  }, [bolsilloOrigen]);

  const handleSubmit = async () => {
    const m = parseFloat(form.monto);
    if (!form.origenId) { setError('Selecciona el bolsillo origen.'); return; }
    if (!form.destinoId) { setError('Selecciona el bolsillo destino.'); return; }
    if (form.origenId === form.destinoId) { setError('El origen y destino no pueden ser iguales.'); return; }
    if (!m || m <= 0) { setError('Ingresa un monto válido.'); return; }
    setLoading(true);
    setError('');
    try {
      await onTransferir({ origenId: form.origenId, destinoId: form.destinoId, monto: m, descripcion: form.descripcion });
      setForm({ origenId: '', destinoId: '', monto: '', descripcion: '' });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Transferir entre bolsillos">
      <div className="formulario-modal">
        <div className="grupo-campo">
          <label className="etiqueta-campo">Desde</label>
          <select className="campo-entrada campo-seleccion" value={form.origenId}
            onChange={(e) => setForm({ ...form, origenId: e.target.value })}>
            <option value="">Selecciona bolsillo origen</option>
            {bolsillos.map((b) => (
              <option key={b.id} value={b.id}>{b.nombre} — {formatMoney(b.saldo)}</option>
            ))}
          </select>
        </div>
        <div className="flecha-transferencia">↓</div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Hacia</label>
          <select className="campo-entrada campo-seleccion" value={form.destinoId}
            onChange={(e) => setForm({ ...form, destinoId: e.target.value })}>
            <option value="">Selecciona bolsillo destino</option>
            {bolsillos.filter((b) => b.id !== form.origenId).map((b) => (
              <option key={b.id} value={b.id}>{b.nombre} — {formatMoney(b.saldo)}</option>
            ))}
          </select>
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto (COP)</label>
          <input className="campo-entrada" type="number" placeholder="0" min="1"
            value={form.monto} onChange={(e) => setForm({ ...form, monto: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional)</label>
          <input className="campo-entrada" placeholder="¿Para qué es esta transferencia?" value={form.descripcion}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Transfiriendo...' : 'Transferir'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalTransferirBolsillo;
