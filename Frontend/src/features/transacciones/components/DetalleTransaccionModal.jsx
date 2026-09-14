import React, { useEffect, useState } from 'react';
import Modal from '../../../shared/components/Modal';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';
import { transaccionesService } from '../services/transaccionesService';
import './DetalleTransaccionModal.css';

const TIPOS_EDITABLES = ['GASTO', 'INGRESO'];

const DetalleTransaccionModal = ({ open, transaccionId, onClose, categorias = [], onActualizado }) => {
  const [detalle, setDetalle] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');
  const [modoEdicion, setModoEdicion] = useState(false);
  const [guardando, setGuardando] = useState(false);
  const [errorFormulario, setErrorFormulario] = useState('');
  const [form, setForm] = useState({ monto: '', id_categoria: '', descripcion: '' });

  useEffect(() => {
    if (!open || !transaccionId) return;
    setCargando(true);
    setError('');
    setDetalle(null);
    setModoEdicion(false);
    setErrorFormulario('');
    transaccionesService.obtenerDetalle(transaccionId)
      .then(setDetalle)
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }, [open, transaccionId]);

  const tipo = detalle?.tipo_transaccion;
  const esEditable = TIPOS_EDITABLES.includes(tipo);

  const handleEditar = () => {
    setForm({
      monto: detalle.monto != null ? String(detalle.monto) : '',
      id_categoria: detalle.id_categoria != null ? String(detalle.id_categoria) : '',
      descripcion: detalle.descripcion || '',
    });
    setErrorFormulario('');
    setModoEdicion(true);
  };

  const handleCancelar = () => {
    setModoEdicion(false);
    setErrorFormulario('');
  };

  const handleGuardar = async () => {
    const monto = parseFloat(form.monto);
    if (!monto || monto <= 0) {
      setErrorFormulario('Ingresa un monto válido.');
      return;
    }
    if (!form.id_categoria) {
      setErrorFormulario('Selecciona una categoría.');
      return;
    }
    setGuardando(true);
    setErrorFormulario('');
    try {
      await transaccionesService.actualizarTransaccion(transaccionId, {
        monto,
        descripcion: form.descripcion.trim() || null,
        id_categoria: parseInt(form.id_categoria, 10),
      });
      setModoEdicion(false);
      onActualizado?.();
      onClose();
    } catch (e) {
      setErrorFormulario(e.message);
    } finally {
      setGuardando(false);
    }
  };

  const categoriasDelTipo = categorias.filter((c) => c.tipo_categoria === tipo);

  return (
    <Modal open={open} onClose={onClose} title="Detalle de transacción">
      {cargando && <p className="detalle-mensaje">Cargando...</p>}
      {error && <p className="detalle-mensaje detalle-mensaje--error">{error}</p>}
      {detalle && (
        <div className="detalle-transaccion">
          {/* Tipo + monto grande */}
          <div className={`detalle-transaccion__hero detalle-transaccion__hero--${tipo?.toLowerCase()}`}>
            <span className="detalle-transaccion__hero-icono">
              {tipo === 'GASTO' ? '↓' : tipo === 'INGRESO' ? '↑' : '→'}
            </span>
            <p className="detalle-transaccion__hero-tipo">
              {tipo === 'GASTO' ? 'Gasto' : tipo === 'INGRESO' ? 'Ingreso' : 'Movimiento a meta'}
            </p>
            <p className="detalle-transaccion__hero-monto">{formatMoney(detalle.monto)}</p>
          </div>

          {modoEdicion ? (
            <div className="detalle-transaccion__formulario">
              <label className="detalle-transaccion__campo">
                <span className="detalle-transaccion__campo-label">Monto</span>
                <input
                  className="detalle-transaccion__input"
                  type="number"
                  min="0"
                  step="0.01"
                  value={form.monto}
                  onChange={(e) => setForm({ ...form, monto: e.target.value })}
                  disabled={guardando}
                />
              </label>

              <label className="detalle-transaccion__campo">
                <span className="detalle-transaccion__campo-label">Categoría</span>
                <select
                  className="detalle-transaccion__input"
                  value={form.id_categoria}
                  onChange={(e) => setForm({ ...form, id_categoria: e.target.value })}
                  disabled={guardando}
                >
                  <option value="">Selecciona una categoría</option>
                  {categoriasDelTipo.map((c) => (
                    <option key={c.id_categoria} value={c.id_categoria}>
                      {c.nombre_categoria}
                    </option>
                  ))}
                </select>
              </label>

              <label className="detalle-transaccion__campo">
                <span className="detalle-transaccion__campo-label">Descripción</span>
                <input
                  className="detalle-transaccion__input"
                  type="text"
                  maxLength={255}
                  value={form.descripcion}
                  onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
                  disabled={guardando}
                />
              </label>

              {errorFormulario && (
                <p className="detalle-mensaje detalle-mensaje--error">{errorFormulario}</p>
              )}

              <div className="detalle-transaccion__acciones">
                <button
                  type="button"
                  className="detalle-transaccion__boton detalle-transaccion__boton--secundario"
                  onClick={handleCancelar}
                  disabled={guardando}
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  className="detalle-transaccion__boton detalle-transaccion__boton--primario"
                  onClick={handleGuardar}
                  disabled={guardando}
                >
                  {guardando ? 'Guardando...' : 'Guardar cambios'}
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Filas de detalle */}
              <div className="detalle-transaccion__filas">
                <div className="detalle-transaccion__fila">
                  <span className="detalle-transaccion__fila-label">Fecha</span>
                  <span className="detalle-transaccion__fila-valor">{formatFechaConHora(detalle.fecha)}</span>
                </div>
                <div className="detalle-transaccion__fila">
                  <span className="detalle-transaccion__fila-label">Estado</span>
                  <span className="detalle-transaccion__fila-valor">{detalle.estado_transaccion}</span>
                </div>
                <div className="detalle-transaccion__fila">
                  <span className="detalle-transaccion__fila-label">Categoría</span>
                  <span className="detalle-transaccion__fila-valor">{detalle.nombre_categoria}</span>
                </div>
                {detalle.descripcion && (
                  <div className="detalle-transaccion__fila">
                    <span className="detalle-transaccion__fila-label">Descripción</span>
                    <span className="detalle-transaccion__fila-valor">{detalle.descripcion}</span>
                  </div>
                )}
                {detalle.nombre_ahorro && (
                  <div className="detalle-transaccion__fila">
                    <span className="detalle-transaccion__fila-label">Meta asociada</span>
                    <span className="detalle-transaccion__fila-valor">{detalle.nombre_ahorro}</span>
                  </div>
                )}
              </div>

              {esEditable && (
                <div className="detalle-transaccion__acciones">
                  <button
                    type="button"
                    className="detalle-transaccion__boton detalle-transaccion__boton--primario"
                    onClick={handleEditar}
                  >
                    Editar
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </Modal>
  );
};

export default DetalleTransaccionModal;
