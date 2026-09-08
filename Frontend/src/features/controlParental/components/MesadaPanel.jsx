import React, { useEffect, useState } from 'react';
import { mesadaService } from '../services/mesadaService';
import './MesadaPanel.css';

const MesadaPanel = ({ idHijo }) => {
  const [mesada, setMesada] = useState(null);
  const [monto, setMonto] = useState('');
  const [frecuencia, setFrecuencia] = useState('MENSUAL');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [editando, setEditando] = useState(false);
  const [error, setError] = useState('');
  const [mensaje, setMensaje] = useState('');

  useEffect(() => {
    let activo = true;
    mesadaService.obtener(idHijo)
      .then((data) => { if (activo) setMesada(data); })
      .catch((e) => { if (activo) setError(e.response?.data?.detail || e.message || 'No se pudo cargar la mesada.'); })
      .finally(() => { if (activo) setCargando(false); });
    return () => { activo = false; };
  }, [idHijo]);

  const guardar = async (event) => {
    event.preventDefault();
    setError('');
    setMensaje('');
    setGuardando(true);
    try {
      const data = await mesadaService.crear(idHijo, {
        monto: Number(monto), frecuencia, fecha_inicio: fechaInicio, fecha_fin: fechaFin || null,
      });
      setMesada(data);
      setMensaje('La mesada quedó configurada.');
      setMonto('');
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'No se pudo configurar la mesada.');
    } finally { setGuardando(false); }
  };

  const ejecutar = async () => {
    setError(''); setMensaje(''); setGuardando(true);
    try {
      const resultado = await mesadaService.ejecutar(idHijo);
      setMensaje(`Mesada ejecutada. Próxima ejecución: ${resultado.proxima_ejecucion}`);
      setMesada({ ...mesada, proxima_ejecucion: resultado.proxima_ejecucion });
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'No se pudo ejecutar la mesada.');
    } finally { setGuardando(false); }
  };

  const iniciarEdicion = () => {
    setMonto(String(mesada.monto));
    setFrecuencia(mesada.frecuencia);
    setFechaInicio(mesada.fecha_inicio);
    setFechaFin(mesada.fecha_fin || '');
    setEditando(true);
  };

  const actualizar = async (event) => {
    event.preventDefault();
    setError(''); setMensaje(''); setGuardando(true);
    try {
      const data = await mesadaService.actualizar(idHijo, {
        monto: Number(monto), frecuencia, fecha_inicio: fechaInicio, fecha_fin: fechaFin || null,
      });
      setMesada(data);
      setEditando(false);
      setMensaje('La mesada fue actualizada.');
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'No se pudo actualizar la mesada.');
    } finally { setGuardando(false); }
  };

  const cancelar = async () => {
    if (!window.confirm('¿Deseas cancelar esta mesada? Se conservará el historial.')) return;
    setError(''); setMensaje(''); setGuardando(true);
    try {
      const data = await mesadaService.cancelar(idHijo);
      setMesada(data);
      setEditando(false);
      setMensaje('La mesada fue cancelada.');
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'No se pudo cancelar la mesada.');
    } finally { setGuardando(false); }
  };

  if (cargando) return <section className="mesada-panel"><p>Cargando mesada...</p></section>;

  const mostrarFormulario = !mesada || editando;

  return (
    <section className="mesada-panel">
      <div className="mesada-panel__title"><div><h3>Mesada</h3><p>Configura y ejecuta la mesada de forma controlada.</p></div></div>
      {error && <p className="mesada-panel__error">{error}</p>}
      {mensaje && <p className="mesada-panel__ok">{mensaje}</p>}
      {!mostrarFormulario ? (
        <div className="mesada-panel__current">
          <strong>${Number(mesada.monto).toLocaleString('es-CO')}</strong>
          <span>{mesada.frecuencia} · {mesada.estado}</span>
          <small>Inicia: {mesada.fecha_inicio}</small>
          {mesada.proxima_ejecucion && <small>Próxima ejecución: {mesada.proxima_ejecucion}</small>}
          <button className="mesada-panel__execute" type="button" onClick={ejecutar} disabled={guardando}>
            {guardando ? 'Ejecutando...' : 'Ejecutar mesada ahora'}
          </button>
          <div className="mesada-panel__actions">
            <button type="button" onClick={iniciarEdicion} disabled={guardando}>Editar mesada</button>
            <button type="button" onClick={cancelar} disabled={guardando}>Cancelar mesada</button>
          </div>
        </div>
      ) : (
        <form className="mesada-form" onSubmit={editando ? actualizar : guardar}>
          <label>Monto<input type="number" min="1" step="0.01" value={monto} onChange={(e) => setMonto(e.target.value)} required /></label>
          <label>Frecuencia<select value={frecuencia} onChange={(e) => setFrecuencia(e.target.value)}><option value="DIARIA">Diaria</option><option value="SEMANAL">Semanal</option><option value="QUINCENAL">Quincenal</option><option value="MENSUAL">Mensual</option></select></label>
          <label>Fecha de inicio<input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} required /></label>
          <label>Fecha final (opcional)<input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} /></label>
          <button type="submit" disabled={guardando}>{guardando ? 'Guardando...' : editando ? 'Guardar cambios' : 'Configurar mesada'}</button>
          {editando && <button type="button" onClick={() => setEditando(false)} disabled={guardando}>Cancelar edición</button>}
        </form>
      )}
    </section>
  );
};

export default MesadaPanel;
