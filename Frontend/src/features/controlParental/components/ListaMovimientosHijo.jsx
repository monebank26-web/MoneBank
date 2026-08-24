import React from 'react';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';

const ListaMovimientosHijo = ({ nombreHijo, movimientos }) => {
  return (
    <div className="seccion-parental">
      <h3 className="titulo-seccion-parental">Últimos movimientos de {nombreHijo}</h3>
      {movimientos.length === 0 ? (
        <p className="sin-movimientos-parental">Sin movimientos registrados aún.</p>
      ) : (
        <div className="lista-movimientos-parental">
          {movimientos.map((movimiento) => (
            <div key={movimiento.id} className="movimiento-parental">
              <div className={`icono-movimiento-parental icono-movimiento-parental--${movimiento.tipo}`}>
                {movimiento.tipo === 'transferencia' ? '↔' : '↓'}
              </div>
              <div className="info-movimiento-parental">
                <p className="descripcion-movimiento-parental">
                  {movimiento.tipo === 'transferencia'
                    ? `${movimiento.origenNombre} → ${movimiento.destinoNombre}`
                    : `Depósito en ${movimiento.destinoNombre}`}
                </p>
                <p className="fecha-movimiento-parental">{formatFechaConHora(movimiento.fecha)}</p>
              </div>
              <p className={`monto-movimiento-parental monto-movimiento-parental--${movimiento.tipo}`}>
                {movimiento.tipo === 'deposito' ? '+' : ''}{formatMoney(movimiento.monto)}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ListaMovimientosHijo;
