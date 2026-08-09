import CardAccion from '../components/CardAccion';

export interface RegistroProps {
  nombreModulo: string;
}

function Registro({ nombreModulo }: RegistroProps) {
  const manejarSubmit = (evento: React.FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    const formulario = evento.currentTarget;
    const datos = new FormData(formulario);

    const nombre = datos.get('nombre') as string;
    const correo = datos.get('correo') as string;
    const contrasena = datos.get('contrasena') as string;

    alert(
      `[${nombreModulo}] Nuevo registro\nNombre: ${nombre}\nCorreo: ${correo}\nContraseña: ${contrasena}`
    );
    console.log('[Registro] submit ->', { nombre, correo, contrasena });
  };

  const manejarAccionInfo = (mensaje: string) => {
    alert(`[Módulo Registro] ${mensaje}`);
    console.log('[Registro]', mensaje);
  };

  return (
    <section>
      <div className="page-header">
        <h2>{nombreModulo}</h2>
        <span>Crea tu cuenta en MoneBank</span>
      </div>

      <form className="auth-form" onSubmit={manejarSubmit}>
        <label>
          Nombre completo
          <input type="text" name="nombre" placeholder="Nombre y apellido" required />
        </label>
        <label>
          Correo electrónico
          <input type="email" name="correo" placeholder="usuario@correo.com" required />
        </label>
        <label>
          Contraseña
          <input type="password" name="contrasena" placeholder="••••••••" required />
        </label>
        <button type="submit">Registrarme</button>
      </form>

      <div className="cards-grid">
        <CardAccion
          titulo="Términos y condiciones"
          descripcion="Revisa las políticas de uso antes de registrarte."
          textoBoton="Ver términos"
          icono="📄"
          onAccion={manejarAccionInfo}
        />
      </div>
    </section>
  );
}

export default Registro;
