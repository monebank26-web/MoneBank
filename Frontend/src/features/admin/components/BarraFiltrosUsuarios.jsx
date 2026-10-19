import React from 'react';
import { Icon } from '@iconify/react';
import { ROL_ADMIN, ROL_USUARIO } from '../utils/usuariosAdmin';

const ROLES_FILTRO = [
  { etiqueta: 'Todos', valor: '' },
  { etiqueta: 'Administrador', valor: ROL_ADMIN },
  { etiqueta: 'Usuario', valor: ROL_USUARIO },
];

const ESTADOS_FILTRO = [
  { etiqueta: 'Todos', valor: '' },
  { etiqueta: 'Activo', valor: 'ACTIVO' },
  { etiqueta: 'Inactivo', valor: 'INACTIVO' },
  { etiqueta: 'Bloqueado', valor: 'BLOQUEADO' },
];

const GrupoBotones = ({ etiqueta, opciones, valor, onChange }) => (
  <div className="admin-filtros__grupo">
    <span className="admin-filtros__etiqueta">{etiqueta}</span>
    <div className="admin-grupo-botones">
      {opciones.map((opcion) => (
        <button
          key={opcion.etiqueta}
          type="button"
          className={`admin-grupo-botones__item${valor === opcion.valor ? ' admin-grupo-botones__item--activo' : ''}`}
          onClick={() => onChange(opcion.valor)}
        >
          {opcion.etiqueta}
        </button>
      ))}
    </div>
  </div>
);

const BarraFiltrosUsuarios = ({
  busqueda,
  setBusqueda,
  idRol,
  setIdRol,
  estado,
  setEstado,
  onLimpiar,
}) => (
  <div className="admin-filtros">
    <div className="admin-filtros__fila">
      <div className="admin-filtros__busqueda">
        <Icon icon="mdi:magnify" className="admin-filtros__icono" />
        <input
          className="admin-filtros__campo"
          type="text"
          placeholder="Buscar por nombre, apellido o correo..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
      </div>

      <button type="button" className="admin-filtros__limpiar" onClick={onLimpiar}>
        Limpiar
      </button>
    </div>

    <div className="admin-filtros__grid">
      <GrupoBotones
        etiqueta="Rol"
        opciones={ROLES_FILTRO}
        valor={idRol}
        onChange={setIdRol}
      />
      <GrupoBotones
        etiqueta="Estado"
        opciones={ESTADOS_FILTRO}
        valor={estado}
        onChange={setEstado}
      />
    </div>
  </div>
);

export default BarraFiltrosUsuarios;
