import React from 'react';
import { formatMoney } from '../../../core/utils/format';

const CabeceraDetalleBolsillo = ({ bolsillo, onDepositar, onTransferir, onEditar, onEliminar }) => {
  return (
    <div className="tarjeta-cabecera-detalle" style={{ '--color': bolsillo.color }}>
      <div className="franja-color-detalle" />
      <div className="contenido-cabecera-detalle">
        <div className="titulo-cabecera-detalle">
          <span className="punto-color-detalle" />
          <h1 className="nombre-detalle-bolsillo">{bolsillo.nombre}</h1>
        </div>
        {bolsillo.descripcion && <p className="descripcion-detalle-bolsillo">{bolsillo.descripcion}</p>}
        <p className="saldo-detalle-bolsillo">{formatMoney(bolsillo.saldo)}</p>

        <div className="acciones-detalle-bolsillo">
          <button className="boton-tarjeta boton-tarjeta--agregar-dinero" onClick={onDepositar}>
            + Añadir dinero
          </button>
          <button className="boton-tarjeta boton-tarjeta--transferir" onClick={onTransferir}>
            ↔ Transferir
          </button>
          <button className="boton-secundario" onClick={onEditar}>Editar</button>
          <button className="boton-secundario boton-secundario--peligro" onClick={onEliminar}>
            Eliminar
          </button>
        </div>
      </div>
    </div>
  );
};

export default CabeceraDetalleBolsillo;
