
const formatoMoneda = (valor) =>
  new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    maximumFractionDigits: 0,
  }).format(valor);

const formatoFecha = (fecha) =>
  new Date(fecha).toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  });

const aNumero = (v) => Number(v) || 0;

export const ReporteResumen = ({ data, titulo = 'Reporte del periodo' }) => {
  if (!data) return null;

  const balancePositivo = data.balance >= 0;
  const totalMetas = aNumero(data.total_metas);

  return (
    <div className="card">
      <h3>{titulo}</h3>
      <p className="periodo">
        {formatoFecha(data.periodo_inicio)} — {formatoFecha(data.periodo_fin)}
      </p>

      <div className="resumen-grid">
        <div className="resumen-item ingreso">
          <span>Ingresos</span>
          <strong>{formatoMoneda(data.total_ingresos)}</strong>
        </div>
        <div className="resumen-item gasto">
          <span>Gastos</span>
          <strong>{formatoMoneda(data.total_gastos)}</strong>
        </div>
        <div className={`resumen-item balance ${balancePositivo ? 'positivo' : 'negativo'}`}>
          <span>Balance</span>
          <strong>{formatoMoneda(data.balance)}</strong>
        </div>
        <div className="resumen-item meta">
          <span>Metas</span>
          <strong>{formatoMoneda(totalMetas)}</strong>
        </div>
      </div>
    </div>
  );
};