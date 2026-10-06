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

const ModalModificarProgramacion = ({ open, onClose, programacion, onChangeEstado }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (open) {
      setLoading(false);
      setError('');
    }
  }, [open]);

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

  return (
    <Modal open={open} onClose={onClose} title="Modificar programación">
      <div className="formulario-modal">
        <div className="etiqueta-saldo-disponible">
          Meta: <strong>{programacion.nombre_ahorro}</strong> · Aporte de{' '}
          {formatMoney(programacion.monto_periodico)}
        </div>

        {finalizada ? (
          <p className="mensaje-programacion-finalizada">
            Esta programación ya está finalizada. No es posible modificar su estado.
          </p>
        ) : (
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
        )}

        {error && <p className="error-formulario">{error}</p>}
      </div>
    </Modal>
  );
};

export default ModalModificarProgramacion;