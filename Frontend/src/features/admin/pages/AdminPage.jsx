import React from 'react';
import { Icon } from '@iconify/react';
import { useAuth } from '../../../core/context/AuthContext';
import '../../../shared/styles/transacciones-modal.css';
import { useUsuariosAdmin } from '../hooks/useUsuariosAdmin';
import { useAccionesUsuarioAdmin } from '../hooks/useAccionesUsuarioAdmin';
import { mensajeVacio, textoTotalUsuarios } from '../utils/usuariosAdmin';
import BarraFiltrosUsuarios from '../components/BarraFiltrosUsuarios';
import FilaUsuarioAdmin from '../components/FilaUsuarioAdmin';
import ModalDetalleUsuario from '../components/ModalDetalleUsuario';
import ModalEditarUsuario from '../components/ModalEditarUsuario';
import ModalEliminarUsuario from '../components/ModalEliminarUsuario';
import ModalBloquearUsuario from '../components/ModalBloquearUsuario';
import ModalDesbloquearUsuario from '../components/ModalDesbloquearUsuario';
import ModalRestablecerPassword from '../components/ModalRestablecerPassword';
import './AdminPage.css';

const TarjetaMetrica = ({ etiqueta, valor, extra, icono, variante }) => (
  <div className={`admin-metrica admin-metrica--${variante}`}>
    <span className="admin-metrica__info">
      <span className="admin-metrica__etiqueta">{etiqueta}</span>
      <span className="admin-metrica__valor">
        {valor}
        {extra && <span className="admin-metrica__extra">{extra}</span>}
      </span>
    </span>
    <span className="admin-metrica__icono" aria-hidden="true">
      {icono === 'punto' ? <span className="admin-metrica__punto" /> : <Icon icon={icono} />}
    </span>
  </div>
);

const PiePaginacion = ({ pagina, totalPaginas, total, cantidad, onChange }) => {
  const maximoVisible = 5;
  let inicio = Math.max(1, pagina - 2);
  let fin = Math.min(totalPaginas, inicio + maximoVisible - 1);
  inicio = Math.max(1, fin - maximoVisible + 1);
  const paginas = Array.from({ length: fin - inicio + 1 }, (_, indice) => inicio + indice);

  return (
    <div className="admin-pie">
      <p className="admin-pie__info">
        Mostrando <strong>{cantidad}</strong> de <strong>{total}</strong> cuentas institucionales
      </p>

      <div className="admin-pie__controles">
        <button
          type="button"
          className="admin-pie__btn admin-pie__btn--borde"
          disabled={pagina <= 1}
          onClick={() => onChange(pagina - 1)}
        >
          Anterior
        </button>

        {inicio > 1 && (
          <span className="admin-pie__elipsis">
            <Icon icon="mdi:dots-horizontal" aria-hidden="true" />
          </span>
        )}

        {paginas.map((numero) => (
          <button
            key={numero}
            type="button"
            className={`admin-pie__btn admin-pie__btn--numero${
              numero === pagina ? ' admin-pie__btn--activo' : ''
            }`}
            aria-current={numero === pagina ? 'page' : undefined}
            onClick={() => onChange(numero)}
          >
            {numero}
          </button>
        ))}

        {fin < totalPaginas && (
          <span className="admin-pie__elipsis">
            <Icon icon="mdi:dots-horizontal" aria-hidden="true" />
          </span>
        )}

        <button
          type="button"
          className="admin-pie__btn admin-pie__btn--borde admin-pie__btn--siguiente"
          disabled={pagina >= totalPaginas}
          onClick={() => onChange(pagina + 1)}
        >
          Siguiente
        </button>
      </div>
    </div>
  );
};

