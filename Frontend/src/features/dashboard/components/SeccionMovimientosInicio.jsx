import React from 'react';
import { Link } from 'react-router-dom';
import { Icon } from '@iconify/react';
import { formatMoney } from '../../../core/utils/format';
import { ROUTES } from '../../../core/constants';
import './SeccionMovimientosInicio.css';

const ICONOS = {
  GASTO: 'mdi:cart-outline',
  INGRESO: 'mdi:arrow-bottom-left',
  MOVIMIENTO_AHORRO: 'mdi:piggy-bank-outline',
};

const COLORES = {
  GASTO: 'gasto',
  INGRESO: 'ingreso',
  MOVIMIENTO_AHORRO: 'ahorro',
};

const SeccionMovimientosInicio = ({ transacciones }) => {
  return (
    <section className="movimientos-inicio seccion-inicio">
      <div className="movimientos-inicio__encabezado">
        <div className="movimientos-inicio__marca">
          <span className="movimientos-inicio__icono">
            <Icon icon="mdi:receipt-text-outline" />
          </span>
          <h3>Últimos movimientos</h3>
        </div>
        <Link to={ROUTES.TRANSACCIONES} className="movimientos-inicio__enlace">
          Ver todos
          <Icon icon="mdi:arrow-right" />
        </Link>
      </div>

      {transacciones.length === 0 ? (
        <p className="movimientos-inicio__vacio">Sin movimientos aún.</p>
      ) : (
        <div className="movimientos-inicio__lista">
          {transacciones.map((movimiento) => {
            const tipo = movimiento.tipo_transaccion;
            const color = COLORES[tipo] || 'ahorro';
            const signo = tipo === 'INGRESO' ? '+' : tipo === 'GASTO' ? '-' : '';

            return (
              <div key={movimiento.id_transaccion} className="fila-movimiento">
                <span className={`fila-movimiento__icono fila-movimiento__icono--${color}`}>
                  <Icon icon={ICONOS[tipo] || 'mdi:swap-horizontal'} />
                </span>

                <div className="fila-movimiento__info">
                  <p className="fila-movimiento__nombre">
                    {movimiento.descripcion || movimiento.nombre_categoria}
                  </p>
                  <div className="fila-movimiento__detalle">
                    <span className={`fila-movimiento__chip fila-movimiento__chip--${color}`}>
                      {movimiento.nombre_categoria}
                    </span>
                    <span className="fila-movimiento__fecha">
                      {new Date(movimiento.fecha).toLocaleDateString('es-CO', {
                        day: '2-digit',
                        month: 'short',
                      })}
                    </span>
                  </div>
                </div>

                <div className="fila-movimiento__monto">
                  <p className={`fila-movimiento__valor fila-movimiento__valor--${color}`}>
                    {signo}
                    {formatMoney(Math.abs(Number(movimiento.monto) || 0))}
                  </p>
                  <p className="fila-movimiento__moneda">COP</p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
};

export default SeccionMovimientosInicio;