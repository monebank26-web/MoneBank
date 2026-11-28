import React, { useState, useEffect } from 'react';
import Modal from '../../../shared/components/Modal';
import '../../../shared/styles/transacciones-modal.css';
import { formatMoney } from '../../../core/utils/format';
import './ModalModificarProgramacion.css';

const ETIQUETAS_ESTADO = {
  ACTIVA: 'Activa',
  PAUSADA: 'Pausada',
  FINALIZADA: 'Finalizada',
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

const ModalModificarProgramacion = ({
  open,
  onClose,
  programacion,
  onChangeEstado,
  onModificarProgramacion,
}) => {
  const [montoPeriodico, setMontoPeriodico] = useState('');
  const [frecuencia, setFrecuencia] = useState('MENSUAL');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (open && programacion) {
      setMontoPeriodico(String(Number(programacion.monto_periodico) || ''));
      setFrecuencia(programacion.frecuencia || 'MENSUAL');
      setLoading(false);
      setError('');
    }
  }, [open, programacion]);

  if (!programacion) return null;

  const finalizada = programacion.estado === 'FINALIZADA';

  const resolverAccion = async (nuevoEstado) => {
    setLoading(true);
    setError('');
    try {
      await onChangeEstado({ id_programacion_ahorro: programacion.id_programacion_ahorro, estado: nuevoEstado });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const guardarPeriodicidad = async () => {
    const monto = Number(montoPeriodico);
    if (!monto || monto <= 0) {
      setError('Ingresa un monto válido mayor a 0.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await onModificarProgramacion({
        id_programacion_ahorro: programacion.id_programacion_ahorro,
        monto_periodico: monto,
        frecuencia,
      });
      onClose();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose} title="Modificar programación">
      <div className="formulario-modal">
        <div className="etiqueta-saldo-disponible">
          Meta: <strong>{programacion.nombre_ahorro}</strong> · Aporte de{' '}
          {formatMoney(programacion.monto_periodico)}
        </div>

        {finalizada ? (
          <p className="mensaje-programacion-finalizada">
            Esta programación ya está finalizada. No es posible modificarla.
          </p>
        ) : (
          <>
            <div className="grupo-campo">
              <label className="etiqueta-campo">Monto por periodo (COP)</label>
              <input
                className="campo-entrada"
                type="number"
                placeholder="Ej: 50000"
                min="1"
                step="1000"
                value={montoPeriodico}
                onChange={(e) => setMontoPeriodico(e.target.value)}
              />
            </div>
            <div className="grupo-campo">
              <label className="etiqueta-campo">Frecuencia</label>
              <select
                className="campo-entrada"
                value={frecuencia}
                onChange={(e) => setFrecuencia(e.target.value)}
              >
                {FRECUENCIAS.map((opcion) => (
                  <option key={opcion.valor} value={opcion.valor}>
                    {opcion.etiqueta}
                  </option>
                ))}
              </select>
            </div>
            <button
              className="boton-principal"
              type="button"
              onClick={guardarPeriodicidad}
              disabled={loading}
            >
              {loading ? 'Guardando...' : 'Guardar cambios'}
            </button>

            <hr className="separador-programacion" />

            <div className="grupo-estado-programacion">
              <p className="estado-actual-programacion">
                Estado actual:{' '}
                <strong>{ETIQUETAS_ESTADO[programacion.estado] || programacion.estado}</strong>
              </p>
              <div className="acciones-estado-programacion">
                {programacion.estado === 'PAUSADA' ? (
                  <button
                    type="button"
                    className="boton-estado-programacion boton-estado-programacion--activar"
                    onClick={() => resolverAccion('ACTIVA')}
                    disabled={loading}
                  >
                    {loading ? 'Guardando...' : 'Activar'}
                  </button>
                ) : (
                  <button
                    type="button"
                    className="boton-estado-programacion boton-estado-programacion--pausar"
                    onClick={() => resolverAccion('PAUSADA')}
                    disabled={loading}
                  >
                    {loading ? 'Guardando...' : 'Pausar'}
                  </button>
                )}
                <button
                  type="button"
                  className="boton-estado-programacion boton-estado-programacion--finalizar"
                  onClick={() => resolverAccion('FINALIZADA')}
                  disabled={loading}
                >
                  Finalizar
                </button>
              </div>
              <p className="ayuda-programacion-finalizar">
                Finalizar detiene la programación y no se puede deshacer.
              </p>
            </div>
          </>
        )}

        {error && <p className="error-formulario">{error}</p>}
      </div>
    </Modal>
  );
};

export default ModalModificarProgramacion;
