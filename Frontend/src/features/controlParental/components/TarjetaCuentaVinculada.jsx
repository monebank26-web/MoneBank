import React from 'react';

const TarjetaCuentaVinculada = ({ usuarioVinculado, etiquetaRelacion, onDesvincular, children }) => {
  return (
    <div className="tarjeta-vinculado">
      <div className="encabezado-vinculado">
        <div className="avatar-vinculado">
          {usuarioVinculado.nombre.charAt(0).toUpperCase()}
        </div>
        <div>
          <p className="nombre-vinculado">{usuarioVinculado.nombre}</p>
          <p className="correo-vinculado">{usuarioVinculado.email}</p>
          <span className="etiqueta-vinculado">{etiquetaRelacion}</span>
        </div>
        <button className="boton-desvincular" onClick={onDesvincular}>
          Desvincular
        </button>
      </div>

      {children}
    </div>
  );
};

export default TarjetaCuentaVinculada;
