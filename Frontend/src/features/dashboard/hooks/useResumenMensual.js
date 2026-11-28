import { useState, useEffect, useMemo } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { transaccionesService } from '../../transacciones/services/transaccionesService';
import { aNumero } from '../../../core/utils/format';

const MESES = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'];

const extraerAnioMes = (fecha) => {
  const [anio, mes] = String(fecha).slice(0, 7).split('-').map(Number);
  return { anio, mes };
};

const calcularVariacion = (actual, anterior) =>
  anterior > 0 ? ((actual - anterior) / anterior) * 100 : null;

export const useResumenMensual = () => {
  const { user } = useAuth();
  const hoy = new Date();
  const anioActual = hoy.getFullYear();
  const mesActual = hoy.getMonth() + 1;

  const [movimientos, setMovimientos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [anio, setAnio] = useState(anioActual);

  useEffect(() => {
    if (!user) return;
    setCargando(true);
    transaccionesService
      .obtenerHistorial({ por_pagina: 100, ordenar_por: 'fecha', orden: 'desc' })
      .then((data) => setMovimientos(data.items || []))
      .catch(() => setMovimientos([]))
      .finally(() => setCargando(false));
  }, [user]);

  const sumarMes = (tipo, anioBuscado, mesBuscado) =>
    movimientos.reduce((total, m) => {
      const { anio: a, mes } = extraerAnioMes(m.fecha);
      if (m.tipo_transaccion !== tipo || a !== anioBuscado || mes !== mesBuscado) return total;
      return total + Math.abs(aNumero(m.monto));
    }, 0);

  const serie = useMemo(() => {
    const meses = MESES.map((etiqueta, i) => ({
      etiqueta,
      mes: i + 1,
      ingresos: 0,
      gastos: 0,
    }));

    movimientos.forEach((m) => {
      const { anio: a, mes } = extraerAnioMes(m.fecha);
      if (a !== anio || !mes) return;
      const monto = Math.abs(aNumero(m.monto));
      if (m.tipo_transaccion === 'INGRESO') meses[mes - 1].ingresos += monto;
      if (m.tipo_transaccion === 'GASTO') meses[mes - 1].gastos += monto;
    });

    let acumulado = 0;
    const completa = meses.map((m) => {
      acumulado += m.ingresos - m.gastos;
      return { ...m, acumulado };
    });

    return anio === anioActual ? completa.slice(0, mesActual) : completa;
  }, [movimientos, anio, anioActual, mesActual]);

  const mesPrevio = mesActual === 1 ? 12 : mesActual - 1;
  const anioPrevio = mesActual === 1 ? anioActual - 1 : anioActual;

  const ingresosMes = sumarMes('INGRESO', anioActual, mesActual);
  const gastosMes = sumarMes('GASTO', anioActual, mesActual);
  const ingresosPrevio = sumarMes('INGRESO', anioPrevio, mesPrevio);
  const gastosPrevio = sumarMes('GASTO', anioPrevio, mesPrevio);

  return {
    cargando,
    anio,
    setAnio,
    aniosDisponibles: [anioActual, anioActual - 1],
    serie,
    kpi: {
      ingresosMes,
      gastosMes,
      netoMes: ingresosMes - gastosMes,
      variacionIngresos: calcularVariacion(ingresosMes, ingresosPrevio),
      variacionGastos: calcularVariacion(gastosMes, gastosPrevio),
    },
  };
};