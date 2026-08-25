import React from 'react';
import { Link } from 'react-router-dom';
import { formatMoney } from '../../../core/utils/format';
import { ROUTES } from '../../../core/constants';

const SeccionMovimientosInicio = ({ transacciones }) => {
  return (
    <section className="seccion-inicio">
      <div className="encabezado-seccion-inicio">
        <h3>Últimos movimientos</h3>
        <Link to={ROUTES.TRANSACCIONES} className="enlace-ver-todos">Ver todos</Link>
      </div>

      {transacciones.length === 0 ? (
        <p className="seccion-vacia-inicio-text">Sin movimientos aún.</p>
      ) : (
        <div className="lista-movimientos">
          {transacciones.map((movimiento) => (
            <div key={movimiento.id} className="elemento-movimiento">
              <div className={`icono-movimiento icono-movimiento--${movimiento.tipo}`}>
                {movimiento.tipo === 'transferencia' ? '↔' : '↓'}
              </div>
              <div className="informacion-movimiento">
                <p className="descripcion-movimiento">
                  {movimiento.tipo === 'transferencia'
                    ? `${movimiento.origenNombre} → ${movimiento.destinoNombre}`
                    : `Depósito en ${movimiento.destinoNombre}`}
                </p>
                <p className="fecha-movimiento">{new Date(movimiento.fecha).toLocaleDateString('es-CO')}</p>
              </div>
              <p className={`monto-movimiento monto-movimiento--${movimiento.tipo}`}>
                {movimiento.tipo === 'deposito' ? '+' : ''}{formatMoney(movimiento.monto)}
              </p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default SeccionMovimientosInicio;
