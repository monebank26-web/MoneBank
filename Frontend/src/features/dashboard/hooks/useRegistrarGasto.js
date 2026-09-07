import { useState, useEffect } from 'react';
import { transaccionesService } from '../../transacciones/services/transaccionesService';
import { calcularPreviewGasto } from '../helpers/calculoGasto';
import { useConsejoIA } from './useConsejoIA';

export const useRegistrarGasto = ({ open, onClose, saldoCuenta, limites }) => {
  const [montoGasto, setMontoGasto] = useState('');
  const [descripcionGasto, setDescripcionGasto] = useState('');
  const [errorGasto, setErrorGasto] = useState('');
  const [categoriasGasto, setCategoriasGasto] = useState([]);
  const [idCategoriaGasto, setIdCategoriaGasto] = useState('');
  const [cuentaId, setCuentaId] = useState(null);
  const [guardando, setGuardando] = useState(false);

  const {
    consejoIA, generadoConIa, cargandoConsejo, mostrandoConsejo,
    handleVerConsejo, handleCerrarConsejo,
  } = useConsejoIA({ montoGasto, idCategoriaGasto });

  useEffect(() => {
    if (!open || categoriasGasto.length > 0) return;
    transaccionesService.listarCategorias()
      .then((data) => setCategoriasGasto(
        (Array.isArray(data) ? data : []).filter((c) => c.tipo_categoria === 'GASTO')
      ))
      .catch(() => {});
  }, [open, categoriasGasto.length]);

  useEffect(() => {
    if (!open) return;
    import('../../auth/services/authService').then(({ authService }) =>
      authService.obtenerSaldo().then(({ id_cuenta }) => setCuentaId(id_cuenta)).catch(() => {})
    );
  }, [open]);

  const {
    montoPreview, hayMonto, superaSaldo, porcentajeSaldo, claseImpactoSaldo,
    categoriaSeleccionada, limiteAsociado,
    usoActualLimite, baseLimite, usoProyectadoLimite, claseImpactoLimite,
    nivelVeredicto, mensajeVeredicto,
  } = calcularPreviewGasto({ montoGasto, saldoCuenta, idCategoriaGasto, categoriasGasto, limites });

  const handleGasto = async () => {
    const m = parseFloat(montoGasto);
    if (!m || m <= 0) { setErrorGasto('Ingresa un monto válido.'); return; }
    if (!idCategoriaGasto) { setErrorGasto('Selecciona una categoría.'); return; }
    if (!cuentaId) { setErrorGasto('No se encontró tu cuenta.'); return; }
    setGuardando(true);
    try {
      await transaccionesService.registrarGasto({
        monto: m,
        descripcion: descripcionGasto.trim() || null,
        id_cuenta: cuentaId,
        id_categoria: parseInt(idCategoriaGasto, 10),
      });
      limpiar();
      onClose();
    } catch (err) {
      setErrorGasto(err.message);
    } finally {
      setGuardando(false);
    }
  };

  const limpiar = () => {
    setMontoGasto('');
    setDescripcionGasto('');
    setIdCategoriaGasto('');
    setErrorGasto('');
    handleCerrarConsejo();
  };

  const handleClose = () => {
    limpiar();
    onClose();
  };

  return {
    montoGasto, setMontoGasto,
    descripcionGasto, setDescripcionGasto,
    errorGasto,
    idCategoriaGasto, setIdCategoriaGasto,
    categoriasGasto,
    guardando,
    saldoCuenta,
    montoPreview, hayMonto, superaSaldo, porcentajeSaldo, claseImpactoSaldo,
    categoriaSeleccionada,
    limiteAsociado, usoActualLimite, usoProyectadoLimite, baseLimite, claseImpactoLimite,
    nivelVeredicto, mensajeVeredicto,
    consejoIA, generadoConIa, cargandoConsejo, mostrandoConsejo,
    puedeVerConsejo: hayMonto && !!idCategoriaGasto && !superaSaldo,
    handleVerConsejo, handleCerrarConsejo, handleGasto, handleClose,
  };
};
