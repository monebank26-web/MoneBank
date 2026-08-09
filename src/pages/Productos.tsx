import CardAccion from '../components/CardAccion';

/**
 * Productos.tsx  →  en MoneBank el "producto" que el usuario administra
 * son sus BOLSILLOS (cuentas de ahorro segmentadas), por eso esta interfaz
 * se adapta a ese concepto en lugar de un catálogo de productos genérico.
 *
 * Este componente es el PADRE de CardAccion.
 */

export interface Bolsillo {
  nombre: string;
  saldo: number;
}

export interface ProductosProps {
  bolsillos: Bolsillo[];
}

function Productos({ bolsillos }: ProductosProps) {
  const manejarAccionBolsillo = (mensaje: string) => {
    alert(`[Módulo Productos/Bolsillos] ${mensaje}`);
    console.log('[Productos/Bolsillos]', mensaje);
  };

  return (
    <section>
      <div className="page-header">
        <h2>Productos · Bolsillos</h2>
        <span>Tienes {bolsillos.length} bolsillos activos</span>
      </div>

      <div className="cards-grid">
        {bolsillos.map((b) => (
          <CardAccion
            key={b.nombre}
            titulo={b.nombre}
            descripcion={`Saldo actual: $${b.saldo.toLocaleString('es-CO')}`}
            textoBoton="Depositar"
            icono="💰"
            variante="exito"
            onAccion={manejarAccionBolsillo}
          />
        ))}
        <CardAccion
          titulo="Nuevo bolsillo"
          descripcion="Crea un bolsillo para una meta de ahorro nueva."
          textoBoton="Crear"
          icono="➕"
          onAccion={manejarAccionBolsillo}
        />
      </div>
    </section>
  );
}

export default Productos;
