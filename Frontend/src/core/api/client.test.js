import { apiClient } from './client';
import {
  guardarToken,
  limpiarSesion,
  obtenerToken,
} from '../utils/tokenSesion';

const tokenConExp = (exp) =>
  `header.${btoa(JSON.stringify({ exp }))}.firma`;

beforeEach(() => {
  localStorage.clear();
  limpiarSesion();
  global.fetch = jest.fn();
});

describe('apiClient', () => {
  it('reemplaza el token con el que viene en la respuesta', async () => {
    const inicial = tokenConExp(
      Math.floor(Date.now() / 1000) + 60
    );
    const renovado = tokenConExp(
      Math.floor(Date.now() / 1000) + 3600
    );
    guardarToken(inicial);

    global.fetch.mockResolvedValue({
      ok: true,
      headers: {
        get: (nombre) =>
          nombre === 'X-Token-Renovado' ? renovado : null,
      },
      json: async () => ({}),
    });

    await apiClient.get('/cuentas/');

    expect(obtenerToken()).toBe(renovado);
  });
});
