import React from 'react';
import './FormularioChat.css';

const FormularioChat = ({ valor, onChange, onEnviar, cargando }) => {
  const handleEnviar = (e) => {
    e.preventDefault();
    const texto = valor.trim();
    if (!texto || cargando) return;
    onEnviar(texto);
  };

  return (
    <form className="formulario-chat" onSubmit={handleEnviar}>
      <input
        className="entrada-chat"
        placeholder="Escribe tu pregunta sobre tus finanzas..."
        value={valor}
        onChange={(e) => onChange(e.target.value)}
        disabled={cargando}
      />
      <button className="boton-enviar-chat" type="submit" disabled={cargando || !valor.trim()}>
        <svg
          className="boton-enviar-chat__icono"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M22 2 11 13" />
          <path d="m22 2-7 20-4-9-9-4Z" />
        </svg>
        <span>Enviar</span>
      </button>
    </form>
  );
};

export default FormularioChat;