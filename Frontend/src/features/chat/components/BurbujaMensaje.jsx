import React from 'react';
import IconoIA from '../../../shared/components/IconoIA';
import MensajeIA from '../../../shared/components/MensajeIA';
import './BurbujaMensaje.css';

const BurbujaMensaje = ({ mensaje, escribiendo }) => {
  const rol = escribiendo ? 'model' : mensaje.rol;

  return (
    <div className={`burbuja burbuja--${rol}`}>
      {rol === 'model' && (
        <div className="burbuja__avatar">
          <IconoIA />
        </div>
      )}
      <div className={escribiendo ? 'burbuja__texto burbuja__texto--escribiendo' : 'burbuja__texto'}>
        {escribiendo ? (
          <>
            <span className="punto-escribiendo" />
            <span className="punto-escribiendo" />
            <span className="punto-escribiendo" />
          </>
        ) : rol === 'model' ? (
          <MensajeIA texto={mensaje.texto} />
        ) : (
          mensaje.texto
        )}
      </div>
    </div>
  );
};

export default BurbujaMensaje;