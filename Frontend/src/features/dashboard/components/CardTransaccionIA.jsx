import React, { useState } from 'react';
import { formatMoney, formatFechaConHora } from '../../../core/utils/format';
import './CardTransaccionIA.css';

const CardTransaccionIA = ({ monto, nombreCategoria, descripcion, fecha, consejo, generadoConIa, cargandoConsejo }) => {
  const [activeTab, setActiveTab] = useState(1);

  return (
    <div className="card-consejo-ia">
      <div className="card-consejo-ia__encabezado">
        <div className="card-consejo-ia__tabs">
          <div className={`card-consejo-ia__indicator ${activeTab === 1 ? 'card-consejo-ia__indicator--despacho' : ''}`} />
          <button
            className={`card-consejo-ia__tab ${activeTab === 0 ? 'card-consejo-ia__tab--activo' : ''}`}
            onClick={() => setActiveTab(0)}
          >
            Transacción
          </button>
          <button
            className={`card-consejo-ia__tab ${activeTab === 1 ? 'card-consejo-ia__tab--activo' : ''}`}
            onClick={() => setActiveTab(1)}
          >
            Consejo IA
          </button>
        </div>
      </div>

      <div className="card-consejo-ia__contenido">
        <div className={`card-consejo-ia__contenido-inner ${activeTab === 1 ? 'card-consejo-ia__contenido-inner--despacho' : ''}`}>
          <div className="card-consejo-ia__panel">
            <div className="card-consejo-ia__transaccion-layout">
              <div className="card-consejo-ia__icono-categoria">↓</div>
              <div className="card-consejo-ia__info-transaccion">
                <p className="card-consejo-ia__nombre-categoria">{nombreCategoria}</p>
                {descripcion && (
                  <p className="card-consejo-ia__descripcion">{descripcion}</p>
                )}
              </div>
              <div className="card-consejo-ia__monto-fecha">
                <p className="card-consejo-ia__monto">{formatMoney(monto)}</p>
                {fecha && (
                  <p className="card-consejo-ia__fecha">{formatFechaConHora(fecha)}</p>
                )}
              </div>
            </div>
          </div>

          <div className="card-consejo-ia__panel">
            {cargandoConsejo ? (
              <div className="card-consejo-ia__cargando">
                <div className="card-consejo-ia__spinner" />
                <p className="card-consejo-ia__consejo-cargando">Obteniendo sugerencia...</p>
              </div>
            ) : consejo ? (
              <>
                <p className="card-consejo-ia__consejo-texto">{consejo}</p>
                {generadoConIa && (
                  <div className="card-consejo-ia__badge">
                    <span className="card-consejo-ia__badge-punto" />
                    Sugerencia generada con IA
                  </div>
                )}
              </>
            ) : (
              <p className="card-consejo-ia__consejo-error">No se pudo obtener la sugerencia.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardTransaccionIA;
