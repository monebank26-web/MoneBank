import {
  MENSAJE_SOLICITUD_CODIGO,
  codigoRecuperacionValido,
  contrasenasCoinciden,
  mensajeErrorRecuperacion,
  normalizarCodigoRecuperacion,
} from './recuperacionPassword';

describe('normalizarCodigoRecuperacion', () => {
  it('deja solo seis digitos', () => {
    expect(normalizarCodigoRecuperacion('12a34-56')).toBe('123456');
    expect(normalizarCodigoRecuperacion('00004299')).toBe('000042');
    expect(normalizarCodigoRecuperacion(null)).toBe('');
  });
});

describe('codigoRecuperacionValido', () => {
  it('solo acepta exactamente seis digitos', () => {
    expect(codigoRecuperacionValido('000042')).toBe(true);
    expect(codigoRecuperacionValido('12345')).toBe(false);
    expect(codigoRecuperacionValido('1234567')).toBe(false);
    expect(codigoRecuperacionValido('abcdef')).toBe(false);
  });
});

describe('contrasenasCoinciden', () => {
  it('exige una contrasena y que ambas sean iguales', () => {
    expect(contrasenasCoinciden('ClaveNueva1!', 'ClaveNueva1!')).toBe(true);
    expect(contrasenasCoinciden('ClaveNueva1!', 'OtraClave1!')).toBe(false);
    expect(contrasenasCoinciden('', '')).toBe(false);
  });
});

describe('mensajeErrorRecuperacion', () => {
  it('traduce el codigo invalido o expirado', () => {
    expect(mensajeErrorRecuperacion({ status: 410 })).toBe(
      'El código es inválido o ha expirado.'
    );
  });

  it('conserva el mensaje de validacion del backend', () => {
    expect(
      mensajeErrorRecuperacion({
        status: 422,
        message: 'La contraseña debe tener al menos 8 caracteres',
      })
    ).toBe('La contraseña debe tener al menos 8 caracteres');
  });

  it('conserva el mensaje de espera del backend', () => {
    expect(
      mensajeErrorRecuperacion({
        status: 429,
        message: 'Espera 60 segundos antes de solicitar otro código.',
      })
    ).toBe('Espera 60 segundos antes de solicitar otro código.');
  });

  it('deja un mensaje generico ante fallos de red', () => {
    expect(mensajeErrorRecuperacion(new Error('Failed to fetch'))).toBe(
      'No pudimos completar la solicitud. Inténtalo de nuevo.'
    );
  });
});

describe('MENSAJE_SOLICITUD_CODIGO', () => {
  it('no revela si el correo existe', () => {
    expect(MENSAJE_SOLICITUD_CODIGO).toBe(
      'Si el correo está registrado, recibirás un código'
    );
  });
});
