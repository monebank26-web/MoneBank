import { useState } from 'react';

export const useIngreso = () => {
  const [modalIngresoAbierto, setModalIngresoAbierto] = useState(false);

  const abrirIngreso = () => setModalIngresoAbierto(true);
  const cerrarIngreso = () => setModalIngresoAbierto(false);

  return {
    modalIngresoAbierto,
    setModalIngresoAbierto,
    abrirIngreso,
    cerrarIngreso,
  };
};
