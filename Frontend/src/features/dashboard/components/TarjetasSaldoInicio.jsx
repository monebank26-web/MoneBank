import React, { useState } from 'react';
import { Icon } from '@iconify/react';
import { formatMoney } from '../../../core/utils/format';
import './TarjetasSaldoInicio.css';

const TarjetasSaldoInicio = ({ saldoCuenta, onIngreso, onGasto }) => {
  const [oculto, setOculto] = useState(false);

  return (
    <div className="cuenta-card">
      <div className="cuenta-card__cabecera">
        <div className="cuenta-card__titulo">
          <span className="cuenta-card__etiqueta">Mi cuenta</span>
          <span className="cuenta-card__chip">Principal</span>
        </div>
        <button
          className="cuenta-card__ojo"
          onClick={() => setOculto(!oculto)}
          aria-label={oculto ? 'Mostrar saldo' : 'Ocultar saldo'}
        >
          <Icon icon={oculto ? 'mdi:eye-off-outline' : 'mdi:eye-outline'} />
        </button>
      </div>

      <div className="cuenta-card__saldo">
        <h2 className="cuenta-card__valor">
          {oculto ? '$ ••••••' : formatMoney(saldoCuenta)}
          <span>COP</span>
        </h2>
        <p className="cuenta-card__nota">
          <i />
          Saldo disponible para operaciones inmediatas
        </p>
      </div>

      <div className="cuenta-card__acciones">
        <button className="cuenta-card__boton cuenta-card__boton--ingreso" onClick={onIngreso}>
          <Icon icon="mdi:plus-circle-outline" />
          Ingreso
        </button>
        {onGasto && (
          <button className="cuenta-card__boton cuenta-card__boton--gasto" onClick={onGasto}>
            <Icon icon="mdi:minus-circle-outline" />
            Gasto
          </button>
        )}
      </div>
    </div>
  );
};

export default TarjetasSaldoInicio;