import { useEffect, useRef, useState } from 'react';
import { authService } from '../../auth/services/authService';

const validarContrasenaNueva = (password) => {
  if (password.length < 8) {
    return 'La nueva contraseña debe tener al menos 8 caracteres.';
  }
  if (!/[A-Z]/.test(password)) {
    return 'La nueva contraseña debe contener al menos una letra mayúscula.';
  }
  if (!/[a-z]/.test(password)) {
    return 'La nueva contraseña debe contener al menos una letra minúscula.';
  }
  if (!/\d/.test(password)) {
    return 'La nueva contraseña debe contener al menos un número.';
  }
  if (!/[!@#$%^&*(),.?":{}|<>_\-]/.test(password)) {
    return 'La nueva contraseña debe contener al menos un carácter especial.';
  }
  return '';
};

export const useCambiarPassword = () => {
  const [modalPassword, setModalPassword] = useState(false);
  const [formPassword, setFormPassword] = useState({ actual: '', nueva: '', confirmar: '' });
  const [errorPassword, setErrorPassword] = useState('');
  const [exitoPassword, setExitoPassword] = useState('');
  const [cargandoPassword, setCargandoPassword] = useState(false);
  const temporizadorCierre = useRef(null);

  useEffect(() => () => clearTimeout(temporizadorCierre.current), []);

  const handleChangePassword = (e) => {
    setErrorPassword('');
    setExitoPassword('');
    setFormPassword({ ...formPassword, [e.target.name]: e.target.value });
  };

  const handleCerrarModalPassword = () => {
    clearTimeout(temporizadorCierre.current);
    setModalPassword(false);
    setFormPassword({ actual: '', nueva: '', confirmar: '' });
    setErrorPassword('');
    setExitoPassword('');
  };

  const handleGuardarPassword = async (e) => {
    e.preventDefault();
    setErrorPassword('');
    setExitoPassword('');

    if (!formPassword.actual || !formPassword.nueva || !formPassword.confirmar) {
      setErrorPassword('Completa todos los campos.');
      return;
    }

    const errorContrasena = validarContrasenaNueva(formPassword.nueva);
    if (errorContrasena) {
      setErrorPassword(errorContrasena);
      return;
    }

    if (formPassword.nueva !== formPassword.confirmar) {
      setErrorPassword('Las contraseñas nuevas no coinciden.');
      return;
    }

    setCargandoPassword(true);
    try {
      await authService.cambiarPassword(formPassword.actual, formPassword.nueva);
      setExitoPassword('Contraseña actualizada correctamente.');
      temporizadorCierre.current = setTimeout(() => {
        handleCerrarModalPassword();
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
