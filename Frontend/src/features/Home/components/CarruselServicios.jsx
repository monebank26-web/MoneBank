import React, { useState, useEffect, useCallback } from 'react';

const CarruselServicios = ({ servicios }) => {
  const [indiceActivo, setIndiceActivo] = useState(0);
  const total = servicios.length;

  const irSiguiente = useCallback(() => {
    setIndiceActivo((i) => (i + 1) % total);
  }, [total]);

  const irAnterior = () => {
    setIndiceActivo((i) => (i - 1 + total) % total);
  };

  // Avance automático cada 6 segundos; se reinicia el conteo cada vez
  // que el índice cambia (sea por el usuario o por el propio intervalo).
  useEffect(() => {
    const intervalo = setInterval(irSiguiente, 6000);
    return () => clearInterval(intervalo);
  }, [irSiguiente]);

  return (
    <div className="carrusel-servicios">
      <button
        className="flecha-carrusel flecha-carrusel--izquierda"
        onClick={irAnterior}
        aria-label="Servicio anterior"
      >
        ‹
      </button>

      <div className="pista-carrusel">
        <div
          className="lienzo-carrusel"
          style={{ transform: `translateX(-${indiceActivo * 100}%)` }}
        >
          {servicios.map((servicio) => (
            <div className="tarjeta-servicio" key={servicio.titulo}>
              {servicio.imagen ? (
                <img
                  className="imagen-servicio"
                  src={servicio.imagen}
                  alt={servicio.titulo}
                />
              ) : (
                <span className="icono-servicio">{servicio.icono}</span>
              )}
              <h3 className="titulo-servicio">{servicio.titulo}</h3>
              <p className="descripcion-servicio">{servicio.descripcion}</p>
            </div>
          ))}
        </div>
      </div>

      <button
        className="flecha-carrusel flecha-carrusel--derecha"
        onClick={irSiguiente}
        aria-label="Siguiente servicio"
      >
        ›
      </button>

      <div className="puntos-carrusel">
        {servicios.map((servicio, indice) => (
          <button
            key={servicio.titulo}
            className={`punto-carrusel ${indice === indiceActivo ? 'punto-carrusel--activo' : ''}`}
            onClick={() => setIndiceActivo(indice)}
            aria-label={`Ir al servicio ${servicio.titulo}`}
          />
        ))}
      </div>
    </div>
  );
};

export default CarruselServicios;