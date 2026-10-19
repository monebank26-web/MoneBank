import {
  calcularTotalPaginas,
  esCorreoDuplicado,
  etiquetaEstadoAdmin,
  etiquetaRolAdmin,
  fechaCreacionLegible,
  mensajeVacio,
  textoTotalUsuarios,
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
