import React, { useState, useMemo } from 'react';
import { useMetas } from '../hooks/useMetas';
import { useResumenGlobalMetas } from '../hooks/useResumenGlobalMetas';
import TarjetaResumenGlobal from '../components/TarjetaResumenGlobal';
import TarjetaRitmoAhorro from '../components/TarjetaRitmoAhorro';
import ListaMetas from '../components/ListaMetas';
import ModalCrearMeta from '../components/ModalCrearMeta';
import ModalAbonarMeta from '../components/ModalAbonarMeta';
import ModalProgramarAporte from '../components/ModalProgramarAporte';
import ModalConsultarProgramacion from '../components/ModalConsultarProgramacion';
import ModalModificarProgramacion from '../components/ModalModificarProgramacion';
import './MetasPage.css';

const MetasPage = () => {
  const { metas, programaciones, loading, error, crear, abonar, programar, actualizarEstado, recargar } = useMetas();
  const { resumen, loading: loadingResumen, error: errorResumen, recargar: recargarResumen } = useResumenGlobalMetas();
  const [modalCrear, setModalCrear] = useState(false);
  const [metaAbonar, setMetaAbonar] = useState(null);
  const [metaProgramar, setMetaProgramar] = useState(null);
  const [programacionConsultar, setProgramacionConsultar] = useState(null);
  const [programacionModificar, setProgramacionModificar] = useState(null);

  const programacionesPorAhorro = useMemo(
    () => Object.fromEntries((programaciones || []).map((p) => [p.id_ahorro, p])),
    [programaciones],
  );

  const onCrear = async (datos) => {
    await crear(datos);
    recargarResumen();
  };

  const onAbonar = async (datos) => {
    await abonar(datos);
    recargarResumen();
  };

  const onProgramar = async (datos) => {
    await programar(datos);
  };

  const onCambiarEstado = async (datos) => {
    await actualizarEstado(datos);
    recargarResumen();
  };

  const abrirModificar = (programacion) => {
    setProgramacionConsultar(null);
    setProgramacionModificar(programacion);
  };

  return (
    <div className="pagina-metas">
      <div className="encabezado-metas">
        <div>
          <h1 className="titulo-pagina">Mis metas</h1>
          <p className="subtitulo-pagina">Ahorra para lo que te propongas.</p>
        </div>
        <div className="acciones-metas">
          <button className="boton-principal-pequeno" onClick={() => setModalCrear(true)}>+ Nueva meta</button>
        </div>
      </div>

      {error && (
        <div className="error-formulario">
          No se pudieron cargar tus metas: {error}
          <button className="boton-reintentar" onClick={recargar}>Reintentar</button>
        </div>
      )}

      <div className="resumen-metas-grid">
        <TarjetaResumenGlobal
          resumen={resumen}
          loading={loadingResumen}
          error={errorResumen}
          onReintentar={recargarResumen}
        />
        <TarjetaRitmoAhorro
          resumen={resumen}
          loading={loadingResumen}
          error={errorResumen}
          onReintentar={recargarResumen}
        />
      </div>

      {loading ? (
        <p className="cargando-pagina">Cargando metas...</p>
      ) : !error && metas.length === 0 ? (
        <div className="metas-sin-contenido">
          <div className="icono-sin-contenido">◆</div>
          <h3>No tienes metas aún</h3>
          <p>Crea tu primera meta y empieza a ahorrar para ese objetivo.</p>
          <button className="boton-principal" onClick={() => setModalCrear(true)}>Crear mi primera meta</button>
        </div>
      ) : (
        <ListaMetas
          metas={metas}
          programacionesPorAhorro={programacionesPorAhorro}
          onAbonar={setMetaAbonar}
          onProgramar={setMetaProgramar}
          onConsultar={setProgramacionConsultar}
        />
      )}

      <ModalCrearMeta open={modalCrear} onClose={() => setModalCrear(false)} onCrear={onCrear} />
      <ModalAbonarMeta
        open={!!metaAbonar}
        onClose={() => setMetaAbonar(null)}
        meta={metaAbonar}
        onAbonar={onAbonar}
      />
      <ModalProgramarAporte
        open={!!metaProgramar}
        onClose={() => setMetaProgramar(null)}
        meta={metaProgramar}
        onProgramar={onProgramar}
      />
      <ModalConsultarProgramacion
        open={!!programacionConsultar}
        onClose={() => setProgramacionConsultar(null)}
        programacion={programacionConsultar}
        onModificar={abrirModificar}
      />
      <ModalModificarProgramacion
        open={!!programacionModificar}
        onClose={() => setProgramacionModificar(null)}
        programacion={programacionModificar}
        onChangeEstado={onCambiarEstado}
      />
    </div>
  );
};

export default MetasPage;
