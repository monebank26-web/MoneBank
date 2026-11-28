import React from 'react';

const PanelMarcaAutenticacion = () => {
  return (
    <aside className="panel-marca-autenticacion">
      <video
        className="video-panel-autenticacion"
        autoPlay
        muted
        loop
        playsInline
      >
        <source src="/video.mp4" type="video/mp4" />
      </video>
      <div className="capa-panel-autenticacion" />

      <div className="contenido-panel-autenticacion">
        <div className="marca-panel-autenticacion">
          <img src="/logo.png" alt="MoneBank" className="logo-panel-autenticacion" />
          <span className="nombre-panel-autenticacion">MoneBank</span>
        </div>

        <div className="mensaje-panel-autenticacion">
          <p className="ojo-panel-autenticacion">Finanzas personales y familiares</p>
          <h2 className="titulo-panel-autenticacion">
            Buen criterio para administrar tu <span>dinero</span>.
          </h2>
          <span className="linea-panel-autenticacion" />
        </div>

        <p className="pie-panel-autenticacion">
          © {new Date().getFullYear()} MoneBank. Tu dinero, con clase.
        </p>
      </div>
    </aside>
  );
};

export default PanelMarcaAutenticacion;