import { useState } from 'react';
import { authService } from '../../auth/services/authService';
import {
  CODIGO_CUENTA_NO_BLOQUEADA,
  LONGITUD_MAXIMA_MOTIVO_BLOQUEO,
  LONGITUD_MINIMA_MOTIVO_BLOQUEO,
  accionCuentaAdmin,
  esCorreoDuplicado,
  mensajeErrorBloqueo,
  mensajeErrorDesactivacion,
  mensajeErrorDesbloqueo,
  mensajeExitoDesbloqueo,
  motivoBloqueoValido,
} from '../utils/usuariosAdmin';

export const useAccionesUsuarioAdmin = ({ recargar }) => {
  const [usuarioSeleccionado, setUsuarioSeleccionado] = useState(null);
  const [modalDetalleAbierto, setModalDetalleAbierto] = useState(false);
  const [modalEditarAbierto, setModalEditarAbierto] = useState(false);
  const [modalEliminarAbierto, setModalEliminarAbierto] = useState(false);
  const [modalBloquearAbierto, setModalBloquearAbierto] = useState(false);
  const [modalDesbloquearAbierto, setModalDesbloquearAbierto] = useState(false);
  const [formularioEdicion, setFormularioEdicion] = useState({});
  const [motivoBloqueo, setMotivoBloqueo] = useState('');
  const [errorEdicion, setErrorEdicion] = useState('');
  const [errorBloqueo, setErrorBloqueo] = useState('');
  const [errorEliminar, setErrorEliminar] = useState('');
  const [errorDesbloquear, setErrorDesbloquear] = useState('');
  const [guardando, setGuardando] = useState(false);
  const [bloqueando, setBloqueando] = useState(false);
  const [desactivando, setDesactivando] = useState(false);
  const [desbloqueando, setDesbloqueando] = useState(false);
  const [mensaje, setMensaje] = useState('');
  const [mensajeEsError, setMensajeEsError] = useState(false);

  const mostrarMensaje = (texto, tipo = 'exito') => {
    setMensaje(texto);
    setMensajeEsError(tipo === 'error');
    setTimeout(() => {
      setMensaje('');
      setMensajeEsError(false);
    }, 3000);
  };

  const abrirDetalle = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setModalDetalleAbierto(true);
  };

  const abrirEditar = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setFormularioEdicion({
      nombres: usuario.nombres || '',
      apellidos: usuario.apellidos || '',
      email: usuario.email || '',
    });
    setErrorEdicion('');
    setModalEditarAbierto(true);
  };

  const cerrarEditar = () => {
    setModalEditarAbierto(false);
    setErrorEdicion('');
  };

  const guardarEdicion = async () => {
    if (guardando || !usuarioSeleccionado) return;

    setGuardando(true);
    setErrorEdicion('');

    try {
      await authService.actualizarUsuario(usuarioSeleccionado.id, {
        nombres: formularioEdicion.nombres,
        apellidos: formularioEdicion.apellidos,
        email: formularioEdicion.email,
      });

      setModalEditarAbierto(false);
      mostrarMensaje('Usuario actualizado correctamente');
      recargar();
    } catch (err) {
      // El correo repetido se avisa dentro del modal, sin cerrarlo,
      // para que el administrador corrija el dato sin volver a escribirlo.
      setErrorEdicion(
        esCorreoDuplicado(err)
          ? 'Ese correo ya está registrado. Usa otro correo.'
          : 'No se pudo actualizar el usuario. Inténtalo de nuevo.'
      );
    } finally {
      setGuardando(false);
    }
  };

  // ---------------------------------------------------------------------
  // HU-0037 (Bloqueo y desactivación de cuentas): las acciones se concentran
  // en el modal de detalle para no saturar la fila del listado.
  // ---------------------------------------------------------------------
  const abrirEliminar = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setErrorEliminar('');
    setModalEliminarAbierto(true);
  };

  const abrirBloquear = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setMotivoBloqueo('');
    setErrorBloqueo('');
    setModalBloquearAbierto(true);
  };

  const cambiarMotivoBloqueo = (valor) => {
    setMotivoBloqueo(valor);
    if (errorBloqueo) setErrorBloqueo('');
  };

  const confirmarBloqueo = async () => {
    if (bloqueando || !usuarioSeleccionado) return;

    if (!motivoBloqueoValido(motivoBloqueo)) {
      const longitud = motivoBloqueo.trim().length;

      setErrorBloqueo(
        longitud > LONGITUD_MAXIMA_MOTIVO_BLOQUEO
          ? `El motivo no puede superar ${LONGITUD_MAXIMA_MOTIVO_BLOQUEO} caracteres.`
          : `Escribe un motivo de al menos ${LONGITUD_MINIMA_MOTIVO_BLOQUEO} caracteres.`
      );
      return;
    }

    setBloqueando(true);
    setErrorBloqueo('');

    try {
      await authService.bloquearUsuario(usuarioSeleccionado.id, motivoBloqueo.trim());
      setModalBloquearAbierto(false);
      setMotivoBloqueo('');
      mostrarMensaje('Cuenta bloqueada correctamente');
      recargar();
    } catch (err) {
      setErrorBloqueo(mensajeErrorBloqueo(err));
      if (err?.status === 404 || err?.status === 409) recargar();
    } finally {
      setBloqueando(false);
    }
  };

  // ---------------------------------------------------------------------
  // HU-0038 (Desbloqueo y reactivación de cuentas): una sola acción cubre
  // el bloqueo explícito, el bloqueo temporal y la cuenta inactiva.
  // ---------------------------------------------------------------------
  const abrirDesbloquear = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setErrorDesbloquear('');
    setModalDesbloquearAbierto(true);
  };

  const cerrarDesbloquear = () => {
    if (desbloqueando) return;

    setModalDesbloquearAbierto(false);
    setErrorDesbloquear('');
  };

  const confirmarDesbloqueo = async () => {
    if (desbloqueando || !usuarioSeleccionado) return;

    const accion = accionCuentaAdmin(usuarioSeleccionado);
    if (!accion) {
      setErrorDesbloquear(mensajeErrorDesbloqueo());
      return;
    }

    setDesbloqueando(true);
    setErrorDesbloquear('');

    try {
      await authService.desbloquearUsuario(usuarioSeleccionado.id);
      setModalDesbloquearAbierto(false);
      setModalDetalleAbierto(false);
      mostrarMensaje(mensajeExitoDesbloqueo(accion));
      recargar();
    } catch (err) {
      if (err?.code === CODIGO_CUENTA_NO_BLOQUEADA) {
        setModalDesbloquearAbierto(false);
        setModalDetalleAbierto(false);
        mostrarMensaje(mensajeErrorDesbloqueo(err), 'error');
        recargar();
      } else {
        setErrorDesbloquear(mensajeErrorDesbloqueo(err));
      }
    } finally {
      setDesbloqueando(false);
    }
  };

  const eliminarUsuario = async () => {
    if (desactivando || !usuarioSeleccionado) return;

    setDesactivando(true);
    setErrorEliminar('');

    try {
      await authService.eliminarUsuario(usuarioSeleccionado.id);
      setModalEliminarAbierto(false);
      mostrarMensaje('Usuario desactivado correctamente');
      recargar();
    } catch (err) {
      setErrorEliminar(mensajeErrorDesactivacion(err));
      if (err?.status === 404 || err?.status === 409) recargar();
    } finally {
      setDesactivando(false);
    }
  };

  return {
    usuarioSeleccionado,
    modalDetalleAbierto,
    setModalDetalleAbierto,
    modalEditarAbierto,
    modalEliminarAbierto,
    setModalEliminarAbierto,
    modalBloquearAbierto,
    setModalBloquearAbierto,
    modalDesbloquearAbierto,
    formularioEdicion,
    setFormularioEdicion,
    motivoBloqueo,
    setMotivoBloqueo,
    errorEdicion,
    errorBloqueo,
    errorEliminar,
    errorDesbloquear,
    guardando,
    bloqueando,
    desactivando,
    desbloqueando,
    mensaje,
    mensajeEsError,
    abrirDetalle,
    abrirEditar,
    cerrarEditar,
    guardarEdicion,
    abrirEliminar,
    eliminarUsuario,
    abrirBloquear,
    cambiarMotivoBloqueo,
    confirmarBloqueo,
    abrirDesbloquear,
    cerrarDesbloquear,
    confirmarDesbloqueo,
  };
};
