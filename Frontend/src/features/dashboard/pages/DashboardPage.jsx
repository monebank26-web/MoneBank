import React from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { useBolsillos } from '../../bolsillos/hooks/useBolsillos';
import { useConsignarSaldo } from '../hooks/useConsignarSaldo';
import { useMovimientosRecientes } from '../hooks/useMovimientosRecientes';
import { obtenerSaludoSegunHora } from '../../../core/utils/saludo';
import TarjetasSaldoInicio from '../components/TarjetasSaldoInicio';
import SeccionBolsillosInicio from '../components/SeccionBolsillosInicio';
import SeccionMovimientosInicio from '../components/SeccionMovimientosInicio';
import ModalConsignar from '../components/ModalConsignar';
import './DashboardPage.css';

const DashboardPage = () => {
  const { user } = useAuth();
  const { bolsillos, loading, totalSaldo } = useBolsillos();
  const { transacciones } = useMovimientosRecientes();
  const consignar = useConsignarSaldo();

  const saludo = obtenerSaludoSegunHora();

  return (
    <div className="pagina-inicio">
      <div className="encabezado-inicio">
        <div>
          <p className="saludo-inicio">{saludo},</p>
          <h1 className="nombre-inicio">{user?.nombre}</h1>
        </div>
      </div>

      <TarjetasSaldoInicio
        saldoCuenta={user?.saldoCuenta || 0}
        totalBolsillos={totalSaldo}
        cantidadBolsillos={bolsillos.length}
        onConsignar={() => consignar.setModalConsignarAbierto(true)}
      />

      <SeccionBolsillosInicio bolsillos={bolsillos} cargando={loading} />

      <SeccionMovimientosInicio transacciones={transacciones} />

      <ModalConsignar
        open={consignar.modalConsignarAbierto}
        onClose={() => consignar.setModalConsignarAbierto(false)}
        saldoActual={user?.saldoCuenta || 0}
        monto={consignar.montoConsignar}
        setMonto={consignar.setMontoConsignar}
        error={consignar.errorConsignar}
        onConsignar={consignar.handleConsignar}
      />
    </div>
  );
};

export default DashboardPage;
