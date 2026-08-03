import React, { useState } from 'react';
import Modal from '../../../shared/components/Modal';

const ModalDepositarBolsillo = ({ open, onClose, bolsillo, onDepositar }) => {
  const [monto, setMonto] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    const m = parseFloat(monto);
    if (!m || m <= 0) { setError('Ingresa un monto válido.'); return; }
    setLoading(true);
    setError('');
    try {
      await onDepositar({ bolsilloId: bolsillo.id, monto: m, descripcion });
      setMonto('');
      setDescripcion('');
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title={`Añadir dinero · ${bolsillo?.nombre}`}>
      <div className="formulario-modal">
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto (COP)</label>
          <input className="campo-entrada" type="number" placeholder="0" min="1"
            value={monto} onChange={(e) => setMonto(e.target.value)} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional)</label>
          <input className="campo-entrada" placeholder="Ej: Salario, venta..." value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)} />
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Procesando...' : 'Añadir dinero'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalDepositarBolsillo;
