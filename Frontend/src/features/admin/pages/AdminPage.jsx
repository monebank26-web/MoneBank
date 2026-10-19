import React from 'react';
import { Icon } from '@iconify/react';
import Paginacion from '../../transacciones/components/Paginacion';
import '../../../shared/styles/transacciones-modal.css';
import { useUsuariosAdmin } from '../hooks/useUsuariosAdmin';
import { useAccionesUsuarioAdmin } from '../hooks/useAccionesUsuarioAdmin';
import { mensajeVacio, textoTotalUsuarios } from '../utils/usuariosAdmin';
import BarraFiltrosUsuarios from '../components/BarraFiltrosUsuarios';
import FilaUsuarioAdmin from '../components/FilaUsuarioAdmin';
import ModalDetalleUsuario from '../components/ModalDetalleUsuario';
import ModalEditarUsuario from '../components/ModalEditarUsuario';
import ModalEliminarUsuario from '../components/ModalEliminarUsuario';
import './AdminPage.css';

const AdminPage = () => {
  const {
    usuarios,
    total,
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

  return (
    <div className="admin-pagina">
      <div className="admin-encabezado">
        <div>
          <h1 className="admin-titulo">Panel de administrador</h1>
          <p className="admin-subtitulo">Gestiona las cuentas de MoneBank.</p>
        </div>

        <div className="admin-encabezado__lado">
          {acciones.mensaje && (
            <span className="admin-mensaje-exito">
              <Icon icon="mdi:check-circle-outline" />
              {acciones.mensaje}
            </span>
          )}
          <span className="admin-total">{textoTotalUsuarios(total)}</span>
        </div>
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
          <div className="admin-lista">
            {usuarios.map((usuario) => (
              <FilaUsuarioAdmin
                key={usuario.id}
                usuario={usuario}
                onVerDetalle={acciones.abrirDetalle}
                onEditar={acciones.abrirEditar}
              />
            ))}
          </div>

          <Paginacion pagina={pagina} totalPaginas={totalPaginas} onChange={setPagina} />
        </>
      )}

      <ModalDetalleUsuario
        open={acciones.modalDetalleAbierto}
        onClose={() => acciones.setModalDetalleAbierto(false)}
        usuario={acciones.usuarioSeleccionado}
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

      <ModalEliminarUsuario
        open={acciones.modalEliminarAbierto}
        onClose={() => acciones.setModalEliminarAbierto(false)}
        usuario={acciones.usuarioSeleccionado}
        onConfirmar={acciones.eliminarUsuario}
      />
    </div>
  );
};

export default AdminPage;
