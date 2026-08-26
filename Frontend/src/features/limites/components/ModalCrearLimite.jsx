import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';
import { limitesService } from '../services/limitesService';
import { PERIODOS_LIMITE } from '../../../core/constants';

const ETIQUETAS_PERIODO = {
  DIARIO: 'Diario',
  SEMANAL: 'Semanal',
  MENSUAL: 'Mensual',
};

const ModalCrearLimite = ({ open, onClose, onCrear }) => {
  const [form, setForm] = useState({ nombre: '', monto_limite: '', periodo: 'MENSUAL', id_categoria: '' });
  const [categorias, setCategorias] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open) return;
    limitesService.listarCategoriasGasto()
      .then(setCategorias)
      .catch((err) => setError(`No se pudieron cargar las categorías: ${err.message}`));
  }, [open]);

  const handleSubmit = async () => {
    if (form.nombre.trim().length > 100) { setError('El nombre no puede superar 100 caracteres.'); return; }
    const monto = parseFloat(form.monto_limite);
    if (!monto || monto <= 0) { setError('El monto del límite debe ser mayor a 0.'); return; }
    if (!PERIODOS_LIMITE.includes(form.periodo)) { setError('Selecciona un periodo válido.'); return; }
    if (!form.id_categoria) { setError('Selecciona una categoría.'); return; }

    setLoading(true);
    setError('');
    try {
      await onCrear({
        nombre: form.nombre.trim(),
        monto_limite: monto,
        periodo: form.periodo,
        id_categoria: parseInt(form.id_categoria, 10),
      });
      setForm({ nombre: '', monto_limite: '', periodo: 'MENSUAL', id_categoria: '' });
      onClose();
    } catch (e) {
      if (/duplicado/i.test(e.message)) {
        setError('Ya tienes un límite activo para esa categoría en ese periodo.');
      } else {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Nuevo límite de gasto">
      <div className="formulario-modal">
        <div className="grupo-campo">
          <label className="etiqueta-campo">Nombre (opcional)</label>
          <input
            className="campo-entrada"
            placeholder="Se genera automáticamente si lo dejas vacío"
            maxLength={100}
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto límite (COP)</label>
          <input
            className="campo-entrada"
            type="number"
            placeholder="Ej: 200000"
            min="1"
            step="1000"
            value={form.monto_limite}
            onChange={(e) => setForm({ ...form, monto_limite: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Periodo</label>
          <select
            className="campo-entrada campo-seleccion"
            value={form.periodo}
            onChange={(e) => setForm({ ...form, periodo: e.target.value })}
          >
            {PERIODOS_LIMITE.map((p) => (
              <option key={p} value={p}>{ETIQUETAS_PERIODO[p]}</option>
            ))}
          </select>
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Categoría de gasto</label>
          <select
            className="campo-entrada campo-seleccion"
            value={form.id_categoria}
            onChange={(e) => setForm({ ...form, id_categoria: e.target.value })}
          >
            <option value="">Selecciona una categoría...</option>
            {categorias.map((c) => (
              <option key={c.id_categoria} value={c.id_categoria}>{c.nombre_categoria}</option>
            ))}
          </select>
        </div>
        {error && <p className="error-formulario">{error}</p>}
        <button className="boton-principal" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Creando...' : 'Crear límite'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalCrearLimite;
