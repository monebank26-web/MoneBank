import React, { useState, useEffect, useRef } from 'react';
import { useMediaQuery } from '../../../core/hooks/useMediaQuery';
import './FiltrosHistorial.css';

const TIPOS = [
  { etiqueta: 'Ingreso', valor: '1' },
  { etiqueta: 'Gasto', valor: '2' },
  { etiqueta: 'Mov. a Meta', valor: '3' },
];

const FiltrosHistorial = ({ onFiltrar, categorias = [] }) => {
  const esMovil = useMediaQuery('(max-width: 768px)');

  const [busqueda, setBusqueda] = useState('');
  const [tipoFiltro, setTipoFiltro] = useState('');
  const [categoriaFiltro, setCategoriaFiltro] = useState('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [montoMin, setMontoMin] = useState('');
  const [montoMax, setMontoMax] = useState('');
  const [ordenarPor, setOrdenarPor] = useState('fecha');
  const [orden, setOrden] = useState('desc');

 const primero = useRef(true);

useEffect(() => {
  if (primero.current) {
    primero.current = false;
    return;
  }
  const timeout = setTimeout(() => {
    onFiltrar({
      busqueda: busqueda || undefined,
      id_tipo_transaccion: tipoFiltro || undefined,
      id_categoria: categoriaFiltro || undefined,
      fecha_inicio: fechaInicio || undefined,
      fecha_fin: fechaFin || undefined,
      monto_min: montoMin || undefined,
      monto_max: montoMax || undefined,
      ordenar_por: ordenarPor,
      orden: orden,
      pagina: 1,
    });
  }, 300);
  return () => clearTimeout(timeout);
}, [busqueda, tipoFiltro, categoriaFiltro, fechaInicio, fechaFin, montoMin, montoMax, ordenarPor, orden]);

  const limpiar = () => {
    setBusqueda(''); setTipoFiltro(''); setCategoriaFiltro('');
    setFechaInicio(''); setFechaFin('');
    setMontoMin(''); setMontoMax('');
    setOrdenarPor('fecha'); setOrden('desc');
    onFiltrar({ pagina: 1, ordenar_por: 'fecha', orden: 'desc' });
  };

  const toggleTipo = (valor) => {
    setTipoFiltro(tipoFiltro === valor ? '' : valor);
  };

  const contenidoAvanzados = (
    <div className="filtros-historial__grid">
      <div className="filtros-historial__campo">
        <span className="filtros-historial__etiqueta">Tipo</span>
        <div className="grupo-botones">
          {TIPOS.map((t) => (
            <button
              key={t.valor}
              type="button"
              className={`grupo-botones__item ${tipoFiltro === t.valor ? 'grupo-botones__item--activo' : ''}`}
              onClick={() => toggleTipo(t.valor)}
            >
              {t.etiqueta}
            </button>
          ))}
        </div>
      </div>

      <label className="filtros-historial__campo">
        Categoría
        <select value={categoriaFiltro} onChange={(e) => setCategoriaFiltro(e.target.value)}>
          <option value="">Todas</option>
          {categorias.map((c) => (
            <option key={c.id_categoria} value={c.id_categoria}>{c.nombre_categoria}</option>
          ))}
        </select>
      </label>

      <div className="filtros-historial__campo">
        <span className="filtros-historial__etiqueta">Fecha</span>
        <div className="grupo-rango">
          <input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} aria-label="Fecha inicio" />
          <span className="grupo-rango__conector">–</span>
          <input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} aria-label="Fecha fin" />
        </div>
      </div>

      <div className="filtros-historial__campo">
        <span className="filtros-historial__etiqueta">Monto</span>
        <div className="grupo-rango">
          <input type="number" placeholder="Mín" value={montoMin} onChange={(e) => setMontoMin(e.target.value)} />
          <span className="grupo-rango__conector">–</span>
          <input type="number" placeholder="Máx" value={montoMax} onChange={(e) => setMontoMax(e.target.value)} />
        </div>
      </div>
    </div>
  );

  return (
    <div className="filtros-historial">
      <div className="filtros-historial__fila">
        <input className="filtros-historial__busqueda" type="text"
          placeholder="Buscar en descripción..." value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)} />

        <div className="grupo-botones filtros-historial__orden">
          <button
            type="button"
            className={`grupo-botones__item ${ordenarPor === 'fecha' ? 'grupo-botones__item--activo' : ''}`}
            onClick={() => setOrdenarPor('fecha')}
          >
            Fecha
          </button>
          <button
            type="button"
            className={`grupo-botones__item ${ordenarPor === 'monto' ? 'grupo-botones__item--activo' : ''}`}
            onClick={() => setOrdenarPor('monto')}
          >
            Monto
          </button>
          <button
            type="button"
            className="grupo-botones__item grupo-botones__direccion"
            onClick={() => setOrden(orden === 'asc' ? 'desc' : 'asc')}
            title={`Orden ${orden === 'asc' ? 'ascendente' : 'descendente'}`}
          >
            {orden === 'asc' ? '↑' : '↓'}
          </button>
        </div>

        <button className="filtros-historial__limpiar" onClick={limpiar}>Limpiar</button>
      </div>

      {esMovil ? (
        <details className="filtros-historial__avanzados">
          <summary>Más filtros</summary>
          {contenidoAvanzados}
        </details>
      ) : (
        <div className="filtros-historial__avanzados filtros-historial__avanzados--desplegados">
          {contenidoAvanzados}
        </div>
      )}
    </div>
  );
};

export default FiltrosHistorial;