const AdminPage = () => {
  const { user } = useAuth();
  const {
    usuarios,
    total,
    metricas,
    pagina,
    totalPaginas,
    busqueda,
    setBusqueda,
    idRol,
    setIdRol,
    estado,
    setEstado,
    cargando,
    error,
    setPagina,
    recargar,
    limpiarFiltros,
  } = useUsuariosAdmin();

  const acciones = useAccionesUsuarioAdmin({ recargar });

  const ejecutarAccion = (clave, usuario) => {
    if (clave === 'editar') acciones.abrirEditar(usuario);
    if (clave === 'bloquear') acciones.abrirBloquear(usuario);
    if (clave === 'desbloquear') acciones.abrirDesbloquear(usuario);
    if (clave === 'restablecer') acciones.abrirRestablecer(usuario);
    if (clave === 'desactivar') acciones.abrirEliminar(usuario);
  };

  const porcentajeActivos = metricas.total
    ? `${((metricas.activos / metricas.total) * 100).toFixed(1)}%`
    : '0.0%';

  return (
    <div className="admin-pagina">
      <div className="admin-encabezado">
        <div className="admin-encabezado__marca">
          <span className="admin-encabezado__icono">
            <Icon icon="mdi:shield-account-outline" />
          </span>
          <div className="admin-encabezado__texto">
            <h1 className="admin-titulo">Panel de administrador</h1>
            <p className="admin-subtitulo">Gestiona las cuentas de MoneBank.</p>
            <p className="admin-ayuda">
              <Icon icon="mdi:information-outline" />
              Bloquear impide iniciar sesión; desactivar deja la cuenta inactiva.
            </p>
          </div>
        </div>

        <div className="admin-encabezado__lado">
          {acciones.mensaje && (
            <span
              className={acciones.mensajeEsError ? 'admin-mensaje-error' : 'admin-mensaje-exito'}
              role={acciones.mensajeEsError ? 'alert' : 'status'}
              aria-live="polite"
            >
              <Icon
                icon={
                  acciones.mensajeEsError
                    ? 'mdi:alert-circle-outline'
                    : 'mdi:check-circle-outline'
                }
                aria-hidden="true"
              />
              {acciones.mensaje}
            </span>
          )}
          <span className="admin-total">{textoTotalUsuarios(total)}</span>
        </div>
      </div>

      <div className="admin-metricas">
        <TarjetaMetrica
          etiqueta="TOTAL USUARIOS"
          valor={metricas.total}
          icono="mdi:account-group-outline"
          variante="total"
        />
        <TarjetaMetrica
          etiqueta="ACTIVOS"
          valor={metricas.activos}
          extra={porcentajeActivos}
          icono="punto"
          variante="activos"
        />
        <TarjetaMetrica
          etiqueta="BLOQUEADOS"
          valor={metricas.bloqueados}
          extra="Restringidos"
          icono="mdi:lock"
          variante="bloqueados"
        />
        <TarjetaMetrica
          etiqueta="INACTIVOS"
          valor={metricas.inactivos}
          extra="Sin sesión"
          icono="mdi:prohibited"
          variante="inactivos"
        />
      </div>

      <BarraFiltrosUsuarios
        busqueda={busqueda}
        setBusqueda={setBusqueda}
        idRol={idRol}
        setIdRol={setIdRol}
        estado={estado}
        setEstado={setEstado}
        onLimpiar={limpiarFiltros}
      />

      {error ? (
        <div className="error-formulario">
          {error}
          <button type="button" className="boton-reintentar" onClick={recargar}>
            Reintentar
          </button>
        </div>
      ) : cargando ? (
        <p className="cargando-pagina">Cargando usuarios...</p>
      ) : usuarios.length === 0 ? (
        <div className="admin-sin-resultados">
          <Icon icon="mdi:account-search-outline" className="admin-sin-resultados__icono" />
          <p>{mensajeVacio({ buscar: busqueda.trim(), estado, idRol })}</p>
        </div>
      ) : (
        <>
          <div className="admin-tabla-cabecera" aria-hidden="true">
            <span>Usuario</span>
            <span>ID MoneBank</span>
            <span>Rol</span>
            <span>Estado</span>
            <span>Acciones</span>
          </div>

          <div className="admin-lista">
            {usuarios.map((usuario) => (
              <FilaUsuarioAdmin
                key={usuario.id}
                usuario={usuario}
                usuarioActual={user}
                onVerDetalle={acciones.abrirDetalle}
                onAccion={ejecutarAccion}
              />
            ))}
          </div>

          <PiePaginacion
            pagina={pagina}
            totalPaginas={totalPaginas}
            total={total}
            cantidad={usuarios.length}
            onChange={setPagina}
          />
        </>
      )}

      <ModalDetalleUsuario
        open={acciones.modalDetalleAbierto}
        onClose={() => acciones.setModalDetalleAbierto(false)}
        usuario={acciones.usuarioSeleccionado}
        usuarioActual={user}
        onEditar={(usuario) => {
          acciones.setModalDetalleAbierto(false);
          acciones.abrirEditar(usuario);
        }}
        onBloquear={(usuario) => {
          acciones.setModalDetalleAbierto(false);
          acciones.abrirBloquear(usuario);
        }}
        onEliminar={(usuario) => {
          acciones.setModalDetalleAbierto(false);
          acciones.abrirEliminar(usuario);
        }}
        onDesbloquear={(usuario) => {
          acciones.setModalDetalleAbierto(false);
          acciones.abrirDesbloquear(usuario);
        }}
        onRestablecer={(usuario) => {
          acciones.setModalDetalleAbierto(false);
          acciones.abrirRestablecer(usuario);
        }}
      />

      <ModalEditarUsuario
        open={acciones.modalEditarAbierto}
        onClose={acciones.cerrarEditar}
        formulario={acciones.formularioEdicion}
        setFormulario={acciones.setFormularioEdicion}
        onGuardar={acciones.guardarEdicion}
        error={acciones.errorEdicion}
        guardando={acciones.guardando}
      />

      <ModalBloquearUsuario
        open={acciones.modalBloquearAbierto}
        onClose={() => acciones.setModalBloquearAbierto(false)}
        usuario={acciones.usuarioSeleccionado}
        motivoBloqueo={acciones.motivoBloqueo}
        onCambiarMotivo={acciones.cambiarMotivoBloqueo}
        onConfirmar={acciones.confirmarBloqueo}
        error={acciones.errorBloqueo}
        bloqueando={acciones.bloqueando}
      />

      <ModalEliminarUsuario
        open={acciones.modalEliminarAbierto}
        onClose={() => acciones.setModalEliminarAbierto(false)}
        usuario={acciones.usuarioSeleccionado}
        onConfirmar={acciones.eliminarUsuario}
        error={acciones.errorEliminar}
        desactivando={acciones.desactivando}
      />

      <ModalDesbloquearUsuario
        open={acciones.modalDesbloquearAbierto}
        onClose={acciones.cerrarDesbloquear}
        usuario={acciones.usuarioSeleccionado}
        onConfirmar={acciones.confirmarDesbloqueo}
        error={acciones.errorDesbloquear}
        desbloqueando={acciones.desbloqueando}
      />

      <ModalRestablecerPassword
        open={acciones.modalRestablecerAbierto}
        onClose={acciones.cerrarRestablecer}
        usuario={acciones.usuarioSeleccionado}
        onConfirmar={acciones.confirmarRestablecer}
        error={acciones.errorRestablecer}
        restableciendo={acciones.restableciendo}
      />
    </div>
  );
};

export default AdminPage;
