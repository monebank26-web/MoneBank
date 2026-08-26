import React, { useState } from 'react';
import Modal from '../../../shared/components/Modal';
import { COLORES_BOLSILLO } from '../../../core/constants';
import { formatMoney } from '../../../core/utils/format';

const ModalCrearBolsillo = ({ open, onClose, onCrear, saldoDisponible }) => {
  const [formulario, setFormulario] = useState({ nombre: '', descripcion: '', color: COLORES_BOLSILLO[0], montoInicial: '' });
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);

  const handleCrear = async () => {
    if (!formulario.nombre.trim()) { setError('El nombre es obligatorio.'); return; }
    setCargando(true);
    setError('');
    try {
      await onCrear(formulario);
      setFormulario({ nombre: '', descripcion: '', color: COLORES_BOLSILLO[0], montoInicial: '' });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setCargando(false);
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
          <input className="campo-entrada" placeholder="Ej: Vacaciones, Ahorro..." value={formulario.nombre}
            onChange={(e) => setFormulario({ ...formulario, nombre: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto inicial (COP)</label>
          <input className="campo-entrada" type="number" placeholder="0" min="0"
            value={formulario.montoInicial} onChange={(e) => setFormulario({ ...formulario, montoInicial: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional)</label>
          <input className="campo-entrada" placeholder="Para qué es este bolsillo..." value={formulario.descripcion}
            onChange={(e) => setFormulario({ ...formulario, descripcion: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Color</label>
          <div className="selector-color">
            {COLORES_BOLSILLO.map((color) => (
              <button key={color} className={`circulo-color ${formulario.color === color ? 'circulo-color--activo' : ''}`}
                style={{ background: color }} onClick={() => setFormulario({ ...formulario, color })} />
            ))}
          </div>
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleCrear} disabled={cargando}>
          {cargando ? 'Creando...' : 'Crear bolsillo'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalCrearBolsillo;
