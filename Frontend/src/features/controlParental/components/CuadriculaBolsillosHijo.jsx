import React from 'react';
import { formatMoney } from '../../../core/utils/format';

const CuadriculaBolsillosHijo = ({ nombreHijo, bolsillos }) => {
  if (bolsillos.length === 0) return null;

  return (
    <div className="seccion-parental">
      <h3 className="titulo-seccion-parental">Bolsillos de {nombreHijo}</h3>
      <div className="cuadricula-bolsillos-parental">
        {bolsillos.map((bolsillo) => (
          <div key={bolsillo.id} className="bolsillo-parental" style={{ '--color-bolsillo': bolsillo.color }}>
            <div className="punto-bolsillo-parental" />
            <div>
              <p className="nombre-bolsillo-parental">{bolsillo.nombre}</p>
              <p className="saldo-bolsillo-parental">{formatMoney(bolsillo.saldo)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CuadriculaBolsillosHijo;
