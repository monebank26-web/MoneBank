import React from 'react';
import BadgeIA from '../../../shared/components/BadgeIA';
import './EncabezadoChat.css';

const EncabezadoChat = ({ cantidadMensajes, onLimpiar }) => (
  <div className="encabezado-chat">
    <div>
      <h1 className="titulo-chat">Asesor IA</h1>
      <p className="subtitulo-chat">Tu acompañante financiero inteligente</p>
    </div>
    <div className="acciones-chat">
      <BadgeIA />
      {cantidadMensajes > 0 && (
        <button className="boton-chat-limpiar" onClick={onLimpiar}>Limpiar</button>
      )}
    </div>
  </div>
);

export default EncabezadoChat;