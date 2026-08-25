import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../../core/constants';

const aNumero = (v) => Number(v) || 0;

const claseUsoLimite = (p) =>
  p >= 100 ? 'uso-limite--superado' : p >= 70 ? 'uso-limite--alerta' : 'uso-limite--ok';

const SeccionAhorros = ({ limites, metas, limitesCriticos, metasOrdenadas }) => {
  return (
    <aside className="columna-ahorros-inicio">
      <section className="seccion-inicio tarjeta-acceso-ahorros">
        <div className="encabezado-seccion-inicio">
          <h3>Mis límites</h3>
          <Link to={ROUTES.LIMITES} className="enlace-ver-todos">Ver todos</Link>
        </div>

        {limites.length === 0 ? (
          <p className="acceso-ahorros-vacio-texto">
            Aún no tienes límites de gasto. Empieza a controlar tus gastos.
          </p>
        ) : (
          <div className="lista-mini-limites">
            {limitesCriticos.slice(0, 3).map((l) => {
              const pct = Math.round(aNumero(l.porcentaje_usado));
              return (
                <Link
                  key={l.id_ahorro}
                  to={ROUTES.LIMITES}
                  className="fila-mini-limite fila-mini-enlace"
                >
                  <div className="info-mini-limite">
                    <p className={`nombre-mini-limite ${pct >= 100 ? 'nombre-mini-limite--superado' : ''}`}>
                      {l.nombre}
                    </p>
                    <div className="mini-barra-limite">
                      <div
                        className={`mini-relleno-limite ${claseUsoLimite(pct)}`}
                        style={{ width: `${Math.min(Math.max(pct, 4), 100)}%` }}
                      />
                    </div>
                  </div>
                  <span className={`porcentaje-mini-limite ${claseUsoLimite(pct)}`}>{pct}%</span>
                </Link>
              );
            })}
          </div>
        )}

        <Link to={ROUTES.LIMITES} className="boton-llamada-accion boton-llamada-accion--bloque">
          Iniciar límite
        </Link>
      </section>

      <section className="seccion-inicio tarjeta-acceso-ahorros">
        <div className="encabezado-seccion-inicio">
          <h3>Mis metas</h3>
          <Link to={ROUTES.METAS} className="enlace-ver-todos">Ver todas</Link>
        </div>

        {metas.length === 0 ? (
          <p className="acceso-ahorros-vacio-texto">
            Aún no tienes metas de ahorro. Proponte una y empieza a cumplirlo.
          </p>
        ) : (
          <div className="lista-mini-metas">
            {metasOrdenadas.slice(0, 3).map((m) => {
              const pct = Math.min(Math.round(aNumero(m.porcentaje_completado)), 100);
              return (
                <Link
                  key={m.id_ahorro}
                  to={ROUTES.METAS}
                  className="fila-mini-meta fila-mini-enlace"
                >
                  <div className="info-mini-meta">
                    <p className="nombre-mini-meta">{m.nombre}</p>
                    <div className="mini-barra-meta">
                      <div
                        className={`mini-relleno-meta ${pct >= 100 ? 'mini-relleno-meta--completo' : ''}`}
                        style={{ width: `${Math.max(pct, 4)}%` }}
                      />
                    </div>
                  </div>
                  <span className="porcentaje-mini-meta">{pct}%</span>
                </Link>
              );
            })}
          </div>
        )}

        <Link to={ROUTES.METAS} className="boton-llamada-accion boton-llamada-accion--bloque">
          Iniciar meta
        </Link>
      </section>
    </aside>
  );
};

export default SeccionAhorros;
