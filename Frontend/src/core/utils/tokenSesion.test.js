import { STORAGE_KEYS } from '../constants';
import {
  guardarToken,
  leerExp,
  limpiarSesion,
  motivoSesion,
  obtenerToken,
  suscribirse,
  tokenVigente,
} from './tokenSesion';

const tokenConExp = (exp) =>
  `header.${btoa(JSON.stringify({ exp }))}.firma`;

beforeEach(() => {
  localStorage.clear();
  limpiarSesion();
});

describe('tokenSesion', () => {
  it('guarda el token y lo considera vigente', () => {
    const exp = Math.floor(Date.now() / 1000) + 3600;
    const token = tokenConExp(exp);

    guardarToken(token);

    expect(obtenerToken()).toBe(token);
    expect(leerExp(obtenerToken())).toBe(exp);
    expect(tokenVigente()).toBe(true);
  });

  it('detecta un token expirado', () => {
    guardarToken(
      tokenConExp(Math.floor(Date.now() / 1000) - 10)
    );

    expect(tokenVigente()).toBe(false);
  });

  it('no sobrescribe un token con menor expiracion', () => {
    const exp = Math.floor(Date.now() / 1000) + 3600;
    guardarToken(tokenConExp(exp));
    guardarToken(
      tokenConExp(Math.floor(Date.now() / 1000) + 60)
    );

    expect(leerExp(obtenerToken())).toBe(exp);
  });

  it('notifica cuando se guarda un token renovado', () => {
    const escucha = jest.fn();
    const unsubscribe = suscribirse(escucha);
    const token = tokenConExp(
      Math.floor(Date.now() / 1000) + 3600
    );

    guardarToken(token);

    expect(escucha).toHaveBeenCalledWith({
      tipo: 'token',
      token,
    });
    unsubscribe();
  });

  it('limpia usuario y token y registra el motivo', () => {
    const escucha = jest.fn();
    const unsubscribe = suscribirse(escucha);
    localStorage.setItem(STORAGE_KEYS.USER, '{}');
    guardarToken(
      tokenConExp(Math.floor(Date.now() / 1000) + 3600)
    );

    limpiarSesion({ motivo: 'expirada' });

    expect(
      localStorage.getItem(STORAGE_KEYS.USER)
    ).toBeNull();
    expect(
      localStorage.getItem(STORAGE_KEYS.TOKEN)
    ).toBeNull();
    expect(motivoSesion()).toBe('expirada');
    expect(escucha).toHaveBeenCalledWith({
      tipo: 'logout',
      motivo: 'expirada',
    });
    unsubscribe();
  });

  it('borra el historial de chat solo cuando se pide', () => {
    localStorage.setItem(
      `${STORAGE_KEYS.CHAT_HISTORIAL}_7`,
      '[]'
    );

    limpiarSesion({ borrarChat: true, userId: 7 });

    expect(
      localStorage.getItem(
        `${STORAGE_KEYS.CHAT_HISTORIAL}_7`
      )
    ).toBeNull();
  });
});
