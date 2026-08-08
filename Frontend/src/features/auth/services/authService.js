import { STORAGE_KEYS, CORREO_ADMIN, ROLES } from '../../../core/constants';

const USERS_KEY = STORAGE_KEYS.USERS;

const obtenerUsuarios = () => {
  const datos = localStorage.getItem(USERS_KEY);
  return datos ? JSON.parse(datos) : [];
};

const guardarUsuarios = (usuarios) => {
  localStorage.setItem(USERS_KEY, JSON.stringify(usuarios));
};

export const authService = {
  register: async ({ nombre, email, password, saldoInicial, rol, esMenor }) => {
    const usuarios = obtenerUsuarios();
    const existeCorreo = usuarios.find((u) => u.email === email);
    if (existeCorreo) throw new Error('Este correo ya está registrado.');

    const rolFinal = email === CORREO_ADMIN ? ROLES.ADMIN : (rol || ROLES.NORMAL);

    const nuevoUsuario = {
      id: Date.now().toString(),
      nombre,
      email,
      password,
      saldoCuenta: parseInt(saldoInicial, 10) || 0,
      rol: rolFinal,
      esMenor: esMenor || false,
      cuentaVinculada: null, // id del padre o hijo vinculado
      createdAt: new Date().toISOString(),
    };

    guardarUsuarios([...usuarios, nuevoUsuario]);
    const { password: _, ...usuarioSeguro } = nuevoUsuario;
    return usuarioSeguro;
  },

  login: async ({ email, password }) => {
    const usuarios = obtenerUsuarios();
    const usuario = usuarios.find((u) => u.email === email && u.password === password);
    if (!usuario) throw new Error('Correo o contraseña incorrectos.');
    const { password: _, ...usuarioSeguro } = usuario;
    return usuarioSeguro;
  },

  actualizarSaldo: (userId, nuevoSaldo) => {
    const usuarios = obtenerUsuarios();
    const actualizados = usuarios.map((u) =>
      u.id === userId ? { ...u, saldoCuenta: nuevoSaldo } : u
    );
    guardarUsuarios(actualizados);

    const usuarioSesion = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER) || '{}');
    if (usuarioSesion.id === userId) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify({ ...usuarioSesion, saldoCuenta: nuevoSaldo }));
    }
  },

  obtenerTodosLosUsuarios: () => {
    return obtenerUsuarios().map(({ password: _, ...u }) => u);
  },

  eliminarUsuario: (userId) => {
    const usuarios = obtenerUsuarios();
    guardarUsuarios(usuarios.filter((u) => u.id !== userId));
  },

  actualizarUsuario: (userId, datos) => {
    const usuarios = obtenerUsuarios();
    const actualizados = usuarios.map((u) =>
      u.id === userId ? { ...u, ...datos } : u
    );
    guardarUsuarios(actualizados);
  },

  vincularCuentas: (idPadre, idHijo) => {
    const usuarios = obtenerUsuarios();
    const actualizados = usuarios.map((u) => {
      if (u.id === idPadre) return { ...u, cuentaVinculada: idHijo };
      if (u.id === idHijo) return { ...u, cuentaVinculada: idPadre };
      return u;
    });
    guardarUsuarios(actualizados);

    // Actualizar sesión si aplica
    const sesion = JSON.parse(localStorage.getItem(STORAGE_KEYS.USER) || '{}');
    if (sesion.id === idPadre) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify({ ...sesion, cuentaVinculada: idHijo }));
    } else if (sesion.id === idHijo) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify({ ...sesion, cuentaVinculada: idPadre }));
    }
  },

  obtenerUsuarioPorId: (id) => {
    const usuarios = obtenerUsuarios();
    const usuario = usuarios.find((u) => u.id === id);
    if (!usuario) return null;
    const { password: _, ...usuarioSeguro } = usuario;
    return usuarioSeguro;
  },

  obtenerUsuarioPorCorreo: (email) => {
    const usuarios = obtenerUsuarios();
    const usuario = usuarios.find((u) => u.email === email);
    if (!usuario) return null;
    const { password: _, ...usuarioSeguro } = usuario;
    return usuarioSeguro;
  },

  cambiarPassword: (userId, passwordActual, passwordNueva) => {
    const usuarios = obtenerUsuarios();
    const usuario = usuarios.find((u) => u.id === userId);
    if (!usuario) throw new Error('Usuario no encontrado.');
    if (usuario.password !== passwordActual) {
      throw new Error('La contraseña actual no es correcta.');
    }
    const actualizados = usuarios.map((u) =>
      u.id === userId ? { ...u, password: passwordNueva } : u
    );
    guardarUsuarios(actualizados);
  },
};
