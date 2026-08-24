import React from 'react';
import { useUsuariosAdmin } from '../hooks/useUsuariosAdmin';
import { useAccionesUsuarioAdmin } from '../hooks/useAccionesUsuarioAdmin';
import BarraFiltrosUsuarios from '../components/BarraFiltrosUsuarios';
import FilaUsuarioAdmin from '../components/FilaUsuarioAdmin';
import ModalDetalleUsuario from '../components/ModalDetalleUsuario';
import ModalEditarUsuario from '../components/ModalEditarUsuario';
import ModalEliminarUsuario from '../components/ModalEliminarUsuario';
import './AdminPage.css';

const AdminPage = () => {
  const {
    usuarios,
    usuariosFiltrados,
    busqueda,
    setBusqueda,
    filtroRol,
    setFiltroRol,
    cargarUsuarios,
    obtenerUsuarioVinculado,
  } = useUsuariosAdmin();

  const acciones = useAccionesUsuarioAdmin({ cargarUsuarios });

  return (
    <div className="pagina-admin">
      <div className="encabezado-admin">
        <div>
          <h1 className="titulo-admin">Panel de administrador</h1>
          <p className="subtitulo-admin">{usuarios.length} usuarios registrados</p>
        </div>
        {acciones.mensaje && <div className="mensaje-exito-admin">{acciones.mensaje}</div>}
      </div>

      <BarraFiltrosUsuarios
        busqueda={busqueda}
        setBusqueda={setBusqueda}
        filtroRol={filtroRol}
        setFiltroRol={setFiltroRol}
      />

      {usuariosFiltrados.length === 0 ? (
        <div className="admin-sin-resultados">
          <p>No se encontraron usuarios con ese criterio.</p>
        </div>
      ) : (
        <div className="tabla-admin">
          {usuariosFiltrados.map((usuario) => (
            <FilaUsuarioAdmin
              key={usuario.id}
              usuario={usuario}
              onVerDetalle={acciones.abrirDetalle}
              onEditar={acciones.abrirEditar}
              onEliminar={acciones.abrirEliminar}
            />
          ))}
        </div>
      )}

      <ModalDetalleUsuario
        open={acciones.modalDetalleAbierto}
        onClose={() => acciones.setModalDetalleAbierto(false)}
        usuario={acciones.usuarioSeleccionado}
        usuarioVinculado={acciones.usuarioSeleccionado ? obtenerUsuarioVinculado(acciones.usuarioSeleccionado) : null}
      />

      <ModalEditarUsuario
        open={acciones.modalEditarAbierto}
        onClose={() => acciones.setModalEditarAbierto(false)}
        formulario={acciones.formularioEdicion}
        setFormulario={acciones.setFormularioEdicion}
        onGuardar={acciones.guardarEdicion}
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
