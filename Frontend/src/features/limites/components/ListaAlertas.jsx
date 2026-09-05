import React from 'react';
import './ListaAlertas.css';

const ListaAlertas = ({ alertas }) => {
  if (!alertas || alertas.length === 0) return null;

  return (
    <div className="lista-alertas-limite">
      {alertas.map((a, i) => (
        <div
          key={i}
          className={`alerta-limite ${
            a.tipo_alerta === 'LIMITE_SUPERADO' ? 'alerta-limite--superado' : 'alerta-limite--preventiva'
          }`}
        >
          <span className="icono-alerta-limite">
            {a.tipo_alerta === 'LIMITE_SUPERADO' ? '✕' : '!'}
          </span>
          <div className="contenido-alerta-limite">
            <p className="mensaje-alerta-limite">{a.mensaje}</p>
            {a.fecha && (
              <p className="fecha-alerta-limite">
                {new Date(`${a.fecha}T00:00:00`).toLocaleDateString('es-CO')}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ListaAlertas;
