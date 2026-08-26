import { useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';

export const useCambiarPassword = () => {
  const { user } = useAuth();

  const [modalPassword, setModalPassword] = useState(false);
  const [formPassword, setFormPassword] = useState({ actual: '', nueva: '', confirmar: '' });
  const [errorPassword, setErrorPassword] = useState('');
  const [exitoPassword, setExitoPassword] = useState('');
  const [cargandoPassword, setCargandoPassword] = useState(false);

  const handleChangePassword = (e) => {
    setFormPassword({ ...formPassword, [e.target.name]: e.target.value });
  };

  const handleCerrarModalPassword = () => {
    setModalPassword(false);
    setFormPassword({ actual: '', nueva: '', confirmar: '' });
    setErrorPassword('');
  };

  const handleGuardarPassword = async (e) => {
    e.preventDefault();
    setErrorPassword('');

    if (!formPassword.actual || !formPassword.nueva || !formPassword.confirmar) {
      setErrorPassword('Completa todos los campos.');
      return;
    }
    if (formPassword.nueva.length < 4) {
      setErrorPassword('La nueva contraseña debe tener al menos 4 caracteres.');
      return;
    }
    if (formPassword.nueva !== formPassword.confirmar) {
      setErrorPassword('Las contraseñas nuevas no coinciden.');
      return;
    }

    setCargandoPassword(true);
    try {
      authService.cambiarPassword(user.id, formPassword.actual, formPassword.nueva);
      setExitoPassword('Contraseña actualizada correctamente.');
      setTimeout(() => {
        handleCerrarModalPassword();
        setExitoPassword('');
      }, 1200);
    } catch (err) {
      setErrorPassword(err.message);
    } finally {
      setCargandoPassword(false);
    }
  };

  return {
    modalPassword,
    setModalPassword,
    formPassword,
    errorPassword,
    exitoPassword,
    cargandoPassword,
    handleChangePassword,
    handleCerrarModalPassword,
    handleGuardarPassword,
  };
};
