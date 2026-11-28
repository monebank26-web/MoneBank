import React from 'react';
import { Link } from 'react-router-dom';
import { Icon } from '@iconify/react';
import { ROUTES } from '../../../core/constants';
import './SeccionChatInicio.css';

const SeccionChatInicio = () => {
  return (
    <section className="asesor-banner">
      <div className="asesor-banner__avatar">
        <Icon icon="mdi:creation" />
        <i />
      </div>

      <div className="asesor-banner__contenido">
        <div className="asesor-banner__titulo">
          <h3>Asesor IA</h3>
          <span>
            <i />
            Live
          </span>
        </div>
        <p className="asesor-banner__texto">
          ¿Quieres saber cómo ahorrar este mes o en qué categoría optimizar gastos?
        </p>
        <p className="asesor-banner__subtexto">
          Pregúntale a tu asesor financiero todo sobre tus finanzas.
        </p>
      </div>

      <Link to={ROUTES.CHAT} className="asesor-banner__boton">
        <Icon icon="mdi:message-text-outline" />
        Hablar con tu asesor
      </Link>
    </section>
  );
};

export default SeccionChatInicio;