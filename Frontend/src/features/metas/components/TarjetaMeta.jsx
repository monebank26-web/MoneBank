import React from 'react';
import './TarjetaMeta.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(Number(val) || 0);

const ETIQUETAS_ESTADO = {
  ACTIVO: 'Activa',
  PAUSADO: 'Pausada',
  FINALIZADO: 'Finalizada',
};

const TarjetaMeta = ({ meta, onAbonar }) => {
  const porcentaje = Math.min(Number(meta.porcentaje_completado) || 0, 100);
  const finalizada = meta.estado === 'FINALIZADO' || porcentaje >= 100;

  return (
    <div className={`tarjeta-meta ${finalizada ? 'tarjeta-meta--completada' : ''}`}>
      <div className="encabezado-tarjeta-meta">
        <div>
          <h3 className="nombre-tarjeta-meta">{meta.nombre}</h3>
          {meta.nombre_categoria && (
            <span className="categoria-tarjeta-meta">{meta.nombre_categoria}</span>
          )}
        </div>
        <span className={`estado-meta estado-meta--${(meta.estado || '').toLowerCase()}`}>
          {ETIQUETAS_ESTADO[meta.estado] || meta.estado}
        </span>
      </div>

      <div className="progreso-meta">
        <div className="barra-progreso-meta">
          <div
            className={`relleno-progreso-meta ${porcentaje >= 100 ? 'relleno-progreso-meta--completo' : ''}`}
            style={{ width: `${Math.max(porcentaje, porcentaje > 0 ? 4 : 0)}%` }}
          />
        </div>
        <div className="cifras-progreso-meta">
          <span className="acumulado-meta">{formatMoney(meta.saldo_actual)}</span>
          <span className="objetivo-meta">de {formatMoney(meta.monto_objetivo)}</span>
        </div>
      </div>

      <div className="pie-tarjeta-meta">
        <div className="detalles-tarjeta-meta">
          {!finalizada && Number(meta.monto_faltante) > 0 && (
            <p className="faltante-meta">Falta {formatMoney(meta.monto_faltante)}</p>
          )}
          {finalizada && <p className="faltante-meta faltante-meta--lograda">Meta alcanzada</p>}
          {meta.fecha_objetivo && (
            <p className="fecha-meta">
              Fecha límite: {new Date(`${meta.fecha_objetivo}T00:00:00`).toLocaleDateString('es-CO')}
            </p>
          )}
        </div>
        <button
          className="boton-abonar-meta"
          onClick={() => onAbonar(meta)}
          disabled={finalizada}
          title={finalizada ? 'Esta meta ya está completada' : 'Abonar a esta meta'}
        >
          Abonar
        </button>
      </div>
    </div>
  );
};

export default TarjetaMeta;
