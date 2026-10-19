// Utilidades puras del panel de usuarios del administrador (HU-0036).

export const ROL_ADMIN = 1;
export const ROL_USUARIO = 2;

export const POR_PAGINA = 10;

const ETIQUETAS_ROL = {
  administrador: 'Administrador',
  normal: 'Usuario',
};

const ETIQUETAS_ESTADO = {
  ACTIVO: 'Activo',
  INACTIVO: 'Inactivo',
  BLOQUEADO: 'Bloqueado',
};

const MESES = [
  'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
];

// El backend marca el 409 del correo repetido con este codigo. El texto queda
// solo como respaldo por si la respuesta llegara sin `code`.
const CODIGO_CORREO_DUPLICADO = 'CORREO_DUPLICADO';
const MENSAJE_CORREO_DUPLICADO = 'El correo ya está registrado';

export const etiquetaRolAdmin = (rol) => ETIQUETAS_ROL[rol] || rol || '';

export const etiquetaEstadoAdmin = (estado) => ETIQUETAS_ESTADO[estado] || estado || '';

export const claseEstadoAdmin = (estado) =>
  `admin-estado admin-estado--${String(estado || '').toLowerCase()}`;

export const esCorreoDuplicado = (error) =>
  error?.code === CODIGO_CORREO_DUPLICADO ||
  error?.message === MENSAJE_CORREO_DUPLICADO;

export const calcularTotalPaginas = (total, porPagina = POR_PAGINA) => {
  const cantidad = Number(total) || 0;
  const tamano = Number(porPagina) || POR_PAGINA;

  return Math.max(1, Math.ceil(cantidad / tamano));
};

export const textoTotalUsuarios = (total) => {
  const cantidad = Number(total) || 0;

  return `${cantidad} usuario${cantidad === 1 ? '' : 's'}`;
};

export const mensajeVacio = ({ buscar, estado, idRol } = {}) => {
  if (buscar) return 'Usuario no encontrado';
  if (estado || idRol) return 'No hay usuarios con ese filtro';

  return 'No hay usuarios registrados';
};

// `fecha_creacion` llega como "AAAA-MM-DD". Se arma a mano para no correr el
// dia por la zona horaria (new Date("2026-08-31") es UTC y en Colombia cae el 30).
export const fechaCreacionLegible = (fecha) => {
  if (!fecha) return '';

  const [anio, mes, dia] = String(fecha).slice(0, 10).split('-').map(Number);

  if (!anio || !mes || !dia) return String(fecha);

  return `${dia} de ${MESES[mes - 1]} de ${anio}`;
};
