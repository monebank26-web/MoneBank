import { ROLES } from '../constants';
import { esAdministrador } from './permisos';

describe('esAdministrador', () => {
  it('reconoce al administrador', () => {
    expect(esAdministrador({ rol: ROLES.ADMIN })).toBe(true);
  });

  it('no confunde los demas roles con administrador', () => {
    expect(esAdministrador({ rol: ROLES.NORMAL })).toBe(false);
    expect(esAdministrador({ rol: ROLES.PADRE })).toBe(false);
    expect(esAdministrador({ rol: ROLES.HIJO })).toBe(false);
  });

  it('no falla mientras la sesion todavia no esta', () => {
    expect(esAdministrador(undefined)).toBe(false);
    expect(esAdministrador(null)).toBe(false);
    expect(esAdministrador({})).toBe(false);
  });
});
