import { useState } from 'react';
import { authService } from '../../auth/services/authService';
import { esCorreoDuplicado } from '../utils/usuariosAdmin';

export const useAccionesUsuarioAdmin = ({ recargar }) => {
  const [usuarioSeleccionado, setUsuarioSeleccionado] = useState(null);
  const [modalDetalleAbierto, setModalDetalleAbierto] = useState(false);
  const [modalEditarAbierto, setModalEditarAbierto] = useState(false);
  const [modalEliminarAbierto, setModalEliminarAbierto] = useState(false);
  const [modalBloquearAbierto, setModalBloquearAbierto] = useState(false);
  const [formularioEdicion, setFormularioEdicion] = useState({});
  const [motivoBloqueo, setMotivoBloqueo] = useState('');
  const [errorEdicion, setErrorEdicion] = useState('');
  const [guardando, setGuardando] = useState(false);
  const [mensaje, setMensaje] = useState('');

  const mostrarMensaje = (texto) => {
    setMensaje(texto);
    setTimeout(() => setMensaje(''), 3000);
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
  // HU-0037 (Bloqueo Temporal de Cuentas): se conservan las acciones y los
  // modales para reactivarlos cuando llegue su backend. Por ahora la fila de
  // usuarios no ofrece estos botones.
  // ---------------------------------------------------------------------
  const abrirEliminar = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setModalEliminarAbierto(true);
  };

  const abrirBloquear = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setMotivoBloqueo('');
    setModalBloquearAbierto(true);
  };

  const confirmarBloqueo = async () => {
    if (!usuarioSeleccionado) return;

    if (!motivoBloqueo.trim()) {
      mostrarMensaje('Escribe el motivo del bloqueo');
      return;
    }

    try {
      await authService.bloquearUsuario(usuarioSeleccionado.id, motivoBloqueo.trim());
      setModalBloquearAbierto(false);
      mostrarMensaje('Usuario bloqueado correctamente');
      recargar();
    } catch (err) {
      mostrarMensaje('No se pudo bloquear el usuario');
    }
  };

  const eliminarUsuario = async () => {
    if (!usuarioSeleccionado) return;

    try {
      await authService.eliminarUsuario(usuarioSeleccionado.id);
      setModalEliminarAbierto(false);
      mostrarMensaje('Usuario eliminado correctamente');
      recargar();
    } catch {
      mostrarMensaje('No se pudo eliminar el usuario');
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
    formularioEdicion,
    setFormularioEdicion,
    motivoBloqueo,
    setMotivoBloqueo,
    errorEdicion,
    guardando,
    mensaje,
    abrirDetalle,
    abrirEditar,
    cerrarEditar,
    guardarEdicion,
    abrirEliminar,
    eliminarUsuario,
    abrirBloquear,
    confirmarBloqueo,
  };
};
