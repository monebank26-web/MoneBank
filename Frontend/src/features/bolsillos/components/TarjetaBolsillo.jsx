import React from 'react';
import { Link } from 'react-router-dom';
import { formatMoney } from '../../../core/utils/format';
import MenuOpcionesBolsillo from './MenuOpcionesBolsillo';

const TarjetaBolsillo = ({ bolsillo, onDepositar, onTransferir, onEditar, onEliminar }) => {
  return (
    <div className="tarjeta-bolsillo" style={{ '--color': bolsillo.color }}>
      <div className="parte-superior-tarjeta-bolsillo">
        <div className="indicador-color-bolsillo" />
        <Link to={`/bolsillos/${bolsillo.id}`} className="informacion-tarjeta-bolsillo">
          <h3 className="nombre-tarjeta-bolsillo">{bolsillo.nombre}</h3>
          {bolsillo.descripcion && <p className="descripcion-tarjeta-bolsillo">{bolsillo.descripcion}</p>}
        </Link>
        <MenuOpcionesBolsillo
          onDepositar={() => onDepositar(bolsillo)}
          onTransferir={() => onTransferir(bolsillo)}
          onEditar={() => onEditar(bolsillo)}
          onEliminar={() => onEliminar(bolsillo)}
        />
      </div>
      <Link to={`/bolsillos/${bolsillo.id}`} className="saldo-tarjeta-bolsillo saldo-tarjeta-bolsillo--enlace">
        {formatMoney(bolsillo.saldo)}
      </Link>
    </div>
  );
};

export default TarjetaBolsillo;
