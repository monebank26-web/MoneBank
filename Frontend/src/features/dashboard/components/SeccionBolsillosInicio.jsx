import React from 'react';
import { Link } from 'react-router-dom';
import { formatMoney } from '../../../core/utils/format';
import { ROUTES } from '../../../core/constants';

const SeccionBolsillosInicio = ({ bolsillos, cargando }) => {
  return (
    <section className="seccion-inicio">
      <div className="encabezado-seccion-inicio">
        <h3>Mis bolsillos</h3>
        <Link to={ROUTES.BOLSILLOS} className="enlace-ver-todos">Ver todos</Link>
      </div>

      {cargando ? (
        <p className="cargando-inicio">Cargando...</p>
      ) : bolsillos.length === 0 ? (
        <div className="seccion-vacia-inicio">
          <p>Todavía no tienes bolsillos.</p>
          <Link to={ROUTES.BOLSILLOS} className="boton-llamada-accion">Crear mi primer bolsillo</Link>
        </div>
      ) : (
        <div className="cuadricula-bolsillos">
          {bolsillos.slice(0, 4).map((bolsillo) => (
            <div key={bolsillo.id} className="bolsillo-miniatura" style={{ '--color': bolsillo.color }}>
              <div className="punto-bolsillo-miniaturaatura" />
              <div>
                <p className="nombre-bolsillo-miniaturaatura">{bolsillo.nombre}</p>
                <p className="saldo-bolsillo-miniaturaatura">{formatMoney(bolsillo.saldo)}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};

export default SeccionBolsillosInicio;
