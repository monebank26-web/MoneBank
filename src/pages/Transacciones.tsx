import CardAccion from '../components/CardAccion';

/**
 * Transacciones.tsx  →  tercer módulo elegido libremente (además de
 * Login y Registro), ya que MoneBank ya cuenta con historial de
 * transacciones dentro del proyecto real.
 */

export interface Movimiento {
  descripcion: string;
  monto: number;
}

export interface TransaccionesProps {
  movimientos: Movimiento[];
}

function Transacciones({ movimientos }: TransaccionesProps) {
  const manejarAccionMovimiento = (mensaje: string) => {
    alert(`[Módulo Transacciones] ${mensaje}`);
    console.log('[Transacciones]', mensaje);
  };

  return (
    <section>
      <div className="page-header">
        <h2>Transacciones</h2>
        <span>Últimos movimientos de tus bolsillos</span>
      </div>

      <div className="cards-grid">
        {movimientos.map((m) => (
          <CardAccion
            key={m.descripcion}
            titulo={m.descripcion}
            descripcion={`Monto: $${m.monto.toLocaleString('es-CO')}`}
            textoBoton="Ver detalle"
            icono={m.monto >= 0 ? '📈' : '📉'}
            variante={m.monto >= 0 ? 'exito' : 'peligro'}
            onAccion={manejarAccionMovimiento}
          />
        ))}
      </div>
    </section>
  );
}

export default Transacciones;
