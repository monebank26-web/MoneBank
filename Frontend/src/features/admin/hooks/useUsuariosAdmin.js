import { useCallback, useEffect, useRef, useState } from 'react';
import { authService } from '../../auth/services/authService';
import { POR_PAGINA, calcularTotalPaginas } from '../utils/usuariosAdmin';

// HU-0036: la lista se filtra y se pagina en el servidor. Los cambios de
// filtro vuelven a la página 1 y la búsqueda espera 300 ms (debounce).
export const useUsuariosAdmin = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [total, setTotal] = useState(0);
  const [pagina, setPagina] = useState(1);
  const [busqueda, setBusqueda] = useState('');
  const [buscar, setBuscar] = useState('');
  const [idRol, setIdRol] = useState('');
  const [estado, setEstado] = useState('');
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');

  // Contador de peticiones: si una respuesta llega cuando ya se lanzó otra,
  // se descarta para no pintar resultados viejos.
  const ultimaPeticion = useRef(0);

  useEffect(() => {
    const timeout = setTimeout(() => setBuscar(busqueda.trim()), 300);

    return () => clearTimeout(timeout);
  }, [busqueda]);

  useEffect(() => {
    setPagina(1);
  }, [buscar, idRol, estado]);

  const cargar = useCallback(async () => {
    const peticion = ultimaPeticion.current + 1;
    ultimaPeticion.current = peticion;

    setCargando(true);
    setError('');

    try {
      const data = await authService.obtenerTodosLosUsuarios({
        buscar: buscar || undefined,
        estado: estado || undefined,
        id_rol: idRol || undefined,
        pagina,
        por_pagina: POR_PAGINA,
      });

      if (ultimaPeticion.current !== peticion) return;

      const totalPaginas = calcularTotalPaginas(data.total, POR_PAGINA);

      setUsuarios(data.items);
      setTotal(data.total);
      setPagina(Math.min(data.pagina, totalPaginas));
    } catch (err) {
      if (ultimaPeticion.current !== peticion) return;

      setUsuarios([]);
      setTotal(0);
      setError('No se pudieron cargar los usuarios.');
    } finally {
      if (ultimaPeticion.current === peticion) setCargando(false);
    }
  }, [buscar, idRol, estado, pagina]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const limpiarFiltros = () => {
    setBusqueda('');
    setBuscar('');
    setIdRol('');
    setEstado('');
  };

  return {
    usuarios,
    total,
    pagina,
    porPagina: POR_PAGINA,
    totalPaginas: calcularTotalPaginas(total, POR_PAGINA),
    busqueda,
    setBusqueda,
    idRol,
    setIdRol,
    estado,
    setEstado,
    cargando,
    error,
    setPagina,
    recargar: cargar,
    limpiarFiltros,
  };
};
