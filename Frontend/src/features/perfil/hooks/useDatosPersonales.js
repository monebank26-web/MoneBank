import { useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';

export const useDatosPersonales = () => {
  const { user, login } = useAuth();

  const [editando, setEditando] = useState(false);
  const [formDatos, setFormDatos] = useState({ nombre: user?.nombre || '', email: user?.email || '' });
  const [errorDatos, setErrorDatos] = useState('');
  const [exitoDatos, setExitoDatos] = useState('');

  const handleChangeDatos = (e) => {
    setFormDatos({ ...formDatos, [e.target.name]: e.target.value });
    setExitoDatos('');
  };

  const handleGuardarDatos = (e) => {
    e.preventDefault();
    setErrorDatos('');
    setExitoDatos('');

    if (!formDatos.nombre.trim() || !formDatos.email.trim()) {
      setErrorDatos('El nombre y el correo no pueden quedar vacíos.');
      return;
    }

    // Si cambia el correo, verificar que no esté en uso por otra cuenta
    if (formDatos.email !== user.email) {
      const existente = authService.obtenerUsuarioPorCorreo(formDatos.email);
      if (existente && existente.id !== user.id) {
        setErrorDatos('Ese correo ya está en uso por otra cuenta.');
        return;
      }
    }

    authService.actualizarUsuario(user.id, {
      nombre: formDatos.nombre.trim(),
      email: formDatos.email.trim(),
    });
    login({ ...user, nombre: formDatos.nombre.trim(), email: formDatos.email.trim() });
    setEditando(false);
    setExitoDatos('Tus datos se actualizaron correctamente.');
  };

  const handleCancelarEdicion = () => {
    setFormDatos({ nombre: user?.nombre || '', email: user?.email || '' });
    setErrorDatos('');
    setEditando(false);
  };

  return {
    user,
    editando,
    setEditando,
    formDatos,
    errorDatos,
    exitoDatos,
    handleChangeDatos,
    handleGuardarDatos,
    handleCancelarEdicion,
  };
};
