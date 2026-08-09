import CardAccion from '../components/CardAccion';

/**
 * Login.tsx
 * PROHIBIDO usar hooks (ni useState, ni useRef, etc.).
 * Por eso el formulario es "no controlado": en vez de guardar cada
 * tecleo en un estado, leemos los valores directamente del DOM
 * (FormData) SOLO en el momento del submit.
 */

export interface LoginProps {
  nombreModulo: string;
}

function Login({ nombreModulo }: LoginProps) {
  const manejarSubmit = (evento: React.FormEvent<HTMLFormElement>) => {
    evento.preventDefault();
    const formulario = evento.currentTarget;
    const datos = new FormData(formulario);

    const usuario = datos.get('usuario') as string;
    const contrasena = datos.get('contrasena') as string;

    alert(
      `[${nombreModulo}] Intento de inicio de sesión\nUsuario: ${usuario}\nContraseña: ${contrasena}`
    );
    console.log('[Login] submit ->', { usuario, contrasena });
  };

  const manejarAccionAyuda = (mensaje: string) => {
    alert(`[Módulo Login] ${mensaje}`);
    console.log('[Login]', mensaje);
  };

  return (
    <section>
      <div className="page-header">
        <h2>{nombreModulo}</h2>
        <span>Ingresa con tu usuario y contraseña</span>
      </div>

      <form className="auth-form" onSubmit={manejarSubmit}>
        <label>
          Usuario o correo
          <input type="text" name="usuario" placeholder="usuario@correo.com" required />
        </label>
        <label>
          Contraseña
          <input type="password" name="contrasena" placeholder="••••••••" required />
        </label>
        <button type="submit">Ingresar</button>
      </form>

      <div className="cards-grid">
        <CardAccion
          titulo="¿Olvidaste tu contraseña?"
          descripcion="Recupera el acceso a tu cuenta MoneBank."
          textoBoton="Recuperar"
          icono="🔑"
          onAccion={manejarAccionAyuda}
        />
      </div>
    </section>
  );
}

export default Login;
