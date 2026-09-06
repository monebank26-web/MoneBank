import React from 'react';
import BadgeIA from '../../../shared/components/BadgeIA';
import IconoIA from '../../../shared/components/IconoIA';
import './EncabezadoChat.css';

const EncabezadoChat = ({ cantidadMensajes, onLimpiar }) => (
  <div className="encabezado-chat">
    <div className="encabezado-chat__titular">
      <div className="encabezado-chat__avatar">
        <IconoIA />
      </div>
      <div>
        <div className="encabezado-chat__titulo-fila">
          <h1 className="titulo-chat">Asesor IA</h1>
          <span className="pill-en-linea">
            <span className="pill-en-linea__punto" aria-hidden="true" />
            En línea
          </span>
        </div>
        <p className="subtitulo-chat">Tu acompañante financiero inteligente</p>
      </div>
    </div>
    <div className="acciones-chat">
      <BadgeIA />
      {cantidadMensajes > 0 && (
        <button className="boton-chat-limpiar" onClick={onLimpiar}>Limpiar</button>
      )}
      <img src="/logo.png" alt="MoneBank" className="logo-chat" />
    </div>
  </div>
);

export default EncabezadoChat;