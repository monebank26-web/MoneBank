import React from 'react';
import { Icon } from '@iconify/react';
import { formatMoney, formatFechaCorta, aNumero } from '../../../core/utils/format';
import './TarjetaRitmoAhorro.css';

const PROXIMO_APORTE_DUMMY = {
  monto: 150000,
  fecha: '2026-10-01',
};

const TarjetaRitmoAhorro = ({ resumen, loading, error, onReintentar }) => {
  const metasEnCurso = aNumero(resumen.cantidad_metas_en_curso);

  return (
    <article className="tarjeta-ritmo-ahorro">
      <p className="etiqueta-ritmo-ahorro">Ritmo de ahorro</p>

      {loading ? (
        <div className="cifra-ritmo-ahorro carga-ritmo-ahorro">
          <span className="numero-ritmo-ahorro">Cargando…</span>
        </div>
      ) : error ? (
        <div className="error-ritmo-ahorro">
          <p>No se pudo cargar: {error}</p>
          <button className="boton-reintentar" onClick={onReintentar}>Reintentar</button>
        </div>
      ) : (
        <div className="cifra-ritmo-ahorro">
          <Icon icon="mdi:piggy-bank" className="icono-cerdito" />
          <span className="numero-ritmo-ahorro">{metasEnCurso}</span>
        </div>
      )}

      <div className="bloque-aporte-programado">
        <p className="etiqueta-aporte-programado">Próximo aporte programado</p>
        <div className="cifras-aporte-programado">
          <span className="fecha-aporte-programado">{formatFechaCorta(PROXIMO_APORTE_DUMMY.fecha)}</span>
          <span className="monto-aporte-programado">{formatMoney(PROXIMO_APORTE_DUMMY.monto)}</span>
        </div>
      </div>
    </article>
  );
};

export default TarjetaRitmoAhorro;