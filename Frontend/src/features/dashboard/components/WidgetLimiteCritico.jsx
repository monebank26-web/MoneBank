import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../../core/constants';
import './WidgetLimiteCritico.css';

const aNumero = (v) => Number(v) || 0;

const claseUsoLimite = (p) =>
  p >= 100 ? 'uso-limite--superado' : p >= 70 ? 'uso-limite--alerta' : 'uso-limite--ok';

const WidgetLimiteCritico = ({ limiteCritico }) => {
  const porcentaje = limiteCritico ? Math.round(aNumero(limiteCritico.porcentaje_usado)) : 0;

  return (
    <div className="tarjeta-saldo tarjeta-saldo--limites">
      {limiteCritico ? (
        <>
          <p className="etiqueta-saldo">Límite más crítico</p>
          <h2 className={`valor-saldo ${porcentaje >= 100 ? 'valor-saldo--peligro' : ''}`}>
            {porcentaje}%
          </h2>
          <p className="subtexto-saldo">{limiteCritico.nombre}</p>
          <div className="barra-limite-tarjeta">
            <div
              className={`relleno-limite-tarjeta ${claseUsoLimite(porcentaje)}`}
              style={{ width: `${Math.min(Math.max(porcentaje, 4), 100)}%` }}
            />
          </div>
        </>
      ) : (
        <>
          <p className="etiqueta-saldo">Control de gastos</p>
          <h2 className="valor-saldo valor-saldo--vacio">Sin límites</h2>
          <p className="subtexto-saldo">Define cuánto puedes gastar por categoría</p>
        </>
      )}
      <div className="acciones-saldo">
        <Link to={ROUTES.LIMITES} className="boton-saldo">Ver límites →</Link>
      </div>
    </div>
  );
};

export default WidgetLimiteCritico;
