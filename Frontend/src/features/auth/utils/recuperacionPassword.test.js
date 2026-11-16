import {
  MENSAJE_CODIGO_ENVIADO,
  MENSAJE_SOLICITUD_CODIGO,
  SEGUNDOS_ENFRIAMIENTO_CODIGO,
  codigoRecuperacionValido,
  contrasenasCoinciden,
  mensajeErrorRecuperacion,
  normalizarCodigoRecuperacion,
  segundosRestantesEnfriamiento,
  textoBotonReenvio,
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

describe('segundosRestantesEnfriamiento', () => {
  const inicio = 1_000_000;

  it('empieza en sesenta segundos', () => {
    expect(segundosRestantesEnfriamiento(inicio, inicio)).toBe(
      SEGUNDOS_ENFRIAMIENTO_CODIGO
    );
  });

  it('descuenta los segundos transcurridos', () => {
    expect(segundosRestantesEnfriamiento(inicio, inicio + 15_000)).toBe(45);
    expect(segundosRestantesEnfriamiento(inicio, inicio + 59_900)).toBe(1);
  });

  it('no baja de cero ni supera la duracion', () => {
    expect(segundosRestantesEnfriamiento(inicio, inicio + 60_000)).toBe(0);
    expect(segundosRestantesEnfriamiento(inicio, inicio + 90_000)).toBe(0);
    expect(segundosRestantesEnfriamiento(inicio, inicio - 5_000)).toBe(60);
  });

  it('tolera valores invalidos', () => {
    expect(segundosRestantesEnfriamiento(null, inicio)).toBe(0);
    expect(segundosRestantesEnfriamiento(inicio, NaN)).toBe(0);
  });
});

describe('textoBotonReenvio', () => {
  it('muestra la cuenta atras mientras el enfriamiento esta activo', () => {
    expect(textoBotonReenvio(45)).toBe('Reenviar en 45 s');
    expect(textoBotonReenvio(0)).toBe('Reenviar código');
  });
});

describe('MENSAJE_CODIGO_ENVIADO', () => {
  it('invita a revisar el spam', () => {
    expect(MENSAJE_CODIGO_ENVIADO).toBe(
      'Te enviamos un código; revisa también el spam'
    );
  });
});
