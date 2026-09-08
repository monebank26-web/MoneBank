 import React from 'react';
import { useTheme } from '../../../core/context/ThemeContext';

const ToggleTema = () => {
  const { theme, toggleTheme } = useTheme();
  const esOscuro = theme === 'dark';

  return (
    <button
      className="boton-toggle-tema"
      onClick={toggleTheme}
      aria-label={esOscuro ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
      title={esOscuro ? 'Modo claro' : 'Modo oscuro'}
    >
      <span className={`interruptor-tema ${esOscuro ? '' : 'interruptor-tema--claro'}`}>
        <span className="perilla-tema">{esOscuro ? '🌙' : '☀️'}</span>
      </span>
    </button>
  );
};

export default ToggleTema;
