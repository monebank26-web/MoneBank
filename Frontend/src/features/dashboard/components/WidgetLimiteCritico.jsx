import React from 'react';
import { Link } from 'react-router-dom';
import { Icon } from '@iconify/react';
import { ROUTES } from '../../../core/constants';
import './WidgetLimiteCritico.css';

const aNumero = (v) => Number(v) || 0;

const estadoLimite = (p) => (p >= 100 ? 'superado' : p >= 70 ? 'alerta' : 'ok');

const WidgetLimiteCritico = ({ limites = [], limiteCritico }) => {
  const porcentaje = limiteCritico ? Math.round(aNumero(limiteCritico.porcentaje_usado)) : 0;
  const estado = estadoLimite(porcentaje);

  return (
    <div className="gastos-card">
      <div className="gastos-card__cabecera">
        <span className="gastos-card__etiqueta">Control de gastos</span>
        <span className="gastos-card__icono">
          <Icon icon="mdi:speedometer" />
        </span>
      </div>

      {limiteCritico ? (
        <div className="gastos-card__cuerpo">
          <h2 className={`gastos-card__valor gastos-card__valor--${estado}`}>
            {porcentaje}%<span>usado</span>
          </h2>
          <p className="gastos-card__texto">
            Tu límite más crítico es <strong>{limiteCritico.nombre}</strong>
          </p>
          <div className="gastos-card__barra">
            <div
              className={`gastos-card__relleno gastos-card__relleno--${estado}`}
              style={{ width: `${Math.min(Math.max(porcentaje, 4), 100)}%` }}
            />
          </div>
          <p className="gastos-card__detalle">
            <Icon icon="mdi:tune-variant" />
            {limites.length} {limites.length === 1 ? 'límite en seguimiento' : 'límites en seguimiento'}
          </p>
        </div>
      ) : (
        <div className="gastos-card__cuerpo">
          <h2 className="gastos-card__valor gastos-card__valor--vacio">Sin límites</h2>
          <p className="gastos-card__texto">Define cuánto puedes gastar por categoría.</p>
        </div>
      )}

      <Link to={ROUTES.LIMITES} className="gastos-card__enlace">
        Ver límites
        <Icon icon="mdi:arrow-right" />
      </Link>
    </div>
  );
};

export default WidgetLimiteCritico;