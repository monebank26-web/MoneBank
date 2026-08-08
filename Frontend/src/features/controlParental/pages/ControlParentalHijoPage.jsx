import React, { useState, useEffect } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';
import './ControlParentalPage.css';

const ControlParentalHijoPage = () => {
  const { user, login } = useAuth();
  const [usuarioVinculado, setUsuarioVinculado] = useState(null);
  const [correoVincular, setCorreoVincular] = useState('');
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');

  useEffect(() => {
    if (user?.cuentaVinculada) {
      const vinculado = authService.obtenerUsuarioPorId(user.cuentaVinculada);
      setUsuarioVinculado(vinculado);
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
    if (usuarioObjetivo.rol !== 'padre') {
      setError('El correo ingresado no pertenece a una cuenta de padre/madre.');
      return;
    }

    authService.vincularCuentas(usuarioObjetivo.id, user.id);

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
    setExito('Cuentas desvinculadas correctamente.');
  };

  return (
    <div className="pagina-control-parental">
      <div className="encabezado-parental">
        <h1 className="titulo-parental">Control parental</h1>
        <p className="subtitulo-parental">
          {user?.esMenor
            ? 'Como eres menor de edad, tu cuenta debe estar vinculada a la de tu padre o madre.'
            : 'Aquí puedes vincularte a la cuenta de tus padres.'}
        </p>
      </div>

      {exito && <div className="mensaje-exito-parental">{exito}</div>}
      {error && <div className="mensaje-error-parental">{error}</div>}

      {!usuarioVinculado && (
        <div className="tarjeta-vincular">
          <div className="icono-vincular">🧒</div>
          <h2 className="titulo-vincular">Vincúlate a la cuenta de tus padres</h2>
          <p className="descripcion-vincular">
            Ingresa el correo de la cuenta de tu padre o madre para vincularte.
          </p>
          <div className="campo-vincular">
            <input
              className="campo-entrada-parental"
              type="email"
              placeholder="Correo del padre/madre"
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
        <div className="tarjeta-vinculado">
          <div className="encabezado-vinculado">
            <div className="avatar-vinculado">
              {usuarioVinculado.nombre.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="nombre-vinculado">{usuarioVinculado.nombre}</p>
              <p className="correo-vinculado">{usuarioVinculado.email}</p>
              <span className="etiqueta-vinculado">👨‍👧 Tu padre/madre</span>
            </div>
            <button className="boton-desvincular" onClick={handleDesvincular}>
              Desvincular
            </button>
          </div>

          <div className="seccion-parental">
            <p className="info-hijo-parental">
              Tu cuenta está vinculada al padre o madre indicado. Ellos pueden ver tu saldo y tus movimientos.
              Si quieres desvincularte, puedes hacerlo en cualquier momento con el botón de arriba.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ControlParentalHijoPage;
