import React from 'react';
import { useResumenSemanal } from '../hooks/useResumenSemanal';
import { ResumenSemanalCard } from '../components/ResumenSemanalCard';
import '../styles/analytics-cards.css';

export const ResumenSemanalPage = () => {
  const { data, loading, error, recargar } = useResumenSemanal();

  if (loading) {
    return <div style={{ padding: '24px', textAlign: 'center', color: 'var(--color-text)' }}>Cargando resumen semanal...</div>;
  }

  if (error) {
    return (
      <div style={{ padding: '24px', color: 'var(--color-danger)' }}>
        <p>{error}</p>
        <button
          onClick={recargar}
          style={{
            marginTop: '12px',
            padding: '8px 16px',
            backgroundColor: 'var(--color-accent)',
            color: '#080808',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            fontWeight: 600,
          }}
        >
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '640px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: '1.75rem', color: 'var(--color-text)' }}>
          Resumen Semanal
        </h1>
        <button
          onClick={recargar}
          style={{
            padding: '8px 16px',
            backgroundColor: 'var(--color-accent)',
            color: '#080808',
            border: 'none',
            borderRadius: 'var(--radius-sm)',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Actualizar
        </button>
      </div>

      <ResumenSemanalCard data={data} />
    </div>
  );
};

export default ResumenSemanalPage;