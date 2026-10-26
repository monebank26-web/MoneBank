// Utilidades puras del panel de usuarios del administrador (HU-0036).

export const ROL_ADMIN = 1;
export const ROL_USUARIO = 2;

export const POR_PAGINA = 10;

export const LONGITUD_MINIMA_MOTIVO_BLOQUEO = 5;
export const LONGITUD_MAXIMA_MOTIVO_BLOQUEO = 255;

const ETIQUETAS_ROL = {
  administrador: 'Administrador',
  normal: 'Usuario',
};

const ETIQUETAS_ESTADO = {
  ACTIVO: 'Activo',
  INACTIVO: 'Inactivo',
  BLOQUEADO: 'Bloqueado',
};

const ICONOS_ESTADO = {
  ACTIVO: 'mdi:check-circle-outline',
  INACTIVO: 'mdi:minus-circle-outline',
  BLOQUEADO: 'mdi:lock-outline',
};

const MESES = [
  'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
  'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
];

// El backend marca el 409 del correo repetido con este codigo. El texto queda
// solo como respaldo por si la respuesta llegara sin `code`.
const CODIGO_CORREO_DUPLICADO = 'CORREO_DUPLICADO';
const MENSAJE_CORREO_DUPLICADO = 'El correo ya está registrado';

const MENSAJES_ERROR_ACCION = {
  NO_PUEDE_BLOQUEARSE: 'No puedes bloquear tu propia cuenta.',
  NO_PUEDE_DESACTIVARSE: 'No puedes desactivar tu propia cuenta.',
  CUENTA_YA_BLOQUEADA: 'Esta cuenta ya está bloqueada.',
  CUENTA_INACTIVA_NO_BLOQUEABLE: 'No puedes bloquear una cuenta inactiva.',
  CUENTA_YA_INACTIVA: 'Esta cuenta ya está inactiva.',
  ULTIMO_ADMINISTRADOR: 'No puedes dejar el sistema sin administradores activos.',
};

export const etiquetaRolAdmin = (rol) => ETIQUETAS_ROL[rol] || rol || '';

export const etiquetaEstadoAdmin = (estado) => ETIQUETAS_ESTADO[estado] || estado || '';

export const claseEstadoAdmin = (estado) =>
  `admin-estado admin-estado--${String(estado || '').toLowerCase()}`;

export const iconoEstadoAdmin = (estado) => ICONOS_ESTADO[estado] || 'mdi:circle-outline';

export const puedeBloquearUsuario = (estado) => estado === 'ACTIVO';

export const puedeDesactivarUsuario = (estado) =>
  estado === 'ACTIVO' || estado === 'BLOQUEADO';

export const motivoBloqueoValido = (motivo) => {
  const longitud = String(motivo || '').trim().length;

  return (
    longitud >= LONGITUD_MINIMA_MOTIVO_BLOQUEO &&
    longitud <= LONGITUD_MAXIMA_MOTIVO_BLOQUEO
  );
};

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

export const fechaBloqueoLegible = (fecha) => fechaCreacionLegible(fecha);

const mensajeErrorDeEstado = (error) => {
  if (error?.status === 404) return 'El usuario ya no existe. Actualiza la lista.';
  if (error?.status === 403) return 'No tienes permisos para realizar esta acción.';

  return '';
};

export const mensajeErrorBloqueo = (error) =>
  MENSAJES_ERROR_ACCION[error?.code] ||
  (error?.status === 422
    ? `El motivo debe tener entre ${LONGITUD_MINIMA_MOTIVO_BLOQUEO} y ${LONGITUD_MAXIMA_MOTIVO_BLOQUEO} caracteres.`
    : '') ||
  mensajeErrorDeEstado(error) ||
  'No se pudo bloquear la cuenta. Inténtalo de nuevo.';

export const mensajeErrorDesactivacion = (error) =>
  MENSAJES_ERROR_ACCION[error?.code] ||
  mensajeErrorDeEstado(error) ||
  'No se pudo desactivar la cuenta. Inténtalo de nuevo.';
