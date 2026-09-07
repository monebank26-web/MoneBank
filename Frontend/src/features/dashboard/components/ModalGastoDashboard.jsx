import React from 'react';
import Modal from '../../../shared/components/Modal';
import { formatMoney, aNumero } from '../../../core/utils/format';
import CardTransaccionIA from './CardTransaccionIA';
import '../../../shared/styles/transacciones-modal.css';
import './ModalTransaccion.css';

const ModalGastoDashboard = ({
  open, handleClose, saldoCuenta,
  montoGasto, setMontoGasto,
  descripcionGasto, setDescripcionGasto,
  errorGasto,
  idCategoriaGasto, setIdCategoriaGasto,
  categoriasGasto,
  guardando,
  montoPreview, hayMonto, superaSaldo, porcentajeSaldo, claseImpactoSaldo,
  categoriaSeleccionada,
  limiteAsociado, usoActualLimite, usoProyectadoLimite, baseLimite, claseImpactoLimite,
  nivelVeredicto, mensajeVeredicto,
  consejoIA, generadoConIa, cargandoConsejo, mostrandoConsejo,
  puedeVerConsejo,
  handleVerConsejo, handleCerrarConsejo, handleGasto,
}) => (
  <Modal open={open} onClose={handleClose} title="Registrar gasto" className={mostrandoConsejo ? 'modal-gasto-expandido' : ''}>
    <div className={`formulario-gasto__layout ${mostrandoConsejo ? 'formulario-gasto__layout--con-consejo' : ''}`}>
      <div className="formulario-gasto__campos">
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
                  <span>Quedarían <strong>{formatMoney(aNumero(saldoCuenta) - montoPreview)}</strong></span>
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
                  <span>Límite {limiteAsociado.nombre} · {limiteAsociado.periodo}</span>
                  <span>{usoActualLimite}% → <strong>{usoProyectadoLimite}%</strong></span>
                </div>
                <div className="barra-impacto-gasto barra-impacto-gasto--proyectada">
                  <div className="marca-uso-actual" style={{ left: `${Math.min(usoActualLimite, 100)}%` }} />
                  <div
                    className={`relleno-impacto-gasto relleno-impacto-gasto--${claseImpactoLimite}`}
                    style={{ width: `${Math.min(Math.max(usoProyectadoLimite, 4), 100)}%` }}
                  />
                </div>
                {usoProyectadoLimite >= 100 ? (
                  <p className="nota-impacto-gasto nota-impacto-gasto--peligro">
                    Superarías tu límite por {formatMoney(aNumero(limiteAsociado.gasto_actual) + montoPreview - baseLimite)}.
                  </p>
                ) : usoProyectadoLimite >= 70 ? (
                  <p className="nota-impacto-gasto">Quedarías cerca del tope de este límite.</p>
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
        {mostrandoConsejo && (
          <div className="formulario-gasto__consejo">
            <p className="formulario-gasto__consejo-titulo">Consejo IA</p>
            <CardTransaccionIA
              consejo={consejoIA}
              generadoConIa={generadoConIa}
              cargandoConsejo={cargandoConsejo}
            />
            <button className="boton-cerrar-consejo" onClick={handleCerrarConsejo}>
              Cerrar sugerencia
            </button>
          </div>
        )}
        {puedeVerConsejo && !mostrandoConsejo && (
          <button className="boton-secundario" onClick={handleVerConsejo}>
            Ver cómo afecta este gasto
          </button>
        )}
        <button className="boton-principal" onClick={handleGasto} disabled={superaSaldo || guardando}>
          {guardando ? 'Registrando...' : 'Registrar gasto'}
        </button>
      </div>
      {mostrandoConsejo && (
        <div className="formulario-gasto__pc-consejo">
          <div className="formulario-gasto__consejo">
            <p className="formulario-gasto__consejo-titulo">Consejo IA</p>
            <CardTransaccionIA
              consejo={consejoIA}
              generadoConIa={generadoConIa}
              cargandoConsejo={cargandoConsejo}
            />
            <button className="boton-cerrar-consejo" onClick={handleCerrarConsejo}>
              Cerrar sugerencia
            </button>
          </div>
        </div>
      )}
    </div>
  </Modal>
);

export default ModalGastoDashboard;
