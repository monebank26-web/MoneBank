import React, { useState, useRef, useEffect } from 'react';

const MenuOpcionesBolsillo = ({ onEditar, onEliminar, onDepositar, onTransferir }) => {
  const [abierto, setAbierto] = useState(false);
  const referencia = useRef(null);

  useEffect(() => {
    const cerrarSiClickAfuera = (e) => {
      if (referencia.current && !referencia.current.contains(e.target)) setAbierto(false);
    };
    document.addEventListener('mousedown', cerrarSiClickAfuera);
    return () => document.removeEventListener('mousedown', cerrarSiClickAfuera);
  }, []);

  return (
    <div className="menu-opciones-bolsillo" ref={referencia}>
      <button className="boton-menu-opciones-bolsillo" onClick={() => setAbierto(!abierto)}>⋮</button>
      {abierto && (
        <div className="desplegable-menu-opciones-bolsillo">
          <button onClick={() => { onDepositar(); setAbierto(false); }}>Añadir dinero</button>
          <button onClick={() => { onTransferir(); setAbierto(false); }}>Transferir</button>
          <button onClick={() => { onEditar(); setAbierto(false); }}>Editar</button>
          <div className="separador-menu-opciones-bolsillo" />
          <button className="opcion-peligrosa" onClick={() => { onEliminar(); setAbierto(false); }}>Eliminar</button>
        </div>
      )}
    </div>
  );
};

export default MenuOpcionesBolsillo;
