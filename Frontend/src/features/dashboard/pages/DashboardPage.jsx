import React, { useEffect, useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { useBolsillos } from '../../bolsillos/hooks/useBolsillos';
import { useConsignarSaldo } from '../hooks/useConsignarSaldo';
import { useRegistrarGasto } from '../hooks/useRegistrarGasto';
import { useMovimientosRecientes } from '../hooks/useMovimientosRecientes';
import { obtenerSaludoSegunHora } from '../../../core/utils/saludo';
import { limitesService } from '../../limites/services/limitesService';
import { metasService } from '../../metas/services/metasService';
import { authService } from '../../auth/services/authService';
import TarjetasSaldoInicio from '../components/TarjetasSaldoInicio';
import SeccionBolsillosInicio from '../components/SeccionBolsillosInicio';
import SeccionMovimientosInicio from '../components/SeccionMovimientosInicio';
import ModalConsignar from '../components/ModalConsignar';
import WidgetLimiteCritico from '../components/WidgetLimiteCritico';
import SeccionAhorros from '../components/SeccionAhorros';
import ModalGastoDashboard from '../components/ModalGastoDashboard';
import './DashboardPage.css';

const aNumero = (v) => Number(v) || 0;

const DashboardPage = () => {
  const { user } = useAuth();
  const { bolsillos, loading, totalSaldo } = useBolsillos();
  const { transacciones } = useMovimientosRecientes();
  const consignar = useConsignarSaldo();

  const [saldoCuenta, setSaldoCuenta] = useState(0);
  const [limites, setLimites] = useState([]);
  const [metas, setMetas] = useState([]);
  const [modalGasto, setModalGasto] = useState(false);
  const gasto = useRegistrarGasto({ open: modalGasto, onClose: () => setModalGasto(false), saldoCuenta, limites });

  useEffect(() => {
    authService.obtenerSaldo().then(({ saldo }) => {
      setSaldoCuenta(saldo);
    }).catch(() => {});
    limitesService.listar().then((data) => setLimites(Array.isArray(data) ? data : [])).catch(() => {});
    metasService.listar().then((data) => setMetas(Array.isArray(data) ? data : [])).catch(() => {});
  }, [user]);

  useEffect(() => {
    if (!modalGasto) {
      authService.obtenerSaldo().then(({ saldo }) => setSaldoCuenta(saldo)).catch(() => {});
    }
  }, [modalGasto]);

  const limitesCriticos = [...limites].sort(
    (a, b) => aNumero(b.porcentaje_usado) - aNumero(a.porcentaje_usado)
  );
  const limiteCritico = limitesCriticos[0];

  const metasOrdenadas = [...metas].sort(
    (a, b) => aNumero(b.porcentaje_completado) - aNumero(a.porcentaje_completado)
  );

  const saludo = obtenerSaludoSegunHora();

  return (
    <div className="pagina-inicio">
      <div className="encabezado-inicio">
        <div>
          <p className="saludo-inicio">{saludo},</p>
          <h1 className="nombre-inicio">{user?.nombres}</h1>
        </div>
      </div>

      <div className="tarjeta-saldos-row">
        <TarjetasSaldoInicio
          saldoCuenta={saldoCuenta}
          onConsignar={() => consignar.setModalConsignarAbierto(true)}
          onGasto={() => setModalGasto(true)}
        />
        <WidgetLimiteCritico limiteCritico={limiteCritico} />
      </div>

      <div className="cuerpo-inicio">
        <div className="columna-contenido-inicio">
          <SeccionBolsillosInicio bolsillos={bolsillos} cargando={loading} />
          <SeccionMovimientosInicio transacciones={transacciones} />
        </div>

        <SeccionAhorros
          limites={limites}
          metas={metas}
          limitesCriticos={limitesCriticos}
          metasOrdenadas={metasOrdenadas}
        />
      </div>

      <ModalConsignar
        open={consignar.modalConsignarAbierto}
        onClose={() => consignar.setModalConsignarAbierto(false)}
        saldoActual={saldoCuenta}
        monto={consignar.montoConsignar}
        setMonto={consignar.setMontoConsignar}
        error={consignar.errorConsignar}
        onConsignar={consignar.handleConsignar}
      />

      <ModalGastoDashboard
        open={modalGasto}
        saldoCuenta={saldoCuenta}
        {...gasto}
      />
    </div>
  );
};

export default DashboardPage;
