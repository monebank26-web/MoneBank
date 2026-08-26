import React from 'react';
import TarjetaMeta from './TarjetaMeta';

const ListaMetas = ({ metas, onAbonar }) => (
  <div className="lista-metas">
    {metas.map((meta) => (
      <TarjetaMeta key={meta.id_ahorro} meta={meta} onAbonar={onAbonar} />
    ))}
  </div>
);

export default ListaMetas;
