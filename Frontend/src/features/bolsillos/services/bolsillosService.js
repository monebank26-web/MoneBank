// features/bolsillos/services/bolsillosService.js
import { STORAGE_KEYS } from '../../../core/constants';

const getBolsillos = () => {
  const data = localStorage.getItem(STORAGE_KEYS.BOLSILLOS);
  return data ? JSON.parse(data) : [];
};

const saveBolsillos = (bolsillos) => {
  localStorage.setItem(STORAGE_KEYS.BOLSILLOS, JSON.stringify(bolsillos));
};

const getTransacciones = () => {
  const data = localStorage.getItem(STORAGE_KEYS.TRANSACCIONES);
  return data ? JSON.parse(data) : [];
};

const saveTransacciones = (transacciones) => {
  localStorage.setItem(STORAGE_KEYS.TRANSACCIONES, JSON.stringify(transacciones));
};

export const bolsillosService = {
  listar: async (userId) => {
    const todos = getBolsillos();
    return todos.filter((b) => b.userId === userId);
  },

  crear: async ({ nombre, descripcion, color, montoInicial, userId }) => {
  const bolsillos = getBolsillos();
  const nuevo = {
    id: Date.now().toString(),
    nombre,
    descripcion: descripcion || '',
    color: color || '#c9a84c',
    saldo: parseFloat(montoInicial) || 0,
    userId,
    createdAt: new Date().toISOString(),
  };
  saveBolsillos([...bolsillos, nuevo]);
  return nuevo;
},
  obtener: async (id, userId) => {
    const bolsillos = getBolsillos();
    const bolsillo = bolsillos.find((b) => b.id === id && b.userId === userId);
    if (!bolsillo) throw new Error('Bolsillo no encontrado.');
    return bolsillo;
  },

  eliminar: async (id, userId) => {
    const bolsillos = getBolsillos();
    const actualizado = bolsillos.filter((b) => !(b.id === id && b.userId === userId));
    saveBolsillos(actualizado);
  },

  transferir: async ({ origenId, destinoId, monto, descripcion, userId }) => {
    const bolsillos = getBolsillos();
    const origen = bolsillos.find((b) => b.id === origenId && b.userId === userId);
    const destino = bolsillos.find((b) => b.id === destinoId && b.userId === userId);

    if (!origen) throw new Error('Bolsillo origen no encontrado.');
    if (!destino) throw new Error('Bolsillo destino no encontrado.');
    if (origen.saldo < monto) throw new Error('Saldo insuficiente en el bolsillo origen.');
    if (monto <= 0) throw new Error('El monto debe ser mayor a 0.');

    origen.saldo -= monto;
    destino.saldo += monto;

    saveBolsillos(bolsillos);

    // Registrar transacción
    const transacciones = getTransacciones();
    const nuevaTx = {
      id: Date.now().toString(),
      tipo: 'transferencia',
      origenId,
      destinoId,
      origenNombre: origen.nombre,
      destinoNombre: destino.nombre,
      monto,
      descripcion: descripcion || '',
      userId,
      fecha: new Date().toISOString(),
    };
    saveTransacciones([nuevaTx, ...transacciones]);

    return { origen, destino, transaccion: nuevaTx };
  },

  depositar: async ({ bolsilloId, monto, descripcion, userId }) => {
    const bolsillos = getBolsillos();
    const bolsillo = bolsillos.find((b) => b.id === bolsilloId && b.userId === userId);
    if (!bolsillo) throw new Error('Bolsillo no encontrado.');
    if (monto <= 0) throw new Error('El monto debe ser mayor a 0.');

    bolsillo.saldo += monto;
    saveBolsillos(bolsillos);

    const transacciones = getTransacciones();
    const nuevaTx = {
      id: Date.now().toString(),
      tipo: 'deposito',
      destinoId: bolsilloId,
      destinoNombre: bolsillo.nombre,
      monto,
      descripcion: descripcion || 'Depósito',
      userId,
      fecha: new Date().toISOString(),
    };
    saveTransacciones([nuevaTx, ...transacciones]);

    return { bolsillo, transaccion: nuevaTx };
  },

  historialTransacciones: async (userId, bolsilloId = null) => {
    const transacciones = getTransacciones();
    let filtradas = transacciones.filter((t) => t.userId === userId);
    if (bolsilloId) {
      filtradas = filtradas.filter(
        (t) => t.origenId === bolsilloId || t.destinoId === bolsilloId
      );
    }
    return filtradas;
  },
};
