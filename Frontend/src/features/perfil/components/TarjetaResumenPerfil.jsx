import React from 'react';
import { ROLES } from '../../../core/constants';
import { formatMoney } from '../../../core/utils/format';
import { etiquetaRol } from '../../../core/utils/roles';

const TarjetaResumenPerfil = ({ user }) => {
  const iniciales = user?.nombre?.charAt(0).toUpperCase() || 'U';

  return (
    <div className="tarjeta-resumen-perfil">
      <div className="avatar-perfil">{iniciales}</div>
      <div className="info-resumen-perfil">
        <h2 className="nombre-resumen-perfil">{user?.nombre}</h2>
        <p className="correo-resumen-perfil">{user?.email}</p>
        <span className="chip-rol-perfil">{etiquetaRol(user?.rol)}</span>
      </div>
      {user?.rol !== ROLES.ADMIN && (
        <div className="saldo-resumen-perfil">
          <p className="etiqueta-saldo-perfil">Saldo en Mi Cuenta</p>
          <p className="valor-saldo-perfil">{formatMoney(user?.saldoCuenta)}</p>
        </div>
      )}
    </div>
  );
};

export default TarjetaResumenPerfil;
