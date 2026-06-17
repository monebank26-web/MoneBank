// shared/components/Modal.jsx
import React, { useEffect } from 'react';
import './Modal.css';

const Modal = ({ open, onClose, title, children }) => {
  useEffect(() => {
    const handleKey = (e) => { if (e.key === 'Escape') onClose(); };
    if (open) document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div className="fondo-modal" onClick={onClose}>
      <div className="caja-modal" onClick={(e) => e.stopPropagation()}>
        <div className="encabezado-modal">
          <h3 className="titulo-modal">{title}</h3>
          <button className="boton-cerrar-modal" onClick={onClose}>✕</button>
        </div>
        <div className="cuerpo-modal">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
