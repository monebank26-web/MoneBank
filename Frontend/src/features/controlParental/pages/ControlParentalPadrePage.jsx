import React from 'react';
import { useVinculacionHijo } from '../hooks/useVinculacionHijo';
import TarjetaVincularCuenta from '../components/TarjetaVincularCuenta';
import TarjetaCuentaVinculada from '../components/TarjetaCuentaVinculada';
import CuadriculaBolsillosHijo from '../components/CuadriculaBolsillosHijo';
import ListaMovimientosHijo from '../components/ListaMovimientosHijo';
import { formatMoney } from '../../../core/utils/format';
import './ControlParentalPage.css';

const ControlParentalPadrePage = () => {
  const {
    usuarioVinculado,
    correoVincular,
    setCorreoVincular,
    error,
    exito,
    transaccionesHijo,
    bolsillosHijo,
    handleVincular,
    handleDesvincular,
  } = useVinculacionHijo();

  return (
    <div className="pagina-control-parental">
      <div className="encabezado-parental">
        <h1 className="titulo-parental">Control parental</h1>
        <p className="subtitulo-parental">Aquí puedes ver y administrar la cuenta de tu hijo o hija.</p>
      </div>

      {exito && <div className="mensaje-exito-parental">{exito}</div>}
      {error && <div className="mensaje-error-parental">{error}</div>}

      {!usuarioVinculado && (
        <TarjetaVincularCuenta
          icono="👨‍👧"
          titulo="Vincula la cuenta de tu hijo o hija"
          descripcion="Ingresa el correo de la cuenta de tu hijo/hija para ver su actividad y saldo."
          placeholder="Correo del hijo/hija"
          correoVincular={correoVincular}
          setCorreoVincular={setCorreoVincular}
          onVincular={handleVincular}
        />
      )}

      {usuarioVinculado && (
        <>
          <TarjetaCuentaVinculada
            usuarioVinculado={usuarioVinculado}
            etiquetaRelacion="🧒 Tu hijo/hija"
            onDesvincular={handleDesvincular}
          >
            <div className="saldo-vinculado">
              <p className="etiqueta-saldo-vinculado">Saldo en cuenta</p>
              <p className="valor-saldo-vinculado">{formatMoney(usuarioVinculado.saldoCuenta)}</p>
            </div>
          </TarjetaCuentaVinculada>

          <CuadriculaBolsillosHijo nombreHijo={usuarioVinculado.nombre} bolsillos={bolsillosHijo} />
          <ListaMovimientosHijo nombreHijo={usuarioVinculado.nombre} movimientos={transaccionesHijo} />
        </>
      )}
    </div>
  );
};

export default ControlParentalPadrePage;
