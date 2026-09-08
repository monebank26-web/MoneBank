import { useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../../auth/services/authService';

const obtenerNombreCompleto = (usuario) => {
  if (usuario?.nombre) {
    return usuario.nombre;
  }

  return `${usuario?.nombres || ''} ${
    usuario?.apellidos || ''
  }`.trim();
};

const obtenerCorreo = (usuario) => {
  return usuario?.email || usuario?.correo || '';
};

export const useDatosPersonales = () => {
  const { user, login } = useAuth();

  const [editando, setEditando] = useState(false);

  const [formDatos, setFormDatos] = useState({
    nombre: obtenerNombreCompleto(user),
    email: obtenerCorreo(user),
  });

  const [errorDatos, setErrorDatos] = useState('');
  const [exitoDatos, setExitoDatos] = useState('');
  const [cargandoDatos, setCargandoDatos] = useState(false);

  const handleChangeDatos = (event) => {
    const { name, value } = event.target;

    setFormDatos((datosAnteriores) => ({
      ...datosAnteriores,
      [name]: value,
    }));

    setErrorDatos('');
    setExitoDatos('');
  };

  const handleGuardarDatos = async (event) => {
    event.preventDefault();

    setErrorDatos('');
    setExitoDatos('');

    const nombre = formDatos.nombre.trim();
    const email = formDatos.email.trim().toLowerCase();

    if (!nombre || !email) {
      setErrorDatos(
        'El nombre y el correo no pueden quedar vacíos.'
      );
      return;
    }

    if (!email.includes('@')) {
      setErrorDatos(
        'Ingresa un correo electrónico válido.'
      );
      return;
    }

    const usuarioId =
      user?.id ||
      user?.id_usuario ||
      user?.usuario_id;

    if (!usuarioId) {
      setErrorDatos(
        'No se pudo identificar el usuario autenticado.'
      );
      return;
    }

    setCargandoDatos(true);

    try {
      const partesNombre = nombre.split(/\s+/);

      const nombres = partesNombre.shift() || '';
      const apellidos = partesNombre.join(' ');

      const usuarioActualizado =
        await authService.actualizarUsuario(
          usuarioId,
          {
            nombres,
            apellidos,
            email,
          }
        );

      const usuarioSesionActualizado = {
        ...user,
        ...usuarioActualizado,

        id: usuarioActualizado?.id || usuarioId,
        id_usuario:
          usuarioActualizado?.id_usuario ||
          usuarioId,

        nombres:
          usuarioActualizado?.nombres ||
          nombres,

        apellidos:
          usuarioActualizado?.apellidos ||
          apellidos,

        nombre,
        email,

        fecha_creacion:
          usuarioActualizado?.fecha_creacion ||
          user?.fecha_creacion,

        access_token:
          user?.access_token ||
          usuarioActualizado?.access_token,
      };

      login(usuarioSesionActualizado);

      setFormDatos({
        nombre,
        email,
      });

      setEditando(false);
      setExitoDatos(
        'Tus datos se actualizaron correctamente.'
      );
    } catch (error) {
      const mensaje =
        error?.message ||
        'No se pudieron actualizar tus datos.';

      if (
        mensaje.toLowerCase().includes('correo') ||
        mensaje.toLowerCase().includes('email') ||
        mensaje.toLowerCase().includes('exist')
      ) {
        setErrorDatos(
          'Ese correo ya está en uso por otra cuenta.'
        );
      } else {
        setErrorDatos(mensaje);
      }
    } finally {
      setCargandoDatos(false);
    }
  };

  const handleCancelarEdicion = () => {
    setFormDatos({
      nombre: obtenerNombreCompleto(user),
      email: obtenerCorreo(user),
    });

    setErrorDatos('');
    setExitoDatos('');
    setEditando(false);
  };

  return {
    user,
    editando,
    setEditando,
    formDatos,
    errorDatos,
    exitoDatos,
    cargandoDatos,
    handleChangeDatos,
    handleGuardarDatos,
    handleCancelarEdicion,
  };
};
