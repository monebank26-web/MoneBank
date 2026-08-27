import React from 'react';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';
import './TransaccionCard.css';

const ICONOS = {
  GASTO: '↓',
  INGRESO: '↑',
  MOVIMIENTO_AHORRO: '→',
};

const COLORES = {
  GASTO: 'gasto',
  INGRESO: 'ingreso',
  MOVIMIENTO_AHORRO: 'ahorro',
};

const TransaccionCard = ({ transaccion, onDetalle }) => {
  const tipo = transaccion.tipo_transaccion;

  return (
    <button className="transaccion-card" onClick={() => onDetalle?.(transaccion)}>
      <div className={`transaccion-card__icono transaccion-card__icono--${COLORES[tipo]}`}>
        {ICONOS[tipo] || '?'}
      </div>

      <div className="transaccion-card__info">
        <p className="transaccion-card__categoria">{transaccion.nombre_categoria}</p>
        {transaccion.descripcion && (
          <p className="transaccion-card__descripcion">{transaccion.descripcion}</p>
        )}
        <p className="transaccion-card__fecha">{formatFechaConHora(transaccion.fecha)}</p>
      </div>

      <div className="transaccion-card__derecha">
        <p className={`transaccion-card__monto transaccion-card__monto--${COLORES[tipo]}`}>
          {tipo === 'INGRESO' ? '+' : ''}{formatMoney(transaccion.monto)}
        </p>
        <span className={`transaccion-card__etiqueta transaccion-card__etiqueta--${COLORES[tipo]}`}>
          {tipo === 'GASTO' ? 'Gasto' : tipo === 'INGRESO' ? 'Ingreso' : 'Ahorro'}
        </span>
      </div>
    </button>
  );
};

export default TransaccionCard;