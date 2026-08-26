import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useBolsillos } from '../hooks/useBolsillos';
import { useDetalleBolsillo } from '../hooks/useDetalleBolsillo';
import CabeceraDetalleBolsillo from '../components/CabeceraDetalleBolsillo';
import ListaMovimientosBolsillo from '../components/ListaMovimientosBolsillo';
import ModalEditarBolsillo from '../components/ModalEditarBolsillo';
import ModalDepositarBolsillo from '../components/ModalDepositarBolsillo';
import ModalTransferirBolsillo from '../components/ModalTransferirBolsillo';
import ModalConfirmarEliminarDetalleBolsillo from '../components/ModalConfirmarEliminarDetalleBolsillo';
import { ROUTES } from '../../../core/constants';
import './BolsilloDetallePage.css';
import '../../transacciones/pages/TransaccionesPage.css';

const BolsilloDetallePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { bolsillos, editar, depositar, transferir, eliminar } = useBolsillos();
  const {
    bolsillo,
    movimientos,
    cargando,
    noEncontrado,
    editarYRecargar,
    depositarYRecargar,
    transferirYRecargar,
  } = useDetalleBolsillo({ id, bolsillos, editar, depositar, transferir });

  const [modalEditarAbierto, setModalEditarAbierto] = useState(false);
  const [modalDepositarAbierto, setModalDepositarAbierto] = useState(false);
  const [modalTransferirAbierto, setModalTransferirAbierto] = useState(false);
  const [modalEliminarAbierto, setModalEliminarAbierto] = useState(false);

  const handleEliminar = async () => {
    await eliminar(id);
    navigate(ROUTES.BOLSILLOS);
  };

  if (cargando) {
    return <p className="cargando-pagina">Cargando bolsillo...</p>;
  }

  if (noEncontrado || !bolsillo) {
    return (
      <div className="pagina-detalle-bolsillo">
        <Link to={ROUTES.BOLSILLOS} className="enlace-volver-detalle">← Volver a bolsillos</Link>
        <div className="detalle-sin-contenido">
          <div className="icono-sin-contenido">◈</div>
          <h3>No encontramos este bolsillo</h3>
          <p>Puede que haya sido eliminado o que el enlace no sea correcto.</p>
          <Link to={ROUTES.BOLSILLOS} className="boton-principal">Ver mis bolsillos</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="pagina-detalle-bolsillo">
      <Link to={ROUTES.BOLSILLOS} className="enlace-volver-detalle">← Volver a bolsillos</Link>

      <CabeceraDetalleBolsillo
        bolsillo={bolsillo}
        onDepositar={() => setModalDepositarAbierto(true)}
        onTransferir={() => setModalTransferirAbierto(true)}
        onEditar={() => setModalEditarAbierto(true)}
        onEliminar={() => setModalEliminarAbierto(true)}
      />

      <ListaMovimientosBolsillo movimientos={movimientos} />

      <ModalEditarBolsillo
        open={modalEditarAbierto}
        onClose={() => setModalEditarAbierto(false)}
        bolsillo={bolsillo}
        onEditar={editarYRecargar}
      />
      <ModalDepositarBolsillo
        open={modalDepositarAbierto}
        onClose={() => setModalDepositarAbierto(false)}
        bolsillo={bolsillo}
        onDepositar={depositarYRecargar}
      />
      <ModalTransferirBolsillo
        open={modalTransferirAbierto}
        onClose={() => setModalTransferirAbierto(false)}
        bolsillos={bolsillos}
        bolsilloOrigen={bolsillo}
        onTransferir={transferirYRecargar}
      />
      <ModalConfirmarEliminarDetalleBolsillo
        open={modalEliminarAbierto}
        onClose={() => setModalEliminarAbierto(false)}
        bolsillo={bolsillo}
        onConfirmar={handleEliminar}
      />
    </div>
  );
};

export default BolsilloDetallePage;
