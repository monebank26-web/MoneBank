import { useState } from 'react';
import { consejoIaService } from '../services/consejoIaService';

export const useConsejoIA = ({ montoGasto, idCategoriaGasto }) => {
  const [consejoIA, setConsejoIA] = useState(null);
  const [generadoConIa, setGeneradoConIa] = useState(false);
  const [cargandoConsejo, setCargandoConsejo] = useState(false);
  const [mostrandoConsejo, setMostrandoConsejo] = useState(false);

  const handleVerConsejo = () => {
    const m = parseFloat(montoGasto);
    if (!m || m <= 0 || !idCategoriaGasto) return;
    setCargandoConsejo(true);
    setMostrandoConsejo(true);
    if (consejoIA) return;
    consejoIaService.obtenerConsejoPrevio(m, parseInt(idCategoriaGasto, 10))
      .then((r) => {
        setConsejoIA(r.consejo);
        setGeneradoConIa(r.generado_con_ia);
      })
      .catch(() => {
        setConsejoIA(null);
        setGeneradoConIa(false);
      })
      .finally(() => setCargandoConsejo(false));
  };

  const handleCerrarConsejo = () => {
    setMostrandoConsejo(false);
    setConsejoIA(null);
    setGeneradoConIa(false);
    setCargandoConsejo(false);
  };

  return {
    consejoIA,
    generadoConIa,
    cargandoConsejo,
    mostrandoConsejo,
    handleVerConsejo,
    handleCerrarConsejo,
  };
};
