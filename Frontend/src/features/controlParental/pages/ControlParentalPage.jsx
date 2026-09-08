import React, { useState } from 'react';
import { useControlParental } from '../hooks/useControlParental';
import { controlParentalService } from '../services/controlParentalServices';
import ModalCodigoParental from '../components/ModalCodigoParental';
import './ControlParentalPage.css';

const ControlParentalPage = () => {
  const {
    relaciones,
    cargando,
    error,
    mensaje,
    ejecutar,
  } = useControlParental();

  const [nombreHijo, setNombreHijo] = useState('');
  const [correoHijo, setCorreoHijo] = useState('');
  const [modal, setModal] = useState(null);
  const [cargandoCodigo, setCargandoCodigo] = useState(false);

  const handleSolicitarVinculacion = async (event) => {
    event.preventDefault();

    const resultado = await ejecutar(
      () =>
        controlParentalService.solicitarVinculacion({
          nombreHijo,
          correoHijo,
        }),
      'Código enviado al correo del hijo.'
    );

    if (resultado) {
      setNombreHijo('');
      setCorreoHijo('');
    }
  };


  const handleConfirmarCodigo = async (codigo) => {
    setCargandoCodigo(true);

    try {
      const resultado = await ejecutar(
        () => {
          if (modal === 'vinculacion') {
            return controlParentalService.confirmarVinculacion(codigo);
          }

          return controlParentalService.confirmarDesvinculacion(codigo);
        },
        modal === 'vinculacion'
          ? 'Cuenta vinculada correctamente.'
          : 'Cuenta desvinculada correctamente.'
      );

      if (resultado) {
        setModal(null);
      }

      return resultado;
    } finally {
      setCargandoCodigo(false);
    }
  };

  return (
    <div className="pagina-control-parental">
      <div>
        <h1>Control parental</h1>
        <p>
          Administra las vinculaciones parentales desde esta sección.
        </p>
      </div>

      {error && (
        <div className="error-parental">
          {error}
        </div>
      )}

      {mensaje && (
        <div className="ok-parental">
          {mensaje}
        </div>
      )}

      <section>
        <h2>Vincular cuenta de hijo</h2>

        <form onSubmit={handleSolicitarVinculacion}>
          <input
            type="text"
            placeholder="Nombre del hijo"
            value={nombreHijo}
            onChange={(event) => setNombreHijo(event.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Correo del hijo"
            value={correoHijo}
            onChange={(event) => setCorreoHijo(event.target.value)}
            required
          />

          <button type="submit">
            Enviar código
          </button>
        </form>

        <small>
          El código de seis dígitos será enviado al correo del hijo.
        </small>
      </section>

      <section>
        <h2>Confirmar vinculación</h2>

        <button
          type="button"
          onClick={() => setModal('vinculacion')}
        >
          Ingresar código de vinculación
        </button>
      </section>

      <section>
        <h2>Vinculaciones activas</h2>

        {cargando && <p>Cargando vinculaciones...</p>}

        {!cargando && relaciones.length === 0 && (
          <p>No hay vinculaciones activas.</p>
        )}

        {!cargando &&
          relaciones.map((relacion) => (
            <div
              className="relacion-parental"
              key={relacion.id_control}
            >
              <p>
                Relación activa
              </p>

              <p>
                Padre: {relacion.id_usuario_parental}
              </p>

              <p>
                Hijo: {relacion.id_usuario_dependiente}
              </p>
            </div>
          ))}
      </section>

          
      <ModalCodigoParental
        abierto={Boolean(modal)}
        titulo={
          modal === 'vinculacion'
            ? 'Confirmar vinculación'
            : 'Confirmar desvinculación'
        }
        descripcion="Escribe el código de seis dígitos recibido por correo."
        cargando={cargandoCodigo}
        onConfirmar={handleConfirmarCodigo}
        onCerrar={() => setModal(null)}
      />
    </div>
  );
};

export default ControlParentalPage;
