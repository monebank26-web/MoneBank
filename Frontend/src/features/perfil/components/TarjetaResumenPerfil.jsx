import React from 'react';
import { ROLES } from '../../../core/constants';
import { formatMoney } from '../../../core/utils/format';

const TarjetaResumenPerfil = ({
  user,
  relaciones = [],
}) => {
  const nombreCompleto =
    user?.nombre ||
    `${user?.nombres || ''} ${user?.apellidos || ''}`.trim() ||
    'Usuario';

  const correo =
    user?.email ||
    user?.correo ||
    '';

  const inicial =
    nombreCompleto.charAt(0).toUpperCase();

  const usuarioId = Number(
    user?.id ||
    user?.id_usuario ||
    user?.usuario_id
  );

  const relacionEstaActiva = (relacion) => {
    return (
      !relacion.estado ||
      relacion.estado === 'ACTIVO'
    );
  };

  const esPadre = relaciones.some(
    (relacion) =>
      relacionEstaActiva(relacion) &&
      Number(relacion.id_usuario_parental) === usuarioId
  );

  const esHijo = relaciones.some(
    (relacion) =>
      relacionEstaActiva(relacion) &&
      Number(relacion.id_usuario_dependiente) === usuarioId
  );

  let tipoCuenta = 'Cuenta normal';
  let claseTipoCuenta = 'normal';

  if (user?.rol === ROLES.ADMIN) {
    tipoCuenta = 'Administrador';
    claseTipoCuenta = 'administrador';
  } else if (esPadre && esHijo) {
    tipoCuenta = 'Cuenta padre e hijo';
    claseTipoCuenta = 'mixta';
  } else if (esPadre) {
    tipoCuenta = 'Cuenta padre';
    claseTipoCuenta = 'padre';
  } else if (esHijo) {
    tipoCuenta = 'Cuenta hijo';
    claseTipoCuenta = 'hijo';
  }

  return (
    <div className="tarjeta-resumen-perfil">
      <div className="avatar-perfil">
        {inicial}
      </div>

      <div className="info-resumen-perfil">
        <h2 className="nombre-resumen-perfil">
          {nombreCompleto}
        </h2>

        <p className="correo-resumen-perfil">
          {correo}
        </p>

        <span
          className={`chip-tipo-cuenta-perfil chip-tipo-cuenta-perfil--${claseTipoCuenta}`}
        >
          {tipoCuenta}
        </span>
      </div>

      {user?.rol !== ROLES.ADMIN && (
        <div className="saldo-resumen-perfil">
          <p className="etiqueta-saldo-perfil">
            Saldo en Mi Cuenta
          </p>

          <p className="valor-saldo-perfil">
            {formatMoney(user?.saldoCuenta || 0)}
          </p>
        </div>
      )}
    </div>
  );
};

export default TarjetaResumenPerfil;
