import { aNumero } from '../../../core/utils/format';

export const calcularPreviewGasto = ({
  montoGasto,
  saldoCuenta,
  idCategoriaGasto,
  categoriasGasto,
  limites,
}) => {
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

  return {
    montoPreview,
    hayMonto,
    superaSaldo,
    porcentajeSaldo,
    claseImpactoSaldo,
    categoriaSeleccionada,
    limiteAsociado,
    usoActualLimite,
    baseLimite,
    usoProyectadoLimite,
    claseImpactoLimite,
    nivelVeredicto,
    mensajeVeredicto,
  };
};
