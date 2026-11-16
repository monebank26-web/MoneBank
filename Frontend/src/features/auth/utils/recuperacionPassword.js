export const MENSAJE_SOLICITUD_CODIGO = (
  'Si el correo está registrado, recibirás un código'
);

export const MENSAJE_CODIGO_ENVIADO = (
  'Te enviamos un código; revisa también el spam'
);

export const SEGUNDOS_ENFRIAMIENTO_CODIGO = 60;

export const REGEX_CODIGO_RECUPERACION = /^\d{6}$/;

export const segundosRestantesEnfriamiento = (
  inicio,
  ahora = Date.now(),
  duracion = SEGUNDOS_ENFRIAMIENTO_CODIGO
) => {
  const inicioMs = Number(inicio);
  const ahoraMs = Number(ahora);

  if (!Number.isFinite(inicioMs) || !Number.isFinite(ahoraMs)) return 0;

  const transcurridos = Math.floor(Math.max(0, ahoraMs - inicioMs) / 1000);

  return Math.max(0, Math.min(duracion, duracion - transcurridos));
};

export const textoBotonReenvio = (segundos) =>
  segundos > 0 ? `Reenviar en ${segundos} s` : 'Reenviar código';

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
