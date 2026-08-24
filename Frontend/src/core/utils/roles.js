const ETIQUETAS_ROL = {
  administrador: '👑 Administrador',
  padre: '👨‍👧 Padre/Madre',
  hijo: '🧒 Hijo/Hija',
  normal: '👤 Cuenta normal',
};

export const etiquetaRol = (rol) => ETIQUETAS_ROL[rol] || rol;
