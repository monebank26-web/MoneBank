import { apiClient } from '../../../core/api/client';
import { authService, toFrontend } from './authService';

jest.mock('../../../core/api/client', () => ({
  apiClient: {
    post: jest.fn(),
    put: jest.fn(),
  },
}));

const USUARIO_BASE = {
  id_usuario: 7,
  nombres: 'Ana',
  apellidos: 'Perez',
  correo: 'ana@example.com',
  id_rol: 2,
  fecha_creacion: '2026-01-01',
  estado: 'ACTIVO',
};

describe('toFrontend', () => {
  it('mapea bloqueo_temporal ausente a false', () => {
    const usuario = toFrontend(USUARIO_BASE);

    expect(usuario.bloqueo_temporal).toBe(false);
  });

  it('mapea bloqueo_temporal y fecha_desbloqueo', () => {
    const usuario = toFrontend({
      ...USUARIO_BASE,
      bloqueo_temporal: true,
      fecha_desbloqueo: '2026-11-02T10:30:00',
    });

    expect(usuario.bloqueo_temporal).toBe(true);
    expect(usuario.fecha_desbloqueo).toBe('2026-11-02T10:30:00');
  });
});

describe('desbloquearUsuario', () => {
  it('llama al endpoint de desbloqueo del usuario', async () => {
    apiClient.put.mockResolvedValue({});

    await authService.desbloquearUsuario(7);

    expect(apiClient.put).toHaveBeenCalledWith('/usuarios/7/desbloquear');
  });
});

describe('recuperación de contraseña', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('solicita el código con el correo', async () => {
    apiClient.post.mockResolvedValue({ mensaje: 'genérico' });

    await authService.solicitarCodigoRecuperacion({
      email: 'ana@example.com',
    });

    expect(apiClient.post).toHaveBeenCalledWith(
      '/auth/password-recovery/request',
      { correo: 'ana@example.com' }
    );
  });

  it('confirma con correo, código y nueva contraseña', async () => {
    apiClient.post.mockResolvedValue({ mensaje: 'ok' });

    await authService.confirmarCodigoRecuperacion({
      email: 'ana@example.com',
      codigo: '000042',
      nuevaContrasena: 'ClaveNueva1!',
    });

    expect(apiClient.post).toHaveBeenCalledWith(
      '/auth/password-recovery/confirm',
      {
        correo: 'ana@example.com',
        codigo: '000042',
        nueva_contrasena: 'ClaveNueva1!',
      }
    );
  });
});
