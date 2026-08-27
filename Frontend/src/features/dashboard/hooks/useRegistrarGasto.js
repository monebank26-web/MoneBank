import { useState, useEffect } from 'react';
import { transaccionesService } from '../../transacciones/services/transaccionesService';
import { consejoIaService } from '../services/consejoIaService';

const aNumero = (v) => Number(v) || 0;

export const useRegistrarGasto = ({ open, onClose, saldoCuenta, limites }) => {
  const [montoGasto, setMontoGasto] = useState('');
  const [descripcionGasto, setDescripcionGasto] = useState('');
  const [errorGasto, setErrorGasto] = useState('');
  const [categoriasGasto, setCategoriasGasto] = useState([]);
  const [idCategoriaGasto, setIdCategoriaGasto] = useState('');
  const [cuentaId, setCuentaId] = useState(null);
  const [guardando, setGuardando] = useState(false);
  const [consejoIA, setConsejoIA] = useState(null);
  const [generadoConIa, setGeneradoConIa] = useState(false);
  const [cargandoConsejo, setCargandoConsejo] = useState(false);
  const [mostrandoConsejo, setMostrandoConsejo] = useState(false);

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

  const montoPreview = parseFloat(montoGasto);
  const hayMonto = !!montoPreview && montoPreview > 0;
  const superaSaldo = hayMonto && montoPreview > aNumero(saldoCuenta);
  const porcentajeSaldo =
    hayMonto && aNumero(saldoCuenta) > 0 ? (montoPreview / aNumero(saldoCuenta)) * 100 : 0;
  const claseImpactoSaldo = superaSaldo
    ? 'peligro'
    : porcentajeSaldo > 60
      ? 'peligro'
      : porcentajeSaldo >= 30
        ? 'alerta'
        : 'ok';

  const categoriaSeleccionada = categoriasGasto.find(
    (c) => String(c.id_categoria) === String(idCategoriaGasto)
  );
  const limiteAsociado = categoriaSeleccionada
    ? limites.find(
        (l) =>
          l.estado === 'ACTIVO' &&
          l.nombre_categoria === categoriaSeleccionada.nombre_categoria
      )
    : null;

  const usoActualLimite = limiteAsociado ? Math.round(aNumero(limiteAsociado.porcentaje_usado)) : 0;
  const baseLimite = limiteAsociado ? aNumero(limiteAsociado.monto_limite) : 0;
  const usoProyectadoLimite =
    limiteAsociado && baseLimite > 0
      ? Math.round(((aNumero(limiteAsociado.gasto_actual) + montoPreview) / baseLimite) * 100)
      : 0;
  const claseImpactoLimite = !limiteAsociado
    ? null
    : usoProyectadoLimite >= 100
      ? 'peligro'
      : usoProyectadoLimite >= 70
        ? 'alerta'
        : 'ok';

  let nivelVeredicto = null;
  let mensajeVeredicto = '';
  if (hayMonto) {
    const niveles = [claseImpactoSaldo];
    if (claseImpactoLimite) niveles.push(claseImpactoLimite);
    nivelVeredicto = niveles.includes('peligro')
      ? 'peligro'
      : niveles.includes('alerta')
        ? 'alerta'
        : 'ok';
    if (superaSaldo) {
      mensajeVeredicto = 'No puedes registrar este gasto: supera tu saldo disponible.';
    } else if (nivelVeredicto === 'alerta') {
      mensajeVeredicto =
        claseImpactoLimite === 'alerta'
          ? 'Quedarías cerca del tope de tu límite.'
          : 'Es un golpe fuerte para tu saldo. ¿Lo necesitas hoy?';
    } else if (nivelVeredicto === 'peligro') {
      mensajeVeredicto =
        claseImpactoLimite === 'peligro'
          ? 'Este gasto superaría tu límite. Mejor espera o reduce el monto.'
          : 'Golpe muy fuerte a tu saldo. Piénsalo bien.';
    } else {
      mensajeVeredicto = 'Razonable según tu saldo y tus límites.';
    }
  }

  const handleVerConsejo = () => {
    const m = parseFloat(montoGasto);
    if (!m || m <= 0 || !idCategoriaGasto) return;
    setCargandoConsejo(true);
    setMostrandoConsejo(true);
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
