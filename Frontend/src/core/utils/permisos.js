import { ROLES } from '../constants';

// Fuente única para decidir si un usuario es administrador.
// La usan el router (RutaAdmin y RutaInicio), el destino del login y el menú
// lateral, para que esos sitios no puedan discrepar entre sí.
export const esAdministrador = (usuario) => usuario?.rol === ROLES.ADMIN;
