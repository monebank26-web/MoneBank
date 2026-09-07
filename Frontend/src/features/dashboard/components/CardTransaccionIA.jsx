import React from 'react';
import './CardTransaccionIA.css';

const CardTransaccionIA = ({ consejo, generadoConIa, cargandoConsejo }) => (
  <div className="card-consejo-ia">
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
);

export default CardTransaccionIA;
