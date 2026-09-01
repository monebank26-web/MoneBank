import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';
import { metasService } from '../services/metasService';

const ModalCrearMeta = ({ open, onClose, onCrear }) => {
  const [form, setForm] = useState({
    nombre: '',
    monto_objetivo: '',
    saldo_inicial: '',
    fecha_objetivo: '',
    id_categoria: '',
  });
  const [categorias, setCategorias] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open) return;
    metasService.listarCategoriasAhorro()
      .then(setCategorias)
      .catch((err) => setError(`No se pudieron cargar las categorías: ${err.message}`));
  }, [open]);

  const handleSubmit = async () => {
    if (!form.nombre.trim()) { setError('El nombre de la meta es obligatorio.'); return; }
    if (form.nombre.trim().length > 100) { setError('El nombre no puede superar 100 caracteres.'); return; }
    const objetivo = parseFloat(form.monto_objetivo);
    if (!objetivo || objetivo <= 0) { setError('El monto objetivo debe ser mayor a 0.'); return; }
    if (form.saldo_inicial !== '' && parseFloat(form.saldo_inicial) < 0) {
      setError('El saldo inicial no puede ser negativo.');
      return;
    }
    if (!form.fecha_objetivo) { setError('La fecha objetivo es obligatoria.'); return; }
    const hoy = new Date().toISOString().slice(0, 10);
    if (form.fecha_objetivo < hoy) { setError('La fecha objetivo debe ser posterior a hoy.'); return; }
    if (!form.id_categoria) { setError('Selecciona una categoría.'); return; }

    setLoading(true);
    setError('');
    try {
      await onCrear({
        nombre: form.nombre.trim(),
        monto_objetivo: objetivo,
        saldo_inicial: form.saldo_inicial === '' ? undefined : parseFloat(form.saldo_inicial),
        fecha_objetivo: form.fecha_objetivo,
        id_categoria: parseInt(form.id_categoria, 10),
      });
      setForm({ nombre: '', monto_objetivo: '', saldo_inicial: '', fecha_objetivo: '', id_categoria: '' });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Nueva meta de ahorro">
      <div className="formulario-modal">
        <div className="grupo-campo">
          <label className="etiqueta-campo">Nombre de la meta</label>
          <input
            className="campo-entrada"
            placeholder="Ej: Bicicleta nueva, Viaje..."
            maxLength={100}
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto objetivo (COP)</label>
          <input
            className="campo-entrada"
            type="number"
            placeholder="Ej: 500000"
            min="1"
            step="1000"
            value={form.monto_objetivo}
            onChange={(e) => setForm({ ...form, monto_objetivo: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Saldo inicial (opcional)</label>
          <input
            className="campo-entrada"
            type="number"
            placeholder="0"
            min="0"
            step="1000"
            value={form.saldo_inicial}
            onChange={(e) => setForm({ ...form, saldo_inicial: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Fecha objetivo</label>
          <input
            className="campo-entrada"
            type="date"
            value={form.fecha_objetivo}
            onChange={(e) => setForm({ ...form, fecha_objetivo: e.target.value })}
          />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Categoría</label>
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
          {loading ? 'Creando...' : 'Crear meta'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalCrearMeta;
