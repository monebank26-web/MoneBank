import React from 'react';
import './ComparativoPeriodo.css';

const formatoCOP = (valor) =>
  new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(valor ?? 0);

const calcularVariacion = (actual, anterior) => {
  if (!anterior) return null;
  return ((actual - anterior) / Math.abs(anterior)) * 100;
};

const FILAS = [
  { clave: 'ingresos', etiqueta: 'Ingresos', buenoSiSube: true },
  { clave: 'gastos', etiqueta: 'Gastos', buenoSiSube: false },
  { clave: 'balance', etiqueta: 'Balance', buenoSiSube: true },
];

const COLORES = {
  mejora: '#22c55e',
  empeora: '#ef4444',
  neutra: 'inherit',
};

export const ComparativoPeriodo = ({ actual, anterior, rangoAnterior }) => {
  if (!actual) return null;

  return (
    <section className="cmp">
      <h3 className="cmp__titulo">Comparativo con el periodo anterior</h3>

      {rangoAnterior && (
        <p className="cmp__periodo">
          Periodo anterior: {rangoAnterior.inicio} – {rangoAnterior.fin}
        </p>
      )}

      {!anterior && (
        <p className="cmp__aviso" role="status">
          No hay datos del periodo anterior para comparar.
        </p>
      )}

      <div className="cmp__grid">
        {FILAS.map(({ clave, etiqueta, buenoSiSube }) => {
          const valorActual = actual[clave];
          const valorAnterior = anterior ? anterior[clave] : null;
          const variacion = anterior
            ? calcularVariacion(valorActual, valorAnterior)
            : null;

          let clase = 'neutra';
          let flecha = '';
          if (variacion !== null && variacion !== 0) {
            const sube = variacion > 0;
            clase = sube === buenoSiSube ? 'mejora' : 'empeora';
            flecha = sube ? '▲' : '▼';
          }

          return (
            <div key={clave} className="cmp__item">
              <span className="cmp__etiqueta">{etiqueta}</span>
              <strong className="cmp__valor">{formatoCOP(valorActual)}</strong>

              {anterior && (
                <>
                  <small className="cmp__antes" style={{ opacity: 0.65 }}>
                    Antes: {formatoCOP(valorAnterior)}
                  </small>
                  <small
                    className="cmp__variacion"
                    style={{ color: COLORES[clase], fontWeight: 600 }}
                  >
                    {variacion === null
                      ? '—'
                      : `${flecha} ${Math.abs(variacion).toFixed(1)}%`}
                  </small>
                </>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default ComparativoPeriodo;