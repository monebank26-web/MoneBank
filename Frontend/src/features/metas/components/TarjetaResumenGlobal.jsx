import React from 'react';
import { Icon } from '@iconify/react';
import { formatMoney, aNumero } from '../../../core/utils/format';
import './TarjetaResumenGlobal.css';

const TarjetaResumenGlobal = ({ resumen, loading, error, onReintentar }) => {
  const porcentaje = Math.min(aNumero(resumen.porcentaje_consolidado), 100);

  return (
    <article className="tarjeta-resumen-global">
      <p className="etiqueta-resumen-global">Total ahorrado hasta ahora</p>

      {loading ? (
        <div className="cifra-resumen-global carga-resumen-global">
          <span className="monto-resumen-global">Cargando…</span>
        </div>
      ) : error ? (
        <div className="error-resumen-global">
          <p>No se pudo cargar el resumen: {error}</p>
          <button className="boton-reintentar" onClick={onReintentar}>Reintentar</button>
        </div>
      ) : (
        <div className="cifra-resumen-global">
          <Icon icon="mdi:wallet-outline" className="icono-billetera" />
          <span className="monto-resumen-global">{formatMoney(resumen.total_ahorrado)}</span>
        </div>
      )}

      <div className="bloque-meta-global">
        <div className="fila-meta-global">
          <p className="etiqueta-meta-global">Meta global</p>
          <div className="cifras-meta-global">
            <span className="objetivo-meta-global">{formatMoney(resumen.monto_objetivo_total)}</span>
            <span className="porcentaje-meta-global">{Math.round(porcentaje)}%</span>
          </div>
        </div>
        <div className="barra-progreso-global">
          <div
            className={`relleno-progreso-global ${porcentaje >= 100 ? 'relleno-progreso-global--completo' : ''}`}
            style={{ width: `${Math.max(porcentaje, porcentaje > 0 ? 4 : 0)}%` }}
          />
        </div>
      </div>
    </article>
  );
};

export default TarjetaResumenGlobal;