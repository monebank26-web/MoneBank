import React from 'react';
import { Link } from 'react-router-dom';
import { ROUTES } from '../../../core/constants';

const SeccionChatInicio = () => {
  return (
    <section className="seccion-inicio">
      <div className="encabezado-seccion-inicio">
        <h3>Asesor IA</h3>
        <span className="badge-ia-chat badge-ia-chat--mini">
          <span className="badge-ia-chat__punto" />
          IA
        </span>
      </div>

      <div className="chat-inicio">
        <div className="chat-inicio__avatar">◈</div>
        <div className="chat-inicio__contenido">
          <p className="chat-inicio__texto">
            ¿Quieres saber cómo ahorrar este mes o qué gastaste en supermercado?
          </p>
          <p className="chat-inicio__subtexto">
            Pregúntale a tu asesor financiero todo sobre tu dinero.
          </p>
          <Link to={ROUTES.CHAT} className="chat-inicio__cta">
            Hablar con tu asesor
          </Link>
        </div>
      </div>
    </section>
  );
};

export default SeccionChatInicio;
