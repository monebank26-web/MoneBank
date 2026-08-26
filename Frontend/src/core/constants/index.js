
export const STORAGE_KEYS = {
  USER: 'mb_user',
  TOKEN: 'mb_token',
  BOLSILLOS: 'mb_bolsillos',
  TRANSACCIONES: 'mb_transacciones',
  USERS: 'mb_users',
  VINCULOS: 'mb_vinculos',
};

export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  BOLSILLOS: '/bolsillos',
  BOLSILLO_DETALLE: '/bolsillos/:id',
  METAS: '/metas',
  LIMITES: '/limites',
  TRANSACCIONES: '/transacciones',
  ADMIN: '/admin',
  CONTROL_PARENTAL_PADRE: '/control-parental/padre',
  CONTROL_PARENTAL_HIJO: '/control-parental/hijo',
  PERFIL: '/perfil',
};

export const ROLES = {
  ADMIN: 'administrador',
  PADRE: 'padre',
  HIJO: 'hijo',
  NORMAL: 'normal',
};

export const CORREO_ADMIN = 'admin@monebank.com';

export const PERIODOS_LIMITE = ['DIARIO', 'SEMANAL', 'MENSUAL'];

export const COLORES_BOLSILLO = [
  '#3b82f6', // azul
  '#10b981', // verde
  '#f59e0b', // amarillo
  '#ef4444', // rojo
  '#8b5cf6', // morado
  '#06b6d4', // cyan
  '#f97316', // naranja
  '#ec4899', // rosa
];
