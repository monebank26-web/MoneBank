import React from 'react';
import Modal from '../../../shared/components/Modal';
import { formatFecha, formatMoney } from '../../../core/utils/format';
import './ModalConsultarProgramacion.css';

const ETIQUETAS_ESTADO = {
  ACTIVA: 'Activa',
  PAUSADA: 'Pausada',
  FINALIZADA: 'Finalizada',
};

const FRECUENCIA_ETIQUETAS = {
  DIARIA: 'Diaria',
  SEMANAL: 'Semanal',
  QUINCENAL: 'Quincenal',
  MENSUAL: 'Mensual',
  TRIMESTRAL: 'Trimestral',
  SEMESTRAL: 'Semestral',
  ANUAL: 'Anual',
};

const ModalConsultarProgramacion = ({ open, onClose, programacion, onModificar }) => {
  if (!programacion) return null;

  const estado = programacion.estado;
  const estadoClase = (estado || '').toLowerCase();

  return (
    <Modal open={open} onClose={onClose} title="Programación de aportes">
      <div className="detalle-programacion">
        <div className={`detalle-programacion__hero detalle-programacion__hero--${estadoClase}`}>
          <span className="detalle-programacion__hero-icono">↻</span>
          <p className="detalle-programacion__hero-tipo">Aporte programado</p>
          <p className="detalle-programacion__hero-monto">{formatMoney(programacion.monto_periodico)}</p>
          <span className={`estado-programacion estado-programacion--${estadoClase}`}>
            {ETIQUETAS_ESTADO[estado] || estado}
          </span>
        </div>

        <div className="detalle-programacion__filas">
          <div className="detalle-programacion__fila">
            <span className="detalle-programacion__fila-label">Meta</span>
            <span className="detalle-programacion__fila-valor">{programacion.nombre_ahorro}</span>
          </div>
          <div className="detalle-programacion__fila">
            <span className="detalle-programacion__fila-label">Frecuencia</span>
            <span className="detalle-programacion__fila-valor">
              {FRECUENCIA_ETIQUETAS[programacion.frecuencia] || programacion.frecuencia}
            </span>
          </div>
          <div className="detalle-programacion__fila">
            <span className="detalle-programacion__fila-label">Inicio de vigencia</span>
            <span className="detalle-programacion__fila-valor">{formatFecha(programacion.fecha_inicio)}</span>
          </div>
          <div className="detalle-programacion__fila">
            <span className="detalle-programacion__fila-label">Fin de vigencia</span>
            <span className="detalle-programacion__fila-valor">{formatFecha(programacion.fecha_fin)}</span>
          </div>
          <div className="detalle-programacion__fila">
            <span className="detalle-programacion__fila-label">Próximo cobro</span>
            <span className="detalle-programacion__fila-valor">{formatFecha(programacion.fecha_cobro)}</span>
          </div>
          <div className="detalle-programacion__fila">
            <span className="detalle-programacion__fila-label">Tiempo restante</span>
            <span className="detalle-programacion__fila-valor">{programacion.tiempo_restante || '—'}</span>
          </div>
        </div>

        <div className="detalle-programacion__acciones">
          <button
            type="button"
            className="detalle-programacion__boton detalle-programacion__boton--modificar"
            onClick={() => onModificar(programacion)}
          >
            Modificar programación
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default ModalConsultarProgramacion;