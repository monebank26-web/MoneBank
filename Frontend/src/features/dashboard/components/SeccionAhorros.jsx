import React from 'react';
import { Link } from 'react-router-dom';
import { Icon } from '@iconify/react';
import { ROUTES } from '../../../core/constants';
import './SeccionAhorros.css';

const aNumero = (v) => Number(v) || 0;

const estadoLimite = (p) => (p >= 100 ? 'superado' : p >= 70 ? 'alerta' : 'ok');

const SeccionAhorros = ({ limites, metas, limitesCriticos, metasOrdenadas }) => {
  return (
    <aside className="columna-ahorros-inicio">
      <section className="ahorro-card">
        <div className="ahorro-card__cabecera">
          <div>
            <h3>Mis límites</h3>
            <p>Presupuesto por categoría</p>
          </div>
          <Link to={ROUTES.LIMITES} className="ahorro-card__ver">
            Ver todos
          </Link>
        </div>

        <div className="ahorro-card__lista">
          {limites.length === 0 ? (
            <p className="ahorro-card__vacio">
              Aún no tienes límites de gasto. Empieza a controlar tus gastos.
            </p>
          ) : (
            limitesCriticos.slice(0, 3).map((limite) => {
              const pct = Math.round(aNumero(limite.porcentaje_usado));
              const estado = estadoLimite(pct);
              return (
                <Link key={limite.id_ahorro} to={ROUTES.LIMITES} className="ahorro-item">
                  <div className="ahorro-item__fila">
                    <span className="ahorro-item__icono">
                      <Icon icon="mdi:tune-variant" />
                    </span>
                    <p className="ahorro-item__nombre">{limite.nombre}</p>
                    <span className={`ahorro-item__pct ahorro-item__pct--${estado}`}>{pct}%</span>
                  </div>
                  <div className="ahorro-item__barra">
                    <div
                      className={`ahorro-item__relleno ahorro-item__relleno--${estado}`}
                      style={{ width: `${Math.min(Math.max(pct, 4), 100)}%` }}
                    />
                  </div>
                </Link>
              );
            })
          )}
        </div>

        <Link to={ROUTES.LIMITES} className="ahorro-card__boton ahorro-card__boton--suave">
          <Icon icon="mdi:cog-outline" />
          Gestionar límites
        </Link>
      </section>

      <section className="ahorro-card">
        <div className="ahorro-card__cabecera">
          <div>
            <h3>Mis metas</h3>
            <p>Ahorro inteligente</p>
          </div>
          <Link to={ROUTES.METAS} className="ahorro-card__ver">
            Ver todas
          </Link>
        </div>

        <div className="ahorro-card__lista">
          {metas.length === 0 ? (
            <p className="ahorro-card__vacio">
              Aún no tienes metas de ahorro. Proponte una y empieza a cumplirla.
            </p>
          ) : (
            metasOrdenadas.slice(0, 3).map((meta) => {
              const pct = Math.min(Math.round(aNumero(meta.porcentaje_completado)), 100);
              return (
                <Link key={meta.id_ahorro} to={ROUTES.METAS} className="ahorro-item">
                  <div className="ahorro-item__fila">
                    <span className="ahorro-item__icono ahorro-item__icono--meta">
                      <Icon icon={pct >= 100 ? 'mdi:flag-checkered' : 'mdi:flag-outline'} />
                    </span>
                    <p className="ahorro-item__nombre">{meta.nombre}</p>
                    <span
                      className={`ahorro-item__pct ${pct >= 100 ? 'ahorro-item__pct--completo' : 'ahorro-item__pct--meta'}`}
                    >
                      {pct}%
                    </span>
                  </div>
                  <div className="ahorro-item__barra">
                    <div
                      className={`ahorro-item__relleno ${pct >= 100 ? 'ahorro-item__relleno--completo' : 'ahorro-item__relleno--meta'}`}
                      style={{ width: `${Math.max(pct, 4)}%` }}
                    />
                  </div>
                </Link>
              );
            })
          )}
        </div>

        <Link to={ROUTES.METAS} className="ahorro-card__boton">
          <Icon icon="mdi:plus" />
          Iniciar meta
        </Link>
      </section>
    </aside>
  );
};

export default SeccionAhorros;