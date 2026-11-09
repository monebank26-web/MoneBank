import {
  ACCION_DESBLOQUEAR,
  ACCION_REACTIVAR,
  accionCuentaAdmin,
  calcularTotalPaginas,
  esCorreoDuplicado,
  etiquetaEstadoAdmin,
  etiquetaRolAdmin,
  fechaBloqueoLegible,
  fechaCreacionLegible,
  iconoEstadoAdmin,
  mensajeErrorBloqueo,
  mensajeErrorDesactivacion,
  mensajeErrorDesbloqueo,
  mensajeExitoDesbloqueo,
  mensajeVacio,
  motivoBloqueoValido,
  puedeBloquearUsuario,
  puedeDesactivarUsuario,
  textoConfirmacionDesbloqueo,
  textoTotalUsuarios,
  tieneBloqueoTemporalAdmin,
} from './usuariosAdmin';

describe('esCorreoDuplicado', () => {
  it('reconoce el correo repetido por el codigo del backend', () => {
    expect(esCorreoDuplicado({ code: 'CORREO_DUPLICADO' })).toBe(true);
  });

  it('reconoce el correo repetido por el texto exacto si no llega el codigo', () => {
    expect(esCorreoDuplicado({ message: 'El correo ya está registrado' })).toBe(true);
  });

  it('no confunde un fallo de servidor con un correo duplicado', () => {
    expect(esCorreoDuplicado({ message: 'Error interno del servidor' })).toBe(false);
    expect(esCorreoDuplicado(new Error('Failed to fetch'))).toBe(false);
    expect(esCorreoDuplicado(undefined)).toBe(false);
  });
});

describe('mensajeVacio', () => {
  it('prioriza la busqueda sobre los filtros', () => {
    expect(mensajeVacio({ buscar: 'ana' })).toBe('Usuario no encontrado');
    expect(mensajeVacio({ buscar: 'ana', estado: 'ACTIVO', idRol: 1 }))
      .toBe('Usuario no encontrado');
  });

  it('avisa cuando hay filtro pero no busqueda', () => {
    expect(mensajeVacio({ estado: 'BLOQUEADO' })).toBe('No hay usuarios con ese filtro');
    expect(mensajeVacio({ idRol: 2 })).toBe('No hay usuarios con ese filtro');
  });

  it('avisa cuando no hay usuarios ni filtros', () => {
    expect(mensajeVacio({})).toBe('No hay usuarios registrados');
    expect(mensajeVacio()).toBe('No hay usuarios registrados');
  });
});

describe('calcularTotalPaginas', () => {
  it('nunca baja de una pagina', () => {
    expect(calcularTotalPaginas(0, 10)).toBe(1);
    expect(calcularTotalPaginas(undefined, 10)).toBe(1);
  });

  it('redondea hacia arriba', () => {
    expect(calcularTotalPaginas(10, 10)).toBe(1);
    expect(calcularTotalPaginas(11, 10)).toBe(2);
    expect(calcularTotalPaginas(29, 10)).toBe(3);
    expect(calcularTotalPaginas(30, 10)).toBe(3);
    expect(calcularTotalPaginas(31, 10)).toBe(4);
  });
});

describe('textoTotalUsuarios', () => {
  it('singulariza solo con uno', () => {
    expect(textoTotalUsuarios(1)).toBe('1 usuario');
    expect(textoTotalUsuarios(0)).toBe('0 usuarios');
    expect(textoTotalUsuarios(29)).toBe('29 usuarios');
  });
});

describe('etiquetas', () => {
  it('traduce los roles del panel', () => {
    expect(etiquetaRolAdmin('administrador')).toBe('Administrador');
    expect(etiquetaRolAdmin('normal')).toBe('Usuario');
  });

  it('traduce los estados de la base de datos', () => {
    expect(etiquetaEstadoAdmin('ACTIVO')).toBe('Activo');
    expect(etiquetaEstadoAdmin('INACTIVO')).toBe('Inactivo');
    expect(etiquetaEstadoAdmin('BLOQUEADO')).toBe('Bloqueado');
  });
});

