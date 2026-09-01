import React, { useState } from 'react';
import { useMetas } from '../hooks/useMetas';
import ListaMetas from '../components/ListaMetas';
import ModalCrearMeta from '../components/ModalCrearMeta';
import ModalAbonarMeta from '../components/ModalAbonarMeta';
import './MetasPage.css';

const MetasPage = () => {
  const { metas, loading, error, crear, abonar, recargar } = useMetas();
  const [modalCrear, setModalCrear] = useState(false);
  const [metaAbonar, setMetaAbonar] = useState(null);

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
        <ListaMetas metas={metas} onAbonar={setMetaAbonar} />
      )}

      <ModalCrearMeta open={modalCrear} onClose={() => setModalCrear(false)} onCrear={crear} />
      <ModalAbonarMeta
        open={!!metaAbonar}
        onClose={() => setMetaAbonar(null)}
        meta={metaAbonar}
        onAbonar={abonar}
      />
    </div>
  );
};

export default MetasPage;
