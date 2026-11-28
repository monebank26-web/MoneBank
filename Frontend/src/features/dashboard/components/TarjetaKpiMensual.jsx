import React from 'react';
import { Icon } from '@iconify/react';
import { formatMoney } from '../../../core/utils/format';
import './TarjetaKpiMensual.css';

const TarjetaKpiMensual = ({ etiqueta, valor, variacion, tipo }) => {
  const esIngreso = tipo === 'ingreso';
  const hayVariacion = variacion !== null && variacion !== undefined;
  const esBuena = esIngreso ? variacion >= 0 : variacion <= 0;

  return (
    <div className="tarjeta-kpi">
      <div className="tarjeta-kpi__superior">
        <span className={`tarjeta-kpi__icono tarjeta-kpi__icono--${tipo}`}>
          <Icon icon={esIngreso ? 'mdi:arrow-down' : 'mdi:arrow-up'} />
        </span>

        {hayVariacion && (
          <span className={`tarjeta-kpi__variacion ${esBuena ? 'tarjeta-kpi__variacion--buena' : 'tarjeta-kpi__variacion--mala'}`}>
            {variacion > 0 ? '+' : ''}
            {variacion.toFixed(1)}%
          </span>
        )}
      </div>

      <p className="tarjeta-kpi__etiqueta">{etiqueta}</p>
      <p className="tarjeta-kpi__valor">{formatMoney(valor)}</p>
    </div>
  );
};

export default TarjetaKpiMensual;