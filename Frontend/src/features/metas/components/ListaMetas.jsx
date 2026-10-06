import React from 'react';
import TarjetaMeta from './TarjetaMeta';
import './ListaMetas.css';

const ListaMetas = ({ metas, programacionesPorAhorro, onAbonar, onProgramar, onConsultar }) => (
  <div className="lista-metas">
    {metas.map((meta) => (
      <TarjetaMeta
        key={meta.id_ahorro}
        meta={meta}
        programacion={programacionesPorAhorro?.[meta.id_ahorro]}
        onAbonar={onAbonar}
        onProgramar={onProgramar}
        onConsultar={onConsultar}
      />
    ))}
  </div>
);

export default ListaMetas;
