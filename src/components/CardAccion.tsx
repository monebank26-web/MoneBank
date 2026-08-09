/**
 * CardAccion.tsx
 * ---------------------------------------------------------
 * Componente HIJO reutilizable.
 * Se usa dentro de las 5 interfaces (Perfil/Usuarios, Bolsillos/Productos,
 * Login, Registro y Transacciones).
 *
 * Comunicación Padre -> Hijo:
 *   El padre le envía título, descripción, texto del botón, ícono y variante
 *   a través de props (definidas en la interface CardAccionProps).
 *
 * Comunicación Hijo -> Padre:
 *   El hijo NO tiene estado propio ni hooks. Cuando el usuario hace clic,
 *   simplemente ejecuta la función que el padre le pasó por props
 *   (onAccion), enviándole como argumento un mensaje describiendo qué pasó.
 *   Es el padre quien decide qué hacer con esa información (alert/console.log).
 */

// La interface obligatoria en TypeScript que define TODAS las props del hijo
export interface CardAccionProps {
  titulo: string;
  descripcion: string;
  textoBoton: string;
  icono?: string;
  variante?: 'normal' | 'peligro' | 'exito';
  // Función de callback: así el hijo "habla" con el padre sin usar hooks
  onAccion: (mensaje: string) => void;
}

function CardAccion(props: CardAccionProps) {
  const { titulo, descripcion, textoBoton, icono, variante = 'normal', onAccion } = props;

  const manejarClick = () => {
    // El hijo arma un mensaje y se lo entrega al padre mediante la función recibida por props.
    onAccion(`Se ejecutó "${textoBoton}" en la tarjeta "${titulo}"`);
  };

  return (
    <div className={`card-accion variante-${variante}`}>
      {icono && <span className="icono">{icono}</span>}
      <h3>{titulo}</h3>
      <p>{descripcion}</p>
      <button type="button" onClick={manejarClick}>
        {textoBoton}
      </button>
    </div>
  );
}

export default CardAccion;
