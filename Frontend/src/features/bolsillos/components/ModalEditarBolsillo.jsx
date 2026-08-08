import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';
import { COLORES_BOLSILLO } from '../../../core/constants';

const ModalEditarBolsillo = ({ open, onClose, bolsillo, onEditar }) => {
  const [form, setForm] = useState({ nombre: '', descripcion: '', color: COLORES_BOLSILLO[0] });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (bolsillo) setForm({ nombre: bolsillo.nombre, descripcion: bolsillo.descripcion || '', color: bolsillo.color });
  }, [bolsillo]);

  const handleSubmit = async () => {
    if (!form.nombre.trim()) { setError('El nombre es obligatorio.'); return; }
    setLoading(true);
    setError('');
    try {
      await onEditar(bolsillo.id, form);
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Editar bolsillo">
      <div className="formulario-modal">
        <div className="grupo-campo">
          <label className="etiqueta-campo">Nombre</label>
          <input className="campo-entrada" value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción</label>
          <input className="campo-entrada" value={form.descripcion}
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
          {loading ? 'Guardando...' : 'Guardar cambios'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalEditarBolsillo;
