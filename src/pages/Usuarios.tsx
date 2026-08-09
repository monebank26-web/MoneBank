import CardAccion from '../components/CardAccion';

/**
 * Usuarios.tsx  →  en MoneBank equivale a "Perfil / Cuenta" del usuario,
 * ya que este proyecto no maneja un catálogo de usuarios administrables,
 * sino la cuenta y el perfil de la persona que ingresa a la banca.
 *
 * Este componente es el PADRE de CardAccion.
 */

export interface UsuariosProps {
  nombreUsuario: string;
  correo: string;
}

function Usuarios({ nombreUsuario, correo }: UsuariosProps) {
  // Funciones que el padre pasa al hijo (Hijo -> Padre por callback)
  const manejarAccionPerfil = (mensaje: string) => {
    alert(`[Módulo Usuarios/Perfil] ${mensaje}`);
    console.log('[Usuarios/Perfil]', mensaje);
  };

  return (
    <section>
      <div className="page-header">
        <h2>Usuarios · Perfil y Cuenta</h2>
        <span>
          Sesión de {nombreUsuario} ({correo})
        </span>
      </div>

      <div className="cards-grid">
        <CardAccion
          titulo="Editar perfil"
          descripcion="Actualiza tu nombre, foto y datos de contacto."
          textoBoton="Editar"
          icono="👤"
          onAccion={manejarAccionPerfil}
        />
        <CardAccion
          titulo="Cambiar contraseña"
          descripcion="Genera una nueva contraseña segura para tu cuenta."
          textoBoton="Cambiar"
          icono="🔒"
          variante="peligro"
          onAccion={manejarAccionPerfil}
        />
        <CardAccion
          titulo="Verificar identidad"
          descripcion="Confirma tus datos para desbloquear límites más altos."
          textoBoton="Verificar"
          icono="✅"
          variante="exito"
          onAccion={manejarAccionPerfil}
        />
      </div>
    </section>
  );
}

export default Usuarios;
