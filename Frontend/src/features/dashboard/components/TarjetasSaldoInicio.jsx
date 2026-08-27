import React from 'react';
import { formatMoney } from '../../../core/utils/format';

const TarjetasSaldoInicio = ({ saldoCuenta, onIngreso, onGasto }) => {
  return (
    <div className="tarjeta-saldo tarjeta-saldo--cuenta-principal">
      <p className="etiqueta-saldo">Mi Cuenta</p>
      <h2 className="valor-saldo">{formatMoney(saldoCuenta)}</h2>
      <p className="subtexto-saldo">Saldo disponible</p>
      <div className="acciones-saldo">
        <button className="boton-saldo" onClick={onIngreso}>
          + Ingreso
        </button>
        {onGasto && (
          <button className="boton-saldo" onClick={onGasto}>
            − Gasto
          </button>
        )}
      </div>
    </div>
  );
};

export default TarjetasSaldoInicio;
