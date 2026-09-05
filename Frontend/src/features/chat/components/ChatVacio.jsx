import React from 'react';
import './ChatVacio.css';

const SUGERENCIAS = [
  '¿Cómo voy con mis finanzas este mes?',
  'Dame ideas para ahorrar más',
  'Ayúdame a organizar mi presupuesto',
];

const ChatVacio = ({ onSugerencia }) => (
  <div className="chat-vacio">
    <div className="chat-vacio__avatar">◈</div>
    <h3 className="chat-vacio__titulo">¡Hola! Soy tu asesor financiero</h3>
    <p className="chat-vacio__texto">
      Pregúntame sobre tus finanzas: cómo ahorrar, qué has gastado este mes,
      cómo distribuir tu dinero o cómo alcanzar tus metas.
    </p>
    <div className="chat-vacio__sugerencias">
      {SUGERENCIAS.map((sugerencia) => (
        <button key={sugerencia} className="boton-sugerencia" onClick={() => onSugerencia(sugerencia)}>
          {sugerencia}
        </button>
      ))}
    </div>
  </div>
);

export default ChatVacio;