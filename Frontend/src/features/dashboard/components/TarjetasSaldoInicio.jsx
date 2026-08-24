import React from 'react';
import { Link } from 'react-router-dom';
import { formatMoney } from '../../../core/utils/format';
import { ROUTES } from '../../../core/constants';

const TarjetasSaldoInicio = ({ saldoCuenta, totalBolsillos, cantidadBolsillos, onConsignar }) => {
  return (
    <div className="tarjeta-saldos-row">
      <div className="tarjeta-saldo tarjeta-saldo--cuenta-principal">
        <p className="etiqueta-saldo">Mi Cuenta</p>
        <h2 className="valor-saldo">{formatMoney(saldoCuenta)}</h2>
        <p className="subtexto-saldo">Saldo disponible para bolsillos</p>
        <div className="acciones-saldo">
          <button className="boton-saldo" onClick={onConsignar}>
            + Consignar
          </button>
        </div>
      </div>

      <div className="tarjeta-saldo tarjeta-saldo--bolsillos">
        <p className="etiqueta-saldo">En bolsillos</p>
        <h2 className="valor-saldo">{formatMoney(totalBolsillos)}</h2>
        <p className="subtexto-saldo">{cantidadBolsillos} bolsillo{cantidadBolsillos !== 1 ? 's' : ''} activo{cantidadBolsillos !== 1 ? 's' : ''}</p>
        <div className="acciones-saldo">
          <Link to={ROUTES.BOLSILLOS} className="boton-saldo">Ver bolsillos →</Link>
        </div>
      </div>
    </div>
  );
};

export default TarjetasSaldoInicio;
