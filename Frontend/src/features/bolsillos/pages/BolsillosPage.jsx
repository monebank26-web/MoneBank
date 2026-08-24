import React from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { useBolsillos } from '../hooks/useBolsillos';
import { useModalesBolsillos } from '../hooks/useModalesBolsillos';
import { formatMoney } from '../../../core/utils/format';
import TarjetaBolsillo from '../components/TarjetaBolsillo';
import ModalCrearBolsillo from '../components/ModalCrearBolsillo';
import ModalEditarBolsillo from '../components/ModalEditarBolsillo';
import ModalDepositarBolsillo from '../components/ModalDepositarBolsillo';
import ModalTransferirBolsillo from '../components/ModalTransferirBolsillo';
import ModalConfirmarEliminarBolsillo from '../components/ModalConfirmarEliminarBolsillo';
import './BolsillosPage.css';

const BolsillosPage = () => {
  const { user } = useAuth();
  const { bolsillos, loading, totalSaldo, crear, eliminar, transferir, depositar, editar } = useBolsillos();
  const modales = useModalesBolsillos({ eliminar });

  return (
    <div className="pagina-bolsillos">
      <div className="encabezado-bolsillos">
        <div>
          <h1 className="titulo-pagina">Mis bolsillos</h1>
          <p className="subtitulo-pagina">Total acumulado: <strong>{formatMoney(totalSaldo)}</strong></p>
        </div>
        <div className="acciones-bolsillos">
          <button className="boton-secundario" onClick={() => modales.abrirTransferir()}>Transferir</button>
          <button className="boton-principal-pequeno" onClick={() => modales.setModalCrearAbierto(true)}>+ Nuevo bolsillo</button>
        </div>
      </div>

      {loading ? (
        <p className="cargando-pagina">Cargando bolsillos...</p>
      ) : bolsillos.length === 0 ? (
        <div className="bolsillos-sin-contenido">
          <div className="icono-sin-contenido">◈</div>
          <h3>No tienes bolsillos aún</h3>
          <p>Crea tu primer bolsillo para empezar a organizar tu dinero.</p>
          <button className="boton-principal" onClick={() => modales.setModalCrearAbierto(true)}>Crear bolsillo</button>
        </div>
      ) : (
        <div className="lista-bolsillos">
          {bolsillos.map((bolsillo) => (
            <TarjetaBolsillo
              key={bolsillo.id}
              bolsillo={bolsillo}
              onDepositar={modales.setBolsilloParaDepositar}
              onTransferir={modales.abrirTransferir}
              onEditar={modales.setBolsilloParaEditar}
              onEliminar={modales.setBolsilloParaEliminar}
            />
          ))}
        </div>
      )}

      <ModalCrearBolsillo
        open={modales.modalCrearAbierto}
        onClose={() => modales.setModalCrearAbierto(false)}
        onCrear={crear}
        saldoDisponible={user?.saldoCuenta || 0}
      />
      <ModalEditarBolsillo
        open={!!modales.bolsilloParaEditar}
        onClose={() => modales.setBolsilloParaEditar(null)}
        bolsillo={modales.bolsilloParaEditar}
        onEditar={editar}
      />
      <ModalDepositarBolsillo
        open={!!modales.bolsilloParaDepositar}
        onClose={() => modales.setBolsilloParaDepositar(null)}
        bolsillo={modales.bolsilloParaDepositar}
        onDepositar={depositar}
      />
      <ModalTransferirBolsillo
        open={modales.modalTransferirAbierto}
        onClose={modales.cerrarTransferir}
        bolsillos={bolsillos}
        bolsilloOrigen={modales.bolsilloOrigenTransferencia}
        onTransferir={transferir}
      />
      <ModalConfirmarEliminarBolsillo
        bolsillo={modales.bolsilloParaEliminar}
        onCancelar={() => modales.setBolsilloParaEliminar(null)}
        onConfirmar={modales.confirmarEliminar}
      />
    </div>
  );
};

export default BolsillosPage;
