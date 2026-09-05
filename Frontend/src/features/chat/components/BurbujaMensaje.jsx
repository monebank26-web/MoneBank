import React from 'react';
import './BurbujaMensaje.css';

const BurbujaMensaje = ({ mensaje, escribiendo }) => {
  const rol = escribiendo ? 'model' : mensaje.rol;

  return (
    <div className={`burbuja burbuja--${rol}`}>
      {rol === 'model' && <div className="burbuja__avatar">◈</div>}
      <div className={escribiendo ? 'burbuja__texto burbuja__texto--escribiendo' : 'burbuja__texto'}>
        {escribiendo ? (
          <>
            <span className="punto-escribiendo" />
            <span className="punto-escribiendo" />
            <span className="punto-escribiendo" />
          </>
        ) : (
          mensaje.texto
        )}
      </div>
    </div>
  );
};

export default BurbujaMensaje;