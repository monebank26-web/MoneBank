import React from 'react';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';

const ListaMovimientosBolsillo = ({ movimientos }) => {
  return (
    <div className="seccion-detalle-bolsillo">
      <h3 className="titulo-seccion-detalle">Movimientos de este bolsillo</h3>
      {movimientos.length === 0 ? (
        <p className="sin-movimientos-parental">Aún no hay movimientos en este bolsillo.</p>
      ) : (
        <div className="lista-movimientos-completa">
          {movimientos.map((movimiento) => (
            <div key={movimiento.id} className="elemento-movimiento-completo">
              <div className={`icono-elemento-movimiento icono-movimiento--${movimiento.tipo}`}>
                {movimiento.tipo === 'transferencia' ? '↔' : '↓'}
              </div>
              <div className="informacion-elemento-movimiento">
                <p className="descripcion-elemento-movimiento">
                  {movimiento.tipo === 'transferencia'
                    ? `Transferencia: ${movimiento.origenNombre} → ${movimiento.destinoNombre}`
                    : `Depósito en ${movimiento.destinoNombre}`}
                </p>
                {movimiento.descripcion && <p className="nota-elemento-movimiento">"{movimiento.descripcion}"</p>}
                <p className="fecha-movimiento">{formatFechaConHora(movimiento.fecha)}</p>
              </div>
              <div className="columna-derecha-movimiento">
                <p className={`monto-movimiento monto-movimiento--${movimiento.tipo}`}>
                  {movimiento.tipo === 'deposito' ? '+' : ''}{formatMoney(movimiento.monto)}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ListaMovimientosBolsillo;