describe('fechaCreacionLegible', () => {
  it('no corre el dia de una fecha sin hora', () => {
    expect(fechaCreacionLegible('2026-08-31')).toBe('31 de agosto de 2026');
    expect(fechaCreacionLegible('2026-01-01')).toBe('1 de enero de 2026');
  });

  it('devuelve vacio cuando no hay fecha', () => {
    expect(fechaCreacionLegible(null)).toBe('');
    expect(fechaCreacionLegible('')).toBe('');
  });
});

describe('fechaBloqueoLegible', () => {
  it('tolera la hora ISO que devuelve el backend', () => {
    expect(fechaBloqueoLegible('2026-10-25T14:30:00')).toBe('25 de octubre de 2026');
  });

  it('conserva el dia local en una hora nocturna', () => {
    expect(fechaBloqueoLegible('2026-11-02T22:54:00')).toBe('2 de noviembre de 2026');
  });

  it('devuelve vacio cuando no hay fecha de bloqueo', () => {
    expect(fechaBloqueoLegible(null)).toBe('');
    expect(fechaBloqueoLegible('')).toBe('');
  });
});

describe('acciones segun el estado', () => {
  it('solo permite bloquear cuentas activas', () => {
    expect(puedeBloquearUsuario('ACTIVO')).toBe(true);
    expect(puedeBloquearUsuario('BLOQUEADO')).toBe(false);
    expect(puedeBloquearUsuario('INACTIVO')).toBe(false);
    expect(puedeBloquearUsuario(undefined)).toBe(false);
  });

  it('permite desactivar cuentas activas o bloqueadas', () => {
    expect(puedeDesactivarUsuario('ACTIVO')).toBe(true);
    expect(puedeDesactivarUsuario('BLOQUEADO')).toBe(true);
    expect(puedeDesactivarUsuario('INACTIVO')).toBe(false);
  });

  it('asigna un icono a cada estado', () => {
    expect(iconoEstadoAdmin('ACTIVO')).toBe('mdi:check-circle-outline');
    expect(iconoEstadoAdmin('BLOQUEADO')).toBe('mdi:lock-outline');
    expect(iconoEstadoAdmin('INACTIVO')).toBe('mdi:minus-circle-outline');
    expect(iconoEstadoAdmin('OTRO')).toBe('mdi:circle-outline');
  });
});

describe('acciones de desbloqueo y reactivacion', () => {
  it('detecta el bloqueo temporal solo en cuentas activas', () => {
    expect(tieneBloqueoTemporalAdmin({ estado: 'ACTIVO', bloqueo_temporal: true })).toBe(true);
    expect(tieneBloqueoTemporalAdmin({ estado: 'ACTIVO', bloqueo_temporal: false })).toBe(false);
    expect(tieneBloqueoTemporalAdmin({ estado: 'BLOQUEADO', bloqueo_temporal: true })).toBe(false);
    expect(tieneBloqueoTemporalAdmin(undefined)).toBe(false);
  });

  it('elige la accion segun el estado y el bloqueo temporal', () => {
    expect(accionCuentaAdmin({ estado: 'ACTIVO', bloqueo_temporal: false })).toBeNull();
    expect(accionCuentaAdmin({ estado: 'ACTIVO', bloqueo_temporal: true }))
      .toBe(ACCION_DESBLOQUEAR);
    expect(accionCuentaAdmin({ estado: 'BLOQUEADO', bloqueo_temporal: false }))
      .toBe(ACCION_DESBLOQUEAR);
    expect(accionCuentaAdmin({ estado: 'INACTIVO', bloqueo_temporal: false }))
      .toBe(ACCION_REACTIVAR);
    expect(accionCuentaAdmin(undefined)).toBeNull();
  });

  it('describe la consecuencia de cada accion', () => {
    expect(textoConfirmacionDesbloqueo({ estado: 'BLOQUEADO' })).toBe(
      'La cuenta podrá iniciar sesión de nuevo. Se borrará el motivo del ' +
      'bloqueo. La acción quedará registrada.'
    );
    expect(textoConfirmacionDesbloqueo({ estado: 'INACTIVO' })).toBe(
      'La cuenta volverá a estar activa y podrá iniciar sesión. ' +
      'La acción quedará registrada.'
    );
    expect(textoConfirmacionDesbloqueo({
      estado: 'ACTIVO',
      bloqueo_temporal: true,
    })).toBe(
      'Se reiniciarán los intentos fallidos y la cuenta podrá iniciar ' +
      'sesión de nuevo.'
    );
    expect(textoConfirmacionDesbloqueo({ estado: 'ACTIVO' })).toBe('');
  });

  it('elige el mensaje de exito segun la accion', () => {
    expect(mensajeExitoDesbloqueo(ACCION_DESBLOQUEAR))
      .toBe('Cuenta desbloqueada correctamente');
    expect(mensajeExitoDesbloqueo(ACCION_REACTIVAR))
      .toBe('Cuenta reactivada correctamente');
    expect(mensajeExitoDesbloqueo(null)).toBe('');
  });

  it('traduce el codigo de cuenta no bloqueada y deja un generico distinto', () => {
    expect(mensajeErrorDesbloqueo({ code: 'CUENTA_NO_BLOQUEADA' }))
      .toBe('La cuenta no se encuentra bloqueada ni desactivada');
    expect(mensajeErrorDesbloqueo({ code: 'OTRO' }))
      .toBe('No se pudo desbloquear ni reactivar la cuenta. Inténtalo de nuevo.');
    expect(mensajeErrorDesbloqueo(new Error('Failed to fetch')))
      .toBe('No se pudo desbloquear ni reactivar la cuenta. Inténtalo de nuevo.');
  });
});

