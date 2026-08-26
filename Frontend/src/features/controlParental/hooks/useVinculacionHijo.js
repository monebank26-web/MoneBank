import { useState, useEffect } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';

export const useVinculacionHijo = () => {
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

  return {
    usuarioVinculado,
    correoVincular,
    setCorreoVincular,
    error,
    exito,
    transaccionesHijo,
    bolsillosHijo,
    handleVincular,
    handleDesvincular,
  };
};
