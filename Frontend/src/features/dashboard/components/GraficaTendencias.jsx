import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { useTheme } from '../../../core/context/ThemeContext';
import { formatMoney } from '../../../core/utils/format';
import './GraficaTendencias.css';

const GraficaTendencias = ({ serie, anio, aniosDisponibles, onCambiarAnio, cargando }) => {
  const { theme } = useTheme();
  const colorLinea = theme === 'dark' ? '#d4af37' : '#9c7a16';
  const colorRejilla = theme === 'dark' ? '#2a261c' : '#e8dcc0';
  const colorTexto = theme === 'dark' ? '#b8ae98' : '#5c4f30';

  const sinDatos = !serie.some((punto) => punto.ingresos > 0 || punto.gastos > 0);

  return (
    <section className="grafica-tendencias">
      <div className="grafica-tendencias__encabezado">
        <div>
          <h3 className="grafica-tendencias__titulo">Tendencia anual</h3>
          <p className="grafica-tendencias__subtitulo">
            Cómo evoluciona tu saldo neto durante el año
          </p>
        </div>

        <div className="grafica-tendencias__anios">
          {aniosDisponibles.map((a) => (
            <button
              key={a}
              type="button"
              className={`boton-anio ${a === anio ? 'boton-anio--activo' : ''}`}
              onClick={() => onCambiarAnio(a)}
            >
              {a}
            </button>
          ))}
        </div>
      </div>

      {cargando ? (
        <p className="grafica-tendencias__mensaje">Cargando tendencia...</p>
      ) : sinDatos ? (
        <p className="grafica-tendencias__mensaje">
          Aún no hay movimientos registrados en {anio}.
        </p>
      ) : (
        <div className="grafica-tendencias__lienzo">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={serie} margin={{ top: 10, right: 12, left: 12, bottom: 0 }}>
              <defs>
                <linearGradient id="relleno-tendencia" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={colorLinea} stopOpacity={0.3} />
                  <stop offset="100%" stopColor={colorLinea} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid horizontal={false} stroke={colorRejilla} />
              <XAxis
                dataKey="etiqueta"
                tickLine={false}
                axisLine={false}
                tick={{ fill: colorTexto, fontSize: 11, letterSpacing: 1.5 }}
                minTickGap={8}
              />
              <YAxis hide domain={['auto', 'auto']} />
              <Tooltip
                cursor={{ stroke: colorLinea, strokeOpacity: 0.4 }}
                contentStyle={{
                  background: 'var(--color-surface)',
                  border: '1px solid var(--color-border)',
                  borderRadius: 8,
                  color: 'var(--color-text)',
                }}
                labelStyle={{ color: 'var(--color-text-soft)' }}
                formatter={(valor) => [formatMoney(valor), 'Neto acumulado']}
              />
              <Area
                type="monotone"
                dataKey="acumulado"
                stroke={colorLinea}
                strokeWidth={3}
                fill="url(#relleno-tendencia)"
                dot={false}
                activeDot={{ r: 5, fill: colorLinea, stroke: 'var(--color-surface)', strokeWidth: 2 }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
};

export default GraficaTendencias;