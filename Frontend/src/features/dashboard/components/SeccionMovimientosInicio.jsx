import React from 'react';
import { Link } from 'react-router-dom';
import { formatMoney } from '../../../core/utils/format';
import { ROUTES } from '../../../core/constants';

const ICONOS = {
  GASTO: '↓',
  INGRESO: '↑',
  MOVIMIENTO_AHORRO: '→',
};

const COLORES = {
  GASTO: 'gasto',
  INGRESO: 'ingreso',
  MOVIMIENTO_AHORRO: 'ahorro',
};

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
          {transacciones.map((movimiento) => {
            const tipo = movimiento.tipo_transaccion;
            const color = COLORES[tipo] || 'ahorro';
            return (
              <div key={movimiento.id_transaccion} className="elemento-movimiento">
                <div className={`icono-movimiento icono-movimiento--${color}`}>
                  {ICONOS[tipo] || '?'}
                </div>
                <div className="informacion-movimiento">
                  <p className="descripcion-movimiento">
                    {movimiento.nombre_categoria}
                    {movimiento.descripcion && ` · ${movimiento.descripcion}`}
                  </p>
                  <p className="fecha-movimiento">{new Date(movimiento.fecha).toLocaleDateString('es-CO')}</p>
                </div>
                <p className={`monto-movimiento monto-movimiento--${color}`}>
                  {tipo === 'INGRESO' ? '+' : ''}{formatMoney(movimiento.monto)}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};

export default SeccionMovimientosInicio;
