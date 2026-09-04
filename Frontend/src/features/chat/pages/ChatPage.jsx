import React, { useState, useRef, useEffect } from 'react';
import { useChatIA } from '../hooks/useChatIA';
import './ChatPage.css';

const ChatPage = () => {
  const { mensajes, cargando, error, enviar, limpiar } = useChatIA();
  const [entrada, setEntrada] = useState('');
  const finalMensajes = useRef(null);

  useEffect(() => {
    finalMensajes.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes, cargando]);

  const handleEnviar = async (e) => {
    e.preventDefault();
    const texto = entrada.trim();
    if (!texto || cargando) return;
    setEntrada('');
    await enviar(texto);
  };

  return (
    <div className="pagina-chat">
      <div className="encabezado-chat">
        <div>
          <h1 className="titulo-chat">Asesor IA</h1>
          <p className="subtitulo-chat">Tu acompañante financiero inteligente</p>
        </div>
        <div className="acciones-chat">
          <span className="badge-ia-chat">
            <span className="badge-ia-chat__punto" />
            IA
          </span>
          {mensajes.length > 0 && (
            <button className="boton-chat-limpiar" onClick={limpiar}>Limpiar</button>
          )}
        </div>
      </div>

      <div className="panel-conversacion">
        {mensajes.length === 0 ? (
          <div className="chat-vacio">
            <div className="chat-vacio__avatar">◈</div>
            <h3 className="chat-vacio__titulo">¡Hola! Soy tu asesor financiero</h3>
            <p className="chat-vacio__texto">
              Pregúntame sobre tus finanzas: cómo ahorrar, qué has gastado este mes,
              cómo distribuir tu dinero o cómo alcanzar tus metas.
            </p>
            <div className="chat-vacio__sugerencias">
              <button className="boton-sugerencia" onClick={() => enviar('¿Cómo voy con mis finanzas este mes?')}>
                ¿Cómo voy este mes?
              </button>
              <button className="boton-sugerencia" onClick={() => enviar('Dame ideas para ahorrar más')}>
                Ideas para ahorrar
              </button>
              <button className="boton-sugerencia" onClick={() => enviar('Ayúdame a organizar mi presupuesto')}>
                Organizar mi presupuesto
              </button>
            </div>
          </div>
        ) : (
          <div className="lista-mensajes">
            {mensajes.map((mensaje, idx) => (
              <div
                key={idx}
                className={`burbuja burbuja--${mensaje.rol}`}
              >
                {mensaje.rol === 'model' && <div className="burbuja__avatar">◈</div>}
                <div className="burbuja__texto">{mensaje.texto}</div>
              </div>
            ))}
            {cargando && (
              <div className="burbuja burbuja--model">
                <div className="burbuja__avatar">◈</div>
                <div className="burbuja__texto burbuja__texto--escribiendo">
                  <span className="punto-escribiendo" />
                  <span className="punto-escribiendo" />
                  <span className="punto-escribiendo" />
                </div>
              </div>
            )}
            <div ref={finalMensajes} />
          </div>
        )}
      </div>

      {error && <p className="error-chat">{error}</p>}

      <form className="formulario-chat" onSubmit={handleEnviar}>
        <input
          className="entrada-chat"
          placeholder="Escribe tu pregunta sobre tus finanzas..."
          value={entrada}
          onChange={(e) => setEntrada(e.target.value)}
          disabled={cargando}
        />
        <button className="boton-enviar-chat" type="submit" disabled={cargando || !entrada.trim()}>
          Enviar
        </button>
      </form>
    </div>
  );
};

export default ChatPage;
