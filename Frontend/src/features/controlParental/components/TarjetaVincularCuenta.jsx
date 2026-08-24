import React from 'react';

const TarjetaVincularCuenta = ({ icono, titulo, descripcion, placeholder, correoVincular, setCorreoVincular, onVincular }) => {
  return (
    <div className="tarjeta-vincular">
      <div className="icono-vincular">{icono}</div>
      <h2 className="titulo-vincular">{titulo}</h2>
      <p className="descripcion-vincular">{descripcion}</p>
      <div className="campo-vincular">
        <input
          className="campo-entrada-parental"
          type="email"
          placeholder={placeholder}
          value={correoVincular}
          onChange={(e) => setCorreoVincular(e.target.value)}
        />
        <button className="boton-vincular" onClick={onVincular}>
          Vincular cuenta
        </button>
      </div>
    </div>
  );
};

export default TarjetaVincularCuenta;
