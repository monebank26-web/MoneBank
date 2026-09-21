import React from 'react';
import { Icon } from '@iconify/react';
import { formatMoney, formatFechaCorta, formatHora } from '../../../core/utils/format';
import { iconoDeCategoria } from '../constants/iconosCategorias';
import './TransaccionCard.css';

const COLORES = {
  GASTO: 'gasto',
  INGRESO: 'ingreso',
  MOVIMIENTO_AHORRO: 'movimiento-a-meta',
};

const ETIQUETAS = {
  GASTO: 'Gasto',
  INGRESO: 'Ingreso',
  MOVIMIENTO_AHORRO: 'Mov. a meta',
};

const TransaccionCard = ({ transaccion, onDetalle }) => {
  const tipo = transaccion.tipo_transaccion;
  const color = COLORES[tipo] || 'gasto';

  return (
    <button className="transaccion-card" onClick={() => onDetalle?.(transaccion)}>
      <div className={`transaccion-card__icono transaccion-card__icono--${color}`}>
        <Icon icon={iconoDeCategoria(transaccion.nombre_categoria)} />
      </div>

      <p className="transaccion-card__descripcion" title={transaccion.descripcion || ''}>
        {transaccion.descripcion || 'Sin descripción'}
      </p>

      <p className={`transaccion-card__categoria transaccion-card__categoria--${color}`} title={transaccion.nombre_categoria}>
        {transaccion.nombre_categoria}
      </p>

      <div className="transaccion-card__fecha">
        <p className="transaccion-card__fecha-dia">{formatFechaCorta(transaccion.fecha)}</p>
        <p className="transaccion-card__fecha-hora">{formatHora(transaccion.fecha)}</p>
      </div>

      <div className="transaccion-card__monto-celda">
        <p className={`transaccion-card__monto transaccion-card__monto--${color}`}>
          {tipo === 'INGRESO' ? '+' : ''}{formatMoney(transaccion.monto)}
        </p>
        <span className={`transaccion-card__etiqueta transaccion-card__etiqueta--${color}`}>
          {ETIQUETAS[tipo] || 'Transacción'}
        </span>
      </div>
    </button>
  );
};

export default TransaccionCard;