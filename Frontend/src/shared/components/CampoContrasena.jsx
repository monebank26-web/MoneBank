import React, { useState } from 'react';
import './CampoContrasena.css';

const CampoContrasena = ({ className = 'campo-entrada', id, ...props }) => {
  const [visible, setVisible] = useState(false);

  return (
    <div className="envoltorio-campo-contrasena">
      <input
        {...props}
        id={id}
        type={visible ? 'text' : 'password'}
        className={`${className} campo-contrasena-input`}
        autoComplete={props.autoComplete || 'current-password'}
      />
      <button
        type="button"
        className="boton-ver-contrasena"
        onClick={() => setVisible((valorAnterior) => !valorAnterior)}
        aria-label={visible ? 'Ocultar contraseña' : 'Mostrar contraseña'}
        aria-pressed={visible}
      >
        {visible ? (
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M17.94 17.94A10.94 10.94 0 0 1 12 20c-7 0-11-8-11-8a18.5 18.5 0 0 1 5.06-5.94M9.9 4.24A10.94 10.94 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
            <line x1="1" y1="1" x2="23" y2="23" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8Z" />
            <circle cx="12" cy="12" r="3" />
          </svg>
        )}
      </button>
    </div>
  );
};

export default CampoContrasena;