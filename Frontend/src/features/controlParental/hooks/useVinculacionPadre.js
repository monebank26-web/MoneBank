import { useState, useEffect } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';

export const useVinculacionPadre = () => {
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

  return {
    usuarioVinculado,
    correoVincular,
    setCorreoVincular,
    error,
    exito,
    handleVincular,
    handleDesvincular,
  };
};
