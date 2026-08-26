import React from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { useVinculacionPadre } from '../hooks/useVinculacionPadre';
import TarjetaVincularCuenta from '../components/TarjetaVincularCuenta';
import TarjetaCuentaVinculada from '../components/TarjetaCuentaVinculada';
import './ControlParentalPage.css';

const ControlParentalHijoPage = () => {
  const { user } = useAuth();
  const {
    usuarioVinculado,
    correoVincular,
    setCorreoVincular,
    error,
    exito,
    handleVincular,
    handleDesvincular,
  } = useVinculacionPadre();

  return (
    <div className="pagina-control-parental">
      <div className="encabezado-parental">
        <h1 className="titulo-parental">Control parental</h1>
        <p className="subtitulo-parental">
          {user?.esMenor
            ? 'Como eres menor de edad, tu cuenta debe estar vinculada a la de tu padre o madre.'
            : 'Aquí puedes vincularte a la cuenta de tus padres.'}
        </p>
      </div>

      {exito && <div className="mensaje-exito-parental">{exito}</div>}
      {error && <div className="mensaje-error-parental">{error}</div>}

      {!usuarioVinculado && (
        <TarjetaVincularCuenta
          icono="🧒"
          titulo="Vincúlate a la cuenta de tus padres"
          descripcion="Ingresa el correo de la cuenta de tu padre o madre para vincularte."
          placeholder="Correo del padre/madre"
          correoVincular={correoVincular}
          setCorreoVincular={setCorreoVincular}
          onVincular={handleVincular}
        />
      )}

      {usuarioVinculado && (
        <TarjetaCuentaVinculada
          usuarioVinculado={usuarioVinculado}
          etiquetaRelacion="👨‍👧 Tu padre/madre"
          onDesvincular={handleDesvincular}
        >
          <div className="seccion-parental">
            <p className="info-hijo-parental">
              Tu cuenta está vinculada al padre o madre indicado. Ellos pueden ver tu saldo y tus movimientos.
              Si quieres desvincularte, puedes hacerlo en cualquier momento con el botón de arriba.
            </p>
          </div>
        </TarjetaCuentaVinculada>
      )}
    </div>
  );
};

export default ControlParentalHijoPage;
