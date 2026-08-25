import React, { useEffect, useState } from 'react';
import Modal from '../../../shared/components/Modal';
import { transaccionesService } from '../../transacciones/services/transaccionesService';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val);

const aNumero = (v) => Number(v) || 0;

const ModalGastoDashboard = ({ open, onClose, saldoCuenta, limites }) => {
  const [montoGasto, setMontoGasto] = useState('');
  const [descripcionGasto, setDescripcionGasto] = useState('');
  const [errorGasto, setErrorGasto] = useState('');
  const [categoriasGasto, setCategoriasGasto] = useState([]);
  const [idCategoriaGasto, setIdCategoriaGasto] = useState('');
  const [cuentaId, setCuentaId] = useState(null);
  const [guardando, setGuardando] = useState(false);

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
      const { authService } = await import('../../auth/services/authService');
      const { saldo } = await authService.obtenerSaldo();
      setMontoGasto('');
      setDescripcionGasto('');
      setIdCategoriaGasto('');
      setErrorGasto('');
      onClose(saldo);
    } catch (err) {
      setErrorGasto(err.message);
    } finally {
      setGuardando(false);
    }
  };

  const handleClose = () => {
    setMontoGasto('');
    setDescripcionGasto('');
    setIdCategoriaGasto('');
    setErrorGasto('');
    onClose();
  };

  return (
    <Modal open={open} onClose={handleClose} title="Registrar gasto">
      <div className="formulario-modal">
        <p style={{ color: 'var(--color-text-soft)', fontSize: '13px' }}>
          Saldo actual: <strong style={{ color: 'var(--color-accent)' }}>{formatMoney(saldoCuenta)}</strong>
        </p>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Monto (COP)</label>
          <input className="campo-entrada" type="number" placeholder="Ej: 50000"
            min="1" step="1" value={montoGasto}
            onChange={(e) => setMontoGasto(e.target.value)} />
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Categoría</label>
          {categoriasGasto.length === 0 ? (
            <select className="campo-entrada campo-seleccion" disabled>
              <option>Cargando categorías...</option>
            </select>
          ) : (
            <select
              className="campo-entrada campo-seleccion"
              value={idCategoriaGasto}
              onChange={(e) => setIdCategoriaGasto(e.target.value)}
            >
              <option value="">Selecciona una categoría...</option>
              {categoriasGasto.map((c) => (
                <option key={c.id_categoria} value={c.id_categoria}>
                  {c.nombre_categoria}
                </option>
              ))}
            </select>
          )}
        </div>
        <div className="grupo-campo">
          <label className="etiqueta-campo">Descripción (opcional, máx. 255)</label>
          <input className="campo-entrada" type="text" placeholder="Ej: Almuerzo"
            maxLength={255} value={descripcionGasto}
            onChange={(e) => setDescripcionGasto(e.target.value)} />
        </div>
        {hayMonto && (
          <div className="preview-gasto">
            <p className="titulo-preview-gasto">¿Cómo afecta este gasto?</p>

            {superaSaldo ? (
              <div className="impacto-gasto impacto-gasto--peligro">
                <p className="mensaje-impacto-gasto">
                  No tienes saldo suficiente: te faltan{' '}
                  <strong>{formatMoney(montoPreview - aNumero(saldoCuenta))}</strong>.
                </p>
              </div>
            ) : (
              <div className={`impacto-gasto impacto-gasto--${claseImpactoSaldo}`}>
                <div className="encabezado-impacto-gasto">
                  <span>{Math.round(porcentajeSaldo)}% de tu saldo</span>
                  <span>
                    Quedarían{' '}
                    <strong>{formatMoney(aNumero(saldoCuenta) - montoPreview)}</strong>
                  </span>
                </div>
                <div className="barra-impacto-gasto">
                  <div
                    className={`relleno-impacto-gasto relleno-impacto-gasto--${claseImpactoSaldo}`}
                    style={{ width: `${Math.min(Math.max(porcentajeSaldo, 4), 100)}%` }}
                  />
                </div>
              </div>
            )}

            {limiteAsociado && (
              <div className={`impacto-gasto impacto-gasto--${claseImpactoLimite}`}>
                <div className="encabezado-impacto-gasto">
                  <span>
                    Límite {limiteAsociado.nombre} · {limiteAsociado.periodo}
                  </span>
                  <span>
                    {usoActualLimite}% →{' '}
                    <strong>{usoProyectadoLimite}%</strong>
                  </span>
                </div>
                <div className="barra-impacto-gasto barra-impacto-gasto--proyectada">
                  <div
                    className="marca-uso-actual"
                    style={{ left: `${Math.min(usoActualLimite, 100)}%` }}
                  />
                  <div
                    className={`relleno-impacto-gasto relleno-impacto-gasto--${claseImpactoLimite}`}
                    style={{ width: `${Math.min(Math.max(usoProyectadoLimite, 4), 100)}%` }}
                  />
                </div>
                {usoProyectadoLimite >= 100 ? (
                  <p className="nota-impacto-gasto nota-impacto-gasto--peligro">
                    Superarías tu límite por{' '}
                    {formatMoney(
                      aNumero(limiteAsociado.gasto_actual) + montoPreview - baseLimite
                    )}
                    .
                  </p>
                ) : usoProyectadoLimite >= 70 ? (
                  <p className="nota-impacto-gasto">
                    Quedarías cerca del tope de este límite.
                  </p>
                ) : null}
              </div>
            )}

            <div className={`veredicto-gasto veredicto-gasto--${nivelVeredicto}`}>
              <span className="icono-veredicto-gasto">
                {nivelVeredicto === 'ok' ? '✓' : nivelVeredicto === 'alerta' ? '!' : '✕'}
              </span>
              <p>{mensajeVeredicto}</p>
            </div>
          </div>
        )}
        {errorGasto && <p className="error-formulario">{errorGasto}</p>}
        <button
          className="boton-principal"
          onClick={handleGasto}
          disabled={superaSaldo || guardando}
        >
          {guardando ? 'Registrando...' : 'Registrar gasto'}
        </button>
      </div>
    </Modal>
  );
};

export default ModalGastoDashboard;