describe('motivoBloqueoValido', () => {
  it('exige al menos cinco caracteres utiles', () => {
    expect(motivoBloqueoValido('abc')).toBe(false);
    expect(motivoBloqueoValido('     ')).toBe(false);
    expect(motivoBloqueoValido('abcde')).toBe(true);
    expect(motivoBloqueoValido('  abcde  ')).toBe(true);
  });

  it('no acepta motivos mayores al limite del backend', () => {
    expect(motivoBloqueoValido('a'.repeat(255))).toBe(true);
    expect(motivoBloqueoValido('a'.repeat(256))).toBe(false);
  });

  it('tolera valores vacios', () => {
    expect(motivoBloqueoValido(null)).toBe(false);
    expect(motivoBloqueoValido(undefined)).toBe(false);
  });
});

describe('mensajes de error de las acciones', () => {
  it('traduce los codigos de negocio del bloqueo', () => {
    expect(mensajeErrorBloqueo({ code: 'NO_PUEDE_BLOQUEARSE' }))
      .toBe('No puedes bloquear tu propia cuenta.');
    expect(mensajeErrorBloqueo({ code: 'CUENTA_YA_BLOQUEADA' }))
      .toBe('Esta cuenta ya está bloqueada.');
    expect(mensajeErrorBloqueo({ code: 'CUENTA_INACTIVA_NO_BLOQUEABLE' }))
      .toBe('No puedes bloquear una cuenta inactiva.');
  });

  it('distingue los errores por estado HTTP', () => {
    expect(mensajeErrorBloqueo({ status: 404 }))
      .toBe('El usuario ya no existe. Actualiza la lista.');
    expect(mensajeErrorBloqueo({ status: 403 }))
      .toBe('No tienes permisos para realizar esta acción.');
    expect(mensajeErrorBloqueo({ status: 422 }))
      .toBe('El motivo debe tener entre 5 y 255 caracteres.');
  });

  it('traduce los codigos de negocio de la desactivacion', () => {
    expect(mensajeErrorDesactivacion({ code: 'NO_PUEDE_DESACTIVARSE' }))
      .toBe('No puedes desactivar tu propia cuenta.');
    expect(mensajeErrorDesactivacion({ code: 'ULTIMO_ADMINISTRADOR' }))
      .toBe('No puedes dejar el sistema sin administradores activos.');
    expect(mensajeErrorDesactivacion({ code: 'CUENTA_YA_INACTIVA' }))
      .toBe('Esta cuenta ya está inactiva.');
  });

  it('deja un mensaje claro cuando el error es desconocido', () => {
    expect(mensajeErrorBloqueo(new Error('Failed to fetch')))
      .toBe('No se pudo bloquear la cuenta. Inténtalo de nuevo.');
    expect(mensajeErrorDesactivacion(new Error('Failed to fetch')))
      .toBe('No se pudo desactivar la cuenta. Inténtalo de nuevo.');
  });
});
