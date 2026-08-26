import { useState } from 'react';
import { authService } from '../../auth/services/authService';

export const useAccionesUsuarioAdmin = ({ cargarUsuarios }) => {
  const [usuarioSeleccionado, setUsuarioSeleccionado] = useState(null);
  const [modalDetalleAbierto, setModalDetalleAbierto] = useState(false);
  const [modalEditarAbierto, setModalEditarAbierto] = useState(false);
  const [modalEliminarAbierto, setModalEliminarAbierto] = useState(false);
  const [formularioEdicion, setFormularioEdicion] = useState({});
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
    setFormularioEdicion({ nombre: usuario.nombre, email: usuario.email, saldoCuenta: usuario.saldoCuenta, rol: usuario.rol });
    setModalEditarAbierto(true);
  };

  const abrirEliminar = (usuario) => {
    setUsuarioSeleccionado(usuario);
    setModalEliminarAbierto(true);
  };

  const guardarEdicion = () => {
    authService.actualizarUsuario(usuarioSeleccionado.id, {
      nombre: formularioEdicion.nombre,
      email: formularioEdicion.email,
      saldoCuenta: parseInt(formularioEdicion.saldoCuenta, 10) || 0,
      rol: formularioEdicion.rol,
    });
    mostrarMensaje('✓ Usuario actualizado correctamente.');
    setModalEditarAbierto(false);
    cargarUsuarios();
  };

  const eliminarUsuario = () => {
    authService.eliminarUsuario(usuarioSeleccionado.id);
    mostrarMensaje('✓ Usuario eliminado correctamente.');
    setModalEliminarAbierto(false);
    cargarUsuarios();
  };

  return {
    usuarioSeleccionado,
    modalDetalleAbierto,
    setModalDetalleAbierto,
    modalEditarAbierto,
    setModalEditarAbierto,
    modalEliminarAbierto,
    setModalEliminarAbierto,
    formularioEdicion,
    setFormularioEdicion,
    mensaje,
    abrirDetalle,
    abrirEditar,
    abrirEliminar,
    guardarEdicion,
    eliminarUsuario,
  };
};
