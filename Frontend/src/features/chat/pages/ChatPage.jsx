import React, { useState } from 'react';
import { useChatIA } from '../hooks/useChatIA';
import EncabezadoChat from '../components/EncabezadoChat';
import ChatVacio from '../components/ChatVacio';
import ListaMensajes from '../components/ListaMensajes';
import FormularioChat from '../components/FormularioChat';
import './ChatPage.css';

const ChatPage = () => {
  const { mensajes, cargando, error, enviar, limpiar } = useChatIA();
  const [entrada, setEntrada] = useState('');

  return (
    <div className="pagina-chat">
      <EncabezadoChat cantidadMensajes={mensajes.length} onLimpiar={limpiar} />

      <div className="panel-conversacion">
        {mensajes.length === 0 ? (
          <ChatVacio onSugerencia={enviar} />
        ) : (
          <ListaMensajes mensajes={mensajes} cargando={cargando} />
        )}
      </div>

      {error && <p className="error-chat">{error}</p>}

      <FormularioChat
        valor={entrada}
        onChange={setEntrada}
        onEnviar={enviar}
        cargando={cargando}
      />
    </div>
  );
};

export default ChatPage;