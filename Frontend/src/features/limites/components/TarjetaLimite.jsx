import React from 'react';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(Number(val) || 0);

const ETIQUETAS_PERIODO = {
  DIARIO: 'Diario',
  SEMANAL: 'Semanal',
  MENSUAL: 'Mensual',
};

const TarjetaLimite = ({ limite }) => {
  const porcentaje = Number(limite.porcentaje_usado) || 0;
  const ancho = Math.min(porcentaje, 100);
  const superado = porcentaje >= 100;
  const enAlerta = porcentaje >= 70 && !superado;

  const claseBarra = superado
    ? 'relleno-progreso-limite--superado'
    : enAlerta
      ? 'relleno-progreso-limite--alerta'
      : 'relleno-progreso-limite--ok';

  const disponible = Number(limite.monto_disponible) || 0;

  return (
    <div className={`tarjeta-limite ${superado ? 'tarjeta-limite--superado' : ''}`}>
      <div className="encabezado-tarjeta-limite">
        <div>
          <h3 className="nombre-tarjeta-limite">{limite.nombre}</h3>
          {limite.nombre_categoria && (
            <span className="categoria-tarjeta-limite">{limite.nombre_categoria}</span>
          )}
        </div>
        <div className="etiquetas-tarjeta-limite">
          {limite.periodo && (
            <span className="periodo-limite">{ETIQUETAS_PERIODO[limite.periodo] || limite.periodo}</span>
          )}
          {superado && <span className="estado-limite estado-limite--superado">Superado</span>}
          {!superado && enAlerta && <span className="estado-limite estado-limite--alerta">Cerca del tope</span>}
        </div>
      </div>

      <div className="progreso-limite">
        <div className="barra-progreso-limite">
          <div
            className={`relleno-progreso-limite ${claseBarra}`}
            style={{ width: `${Math.max(ancho, porcentaje > 0 ? 4 : 0)}%` }}
          />
        </div>
        <div className="cifras-progreso-limite">
          <span className={`gasto-actual-limite ${superado ? 'gasto-actual-limite--superado' : ''}`}>
            {formatMoney(limite.gasto_actual)}
          </span>
          <span className="tope-limite">tope {formatMoney(limite.monto_limite)} · {Math.round(porcentaje)}%</span>
        </div>
      </div>

      <p className={`disponible-limite ${superado ? 'disponible-limite--superado' : ''}`}>
        {superado
          ? `Te pasaste por ${formatMoney(Math.abs(disponible))}`
          : `Disponible: ${formatMoney(disponible)}`}
      </p>
    </div>
  );
};

export default TarjetaLimite;
