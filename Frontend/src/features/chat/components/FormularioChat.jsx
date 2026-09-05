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
        Enviar
      </button>
    </form>
  );
};

export default FormularioChat;