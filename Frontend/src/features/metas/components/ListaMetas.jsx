import React from 'react';
import TarjetaMeta from './TarjetaMeta';
import './ListaMetas.css';

const ListaMetas = ({ metas, onAbonar, onProgramar }) => (
  <div className="lista-metas">
    {metas.map((meta) => (
      <TarjetaMeta key={meta.id_ahorro} meta={meta} onAbonar={onAbonar} onProgramar={onProgramar} />
    ))}
  </div>
);

export default ListaMetas;
