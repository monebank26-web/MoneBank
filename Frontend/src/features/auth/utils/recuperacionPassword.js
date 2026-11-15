export const MENSAJE_SOLICITUD_CODIGO = (
  'Si el correo está registrado, recibirás un código'
);

export const REGEX_CODIGO_RECUPERACION = /^\d{6}$/;

export const normalizarCodigoRecuperacion = (valor) =>
  String(valor || '').replace(/\D/g, '').slice(0, 6);

export const codigoRecuperacionValido = (codigo) =>
  REGEX_CODIGO_RECUPERACION.test(String(codigo || ''));

export const contrasenasCoinciden = (nueva, confirmar) =>
  Boolean(nueva) && nueva === confirmar;

export const mensajeErrorRecuperacion = (error) => {
  if (error?.status === 410) {
    return error.message || 'El código es inválido o ha expirado.';
  }

  if ([400, 422, 429].includes(error?.status) && error?.message) {
    return error.message;
  }

  return 'No pudimos completar la solicitud. Inténtalo de nuevo.';
};
