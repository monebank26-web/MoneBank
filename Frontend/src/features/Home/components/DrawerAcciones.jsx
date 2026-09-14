import React, { useEffect } from 'react';
import './DrawerAcciones.css';

const DrawerAcciones = ({ open, onClose, children }) => {
  useEffect(() => {
    if (!open) return;
    const handleKey = (e) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fondo-drawer-inicio" onClick={onClose}>
      <div className="panel-drawer-inicio" onClick={(e) => e.stopPropagation()}>
        <div className="encabezado-drawer-inicio">
          <span className="titulo-drawer-inicio">MoneBank</span>
          <button className="boton-cerrar-drawer-inicio" onClick={onClose}>✕</button>
        </div>
        <div className="cuerpo-drawer-inicio">
          {children}
        </div>
      </div>
    </div>
  );
};

export default DrawerAcciones;
