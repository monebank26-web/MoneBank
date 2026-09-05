import React, { useRef, useEffect } from 'react';
import BurbujaMensaje from './BurbujaMensaje';
import './ListaMensajes.css';

const ListaMensajes = ({ mensajes, cargando }) => {
  const finalMensajes = useRef(null);

  useEffect(() => {
    finalMensajes.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes, cargando]);

  return (
    <div className="lista-mensajes">
      {mensajes.map((mensaje, idx) => (
        <BurbujaMensaje key={idx} mensaje={mensaje} />
      ))}
      {cargando && <BurbujaMensaje escribiendo />}
      <div ref={finalMensajes} />
    </div>
  );
};

export default ListaMensajes;