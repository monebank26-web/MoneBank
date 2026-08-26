import React, { useState } from 'react';
import { useLimites } from '../hooks/useLimites';
import TarjetaLimite from '../components/TarjetaLimite';
import ListaAlertas from '../components/ListaAlertas';
import ModalCrearLimite from '../components/ModalCrearLimite';
import './LimitesPage.css';

const LimitesPage = () => {
  const { limites, alertas, loading, error, crear, recargar } = useLimites();
  const [modalCrear, setModalCrear] = useState(false);

  return (
    <div className="pagina-limites">
      <div className="encabezado-limites">
        <div>
          <h1 className="titulo-pagina">Mis límites</h1>
          <p className="subtitulo-pagina">Controla cuánto gastas por categoría en cada periodo.</p>
        </div>
        <div className="acciones-limites">
          <button className="boton-principal-pequeno" onClick={() => setModalCrear(true)}>+ Nuevo límite</button>
        </div>
      </div>

      {error && (
        <div className="error-formulario">
          No se pudieron cargar tus límites: {error}
          <button className="boton-reintentar" onClick={recargar}>Reintentar</button>
        </div>
      )}

      {!error && !loading && alertas.length > 0 && <ListaAlertas alertas={alertas} />}

      {loading ? (
        <p className="cargando-pagina">Cargando límites...</p>
      ) : !error && limites.length === 0 ? (
        <div className="limites-sin-contenido">
          <div className="icono-sin-contenido">▲</div>
          <h3>No tienes límites aún</h3>
          <p>Crea un límite de gasto y te avisamos cuando estés cerca del tope.</p>
          <button className="boton-principal" onClick={() => setModalCrear(true)}>Crear mi primer límite</button>
        </div>
      ) : (
        <div className="lista-limites">
          {limites.map((limite) => (
            <TarjetaLimite key={limite.id_ahorro} limite={limite} />
          ))}
        </div>
      )}

      <ModalCrearLimite open={modalCrear} onClose={() => setModalCrear(false)} onCrear={crear} />
    </div>
  );
};

export default LimitesPage;
