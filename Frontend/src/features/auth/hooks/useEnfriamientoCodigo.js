import { useEffect, useState } from 'react';
import {
  SEGUNDOS_ENFRIAMIENTO_CODIGO,
  segundosRestantesEnfriamiento,
} from '../utils/recuperacionPassword';

export const useEnfriamientoCodigo = (
  duracion = SEGUNDOS_ENFRIAMIENTO_CODIGO
) => {
  const [inicio, setInicio] = useState(null);
  const [segundosRestantes, setSegundosRestantes] = useState(0);

  useEffect(() => {
    if (!inicio) return undefined;

    const actualizar = () => {
      const restantes = segundosRestantesEnfriamiento(
        inicio,
        Date.now(),
        duracion
      );

      setSegundosRestantes(restantes);

      if (restantes === 0) setInicio(null);
    };

    actualizar();
    const temporizador = setInterval(actualizar, 1000);

    return () => clearInterval(temporizador);
  }, [inicio, duracion]);

  const iniciarEnfriamiento = () => {
    setInicio(Date.now());
    setSegundosRestantes(duracion);
  };

  return {
    segundosRestantes,
    enfriamientoActivo: segundosRestantes > 0,
    iniciarEnfriamiento,
  };
};
