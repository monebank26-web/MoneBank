import { useState, useEffect } from 'react';
import { authService } from '../../auth/services/authService';

export const useUsuariosAdmin = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [filtroRol, setFiltroRol] = useState('todos');

  const cargarUsuarios = () => {
    const todos = authService.obtenerTodosLosUsuarios();
    setUsuarios(todos);
  };

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const usuariosFiltrados = usuarios.filter((usuario) => {
    const coincideBusqueda =
      usuario.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
      usuario.email.toLowerCase().includes(busqueda.toLowerCase());
    const coincideRol = filtroRol === 'todos' || usuario.rol === filtroRol;
    return coincideBusqueda && coincideRol;
  });

  const obtenerUsuarioVinculado = (usuario) => {
    if (!usuario.cuentaVinculada) return null;
    return usuarios.find((u) => u.id === usuario.cuentaVinculada) || null;
  };

  return {
    usuarios,
    usuariosFiltrados,
    busqueda,
    setBusqueda,
    filtroRol,
    setFiltroRol,
    cargarUsuarios,
    obtenerUsuarioVinculado,
  };
};
