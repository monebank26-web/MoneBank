import React, { useState, useEffect } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';
import './ControlParentalPage.css';

const formatMoney = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', maximumFractionDigits: 0 }).format(val || 0);

const formatFecha = (iso) =>
  new Date(iso).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });

const ControlParentalPadrePage = () => {
  const { user, login } = useAuth();
  const [usuarioVinculado, setUsuarioVinculado] = useState(null);
  const [correoVincular, setCorreoVincular] = useState('');
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const [transaccionesHijo, setTransaccionesHijo] = useState([]);
  const [bolsillosHijo, setBolsillosHijo] = useState([]);

  useEffect(() => {
    if (user?.cuentaVinculada) {
      const vinculado = authService.obtenerUsuarioPorId(user.cuentaVinculada);
      setUsuarioVinculado(vinculado);

      if (vinculado) {
        const bolsillos = JSON.parse(localStorage.getItem('mb_bolsillos') || '[]')
          .filter((b) => b.userId === vinculado.id);
        setBolsillosHijo(bolsillos);

        const transacciones = JSON.parse(localStorage.getItem('mb_transacciones') || '[]')
          .filter((t) => t.userId === vinculado.id);
        setTransaccionesHijo(transacciones.slice(0, 10));
      }
    }
  }, [user]);

  const handleVincular = () => {
    setError('');
    setExito('');

    if (!correoVincular.trim()) {
      setError('Por favor ingresa un correo electrónico.');
      return;
    }

    const usuarioObjetivo = authService.obtenerUsuarioPorCorreo(correoVincular.trim());

    if (!usuarioObjetivo) {
      setError('No se encontró ningún usuario con ese correo.');
      return;
    }
    if (usuarioObjetivo.id === user.id) {
      setError('No puedes vincularte a tu propia cuenta.');
      return;
    }
    if (usuarioObjetivo.rol !== 'hijo') {
      setError('El correo ingresado no pertenece a una cuenta de hijo/hija.');
      return;
    }

    authService.vincularCuentas(user.id, usuarioObjetivo.id);

    const usuarioActualizado = authService.obtenerUsuarioPorId(user.id);
    login(usuarioActualizado);
    setUsuarioVinculado(usuarioObjetivo);
    setCorreoVincular('');
    setExito('¡Cuentas vinculadas correctamente!');
  };

  const handleDesvincular = () => {
    authService.actualizarUsuario(user.id, { cuentaVinculada: null });
    if (usuarioVinculado) {
      authService.actualizarUsuario(usuarioVinculado.id, { cuentaVinculada: null });
    }
    const usuarioActualizado = authService.obtenerUsuarioPorId(user.id);
    login(usuarioActualizado);
    setUsuarioVinculado(null);
    setBolsillosHijo([]);
    setTransaccionesHijo([]);
    setExito('Cuentas desvinculadas correctamente.');
  };

  return (
    <div className="pagina-control-parental">
      <div className="encabezado-parental">
        <h1 className="titulo-parental">Control parental</h1>
        <p className="subtitulo-parental">Aquí puedes ver y administrar la cuenta de tu hijo o hija.</p>
      </div>

      {exito && <div className="mensaje-exito-parental">{exito}</div>}
      {error && <div className="mensaje-error-parental">{error}</div>}

      {!usuarioVinculado && (
        <div className="tarjeta-vincular">
          <div className="icono-vincular">👨‍👧</div>
          <h2 className="titulo-vincular">Vincula la cuenta de tu hijo o hija</h2>
          <p className="descripcion-vincular">
            Ingresa el correo de la cuenta de tu hijo/hija para ver su actividad y saldo.
          </p>
          <div className="campo-vincular">
            <input
              className="campo-entrada-parental"
              type="email"
              placeholder="Correo del hijo/hija"
              value={correoVincular}
              onChange={(e) => setCorreoVincular(e.target.value)}
            />
            <button className="boton-vincular" onClick={handleVincular}>
              Vincular cuenta
            </button>
          </div>
        </div>
      )}

      {usuarioVinculado && (
        <>
          <div className="tarjeta-vinculado">
            <div className="encabezado-vinculado">
              <div className="avatar-vinculado">
                {usuarioVinculado.nombre.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="nombre-vinculado">{usuarioVinculado.nombre}</p>
                <p className="correo-vinculado">{usuarioVinculado.email}</p>
                <span className="etiqueta-vinculado">🧒 Tu hijo/hija</span>
              </div>
              <button className="boton-desvincular" onClick={handleDesvincular}>
                Desvincular
              </button>
            </div>

            <div className="saldo-vinculado">
              <p className="etiqueta-saldo-vinculado">Saldo en cuenta</p>
              <p className="valor-saldo-vinculado">{formatMoney(usuarioVinculado.saldoCuenta)}</p>
            </div>
          </div>

          {bolsillosHijo.length > 0 && (
            <div className="seccion-parental">
              <h3 className="titulo-seccion-parental">Bolsillos de {usuarioVinculado.nombre}</h3>
              <div className="cuadricula-bolsillos-parental">
                {bolsillosHijo.map((b) => (
                  <div key={b.id} className="bolsillo-parental" style={{ '--color-bolsillo': b.color }}>
                    <div className="punto-bolsillo-parental" />
                    <div>
                      <p className="nombre-bolsillo-parental">{b.nombre}</p>
                      <p className="saldo-bolsillo-parental">{formatMoney(b.saldo)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="seccion-parental">
            <h3 className="titulo-seccion-parental">Últimos movimientos de {usuarioVinculado.nombre}</h3>
            {transaccionesHijo.length === 0 ? (
              <p className="sin-movimientos-parental">Sin movimientos registrados aún.</p>
            ) : (
              <div className="lista-movimientos-parental">
                {transaccionesHijo.map((tx) => (
                  <div key={tx.id} className="movimiento-parental">
                    <div className={`icono-movimiento-parental icono-movimiento-parental--${tx.tipo}`}>
                      {tx.tipo === 'transferencia' ? '↔' : '↓'}
                    </div>
                    <div className="info-movimiento-parental">
                      <p className="descripcion-movimiento-parental">
                        {tx.tipo === 'transferencia'
                          ? `${tx.origenNombre} → ${tx.destinoNombre}`
                          : `Depósito en ${tx.destinoNombre}`}
                      </p>
                      <p className="fecha-movimiento-parental">{formatFecha(tx.fecha)}</p>
                    </div>
                    <p className={`monto-movimiento-parental monto-movimiento-parental--${tx.tipo}`}>
                      {tx.tipo === 'deposito' ? '+' : ''}{formatMoney(tx.monto)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default ControlParentalPadrePage;
