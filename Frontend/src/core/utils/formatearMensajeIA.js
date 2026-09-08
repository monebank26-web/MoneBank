import React from 'react';

const MONTO_REGEX =
  /\$\s?\d[\d.,]*|\$?\d{1,3}(?:[.,]\d{3})+(?:\s?(?:COP|USD|EUR))?|\d+\s?(?:COP|USD|EUR)|\d{4,}/;

const INLINE_BOLD_RE = /(\*\*[^*]+\*\*)/g;
const INLINE_ITALIC_RE = /(\*[^*]+\*)/g;

const LIMPIEZA_RE = /[*`_]/g;

const formatearMensajeIA = (texto) => {
  const nodos = [];
  let clave = 0;
  const darClave = () => clave++;

  const bloques = String(texto || '').split('\n');

  bloques.forEach((linea) => {
    const contenido = linea.trim();
    if (!contenido) return;

    const viñeta = contenido.match(/^[-•]\s+(.*)$/);
    const numerada = contenido.match(/^(\d+)[.)]\s+(.*)$/);

    if (viñeta) {
      nodos.push(
        <div className="mensaje-ia__linea" key={darClave()}>
          <span className="mensaje-ia__marcador" aria-hidden="true" />
          <span className="mensaje-ia__contenido-linea">
            {inline(viñeta[1], darClave)}
          </span>
        </div>
      );
    } else if (numerada) {
      nodos.push(
        <div className="mensaje-ia__linea mensaje-ia__linea--numerada" key={darClave()}>
          <span className="mensaje-ia__numero" aria-hidden="true">
            {numerada[1]}
          </span>
          <span className="mensaje-ia__contenido-linea">
            {inline(numerada[2], darClave)}
          </span>
        </div>
      );
    } else {
      nodos.push(
        <p className="mensaje-ia__parrafo" key={darClave()}>
          {inline(contenido, darClave)}
        </p>
      );
    }
  });

  return nodos;
};

const inline = (texto, darClave) => {
  const salida = [];
  const partes = texto.split(INLINE_BOLD_RE);

  partes.forEach((parte) => {
    if (!parte) return;

    if (esNegrita(parte)) {
      const contenido = cuerpo(parte.slice(2, -2), darClave);
      if (soloMontos(contenido)) {
        salida.push(...contenido);
      } else {
        salida.push(
          <strong className="mensaje-ia__negrita" key={darClave()}>
            {contenido}
          </strong>
        );
      }
      return;
    }

    const subpartes = parte.split(INLINE_ITALIC_RE);
    subpartes.forEach((subparte) => {
      if (!subparte) return;

      if (esItalica(subparte)) {
        salida.push(
          <em className="mensaje-ia__italica" key={darClave()}>
            {cuerpo(subparte.slice(1, -1), darClave)}
          </em>
        );
      } else {
        salida.push(...cuerpo(subparte, darClave));
      }
    });
  });

  return salida;
};

const esNegrita = (parte) => parte.startsWith('**') && parte.endsWith('**') && parte.length > 4;

const esItalica = (parte) => parte.startsWith('*') && parte.endsWith('*') && parte.length > 2;

const soloMontos = (nodos) =>
  nodos.length > 0 && nodos.every((nodo) => typeof nodo === 'object' && nodo !== null);

const cuerpo = (texto, darClave) => {
  const limpio = texto.replace(LIMPIEZA_RE, '');
  const salida = [];
  let indice = 0;
  const busqueda = new RegExp(MONTO_REGEX.source, 'g');
  let coincidencia;

  while ((coincidencia = busqueda.exec(limpio)) !== null) {
    if (coincidencia.index > indice) {
      salida.push(limpio.slice(indice, coincidencia.index));
    }
    salida.push(
      <span className="mensaje-ia__monto" key={darClave()}>
        {coincidencia[0]}
      </span>
    );
    indice = coincidencia.index + coincidencia[0].length;
  }

  if (indice < limpio.length) {
    salida.push(limpio.slice(indice));
  }

  return salida;
};

export { formatearMensajeIA };