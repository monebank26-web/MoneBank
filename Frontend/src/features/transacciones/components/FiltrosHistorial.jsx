import React, { useState } from 'react';
import { PERIODOS_LIMITE } from '../../../core/constants';
import './FiltrosHistorial.css';

const FiltrosHistorial = ({ onFiltrar, categorias = [] }) => {
  const [busqueda, setBusqueda] = useState('');
  const [tipoFiltro, setTipoFiltro] = useState('');
  const [categoriaFiltro, setCategoriaFiltro] = useState('');
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [montoMin, setMontoMin] = useState('');
  const [montoMax, setMontoMax] = useState('');
  const [ordenarPor, setOrdenarPor] = useState('fecha');
  const [orden, setOrden] = useState('desc');

  const aplicar = () => {
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
  };

  const limpiar = () => {
    setBusqueda(''); setTipoFiltro(''); setCategoriaFiltro('');
    setFechaInicio(''); setFechaFin('');
    setMontoMin(''); setMontoMax('');
    setOrdenarPor('fecha'); setOrden('desc');
    onFiltrar({ pagina: 1, ordenar_por: 'fecha', orden: 'desc' });
  };

  return (
    <div className="filtros-historial">
      <div className="filtros-historial__fila">
        <input className="filtros-historial__busqueda" type="text"
          placeholder="Buscar en descripción..." value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && aplicar()} />

        <div className="filtros-historial__orden">
          <select value={ordenarPor} onChange={(e) => setOrdenarPor(e.target.value)}>
            <option value="fecha">Fecha</option>
            <option value="monto">Monto</option>
          </select>
          <button onClick={() => setOrden(orden === 'asc' ? 'desc' : 'asc')}>
            {orden === 'asc' ? '↑' : '↓'}
          </button>
        </div>

        <button className="filtros-historial__buscar" onClick={aplicar}>Filtrar</button>
        <button className="filtros-historial__limpiar" onClick={limpiar}>Limpiar</button>
      </div>

      <details className="filtros-historial__avanzados">
        <summary>Más filtros</summary>
        <div className="filtros-historial__grid">
          <label>Tipo
            <select value={tipoFiltro} onChange={(e) => setTipoFiltro(e.target.value)}>
              <option value="">Todos</option>
              <option value="1">Gasto</option>
              <option value="2">Ingreso</option>
              <option value="3">Ahorro</option>
            </select>
          </label>
          <label>Categoría
            <select value={categoriaFiltro} onChange={(e) => setCategoriaFiltro(e.target.value)}>
              <option value="">Todas</option>
              {categorias.map((c) => (
                <option key={c.id_categoria} value={c.id_categoria}>{c.nombre_categoria}</option>
              ))}
            </select>
          </label>
          <label>Fecha inicio
            <input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} />
          </label>
          <label>Fecha fin
            <input type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} />
          </label>
          <label>Monto mín.
            <input type="number" value={montoMin} onChange={(e) => setMontoMin(e.target.value)} />
          </label>
          <label>Monto máx.
            <input type="number" value={montoMax} onChange={(e) => setMontoMax(e.target.value)} />
          </label>
        </div>
      </details>
    </div>
  );
};

export default FiltrosHistorial;