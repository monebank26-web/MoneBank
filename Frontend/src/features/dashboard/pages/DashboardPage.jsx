import React, { useEffect, useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { useIngreso } from '../hooks/useIngreso';
import { useRegistrarGasto } from '../hooks/useRegistrarGasto';
import { useMovimientosRecientes } from '../hooks/useMovimientosRecientes';
import { obtenerSaludoSegunHora } from '../../../core/utils/saludo';
import { limitesService } from '../../limites/services/limitesService';
import { metasService } from '../../metas/services/metasService';
import { authService } from '../../auth/services/authService';
import TarjetasSaldoInicio from '../components/TarjetasSaldoInicio';
import WidgetLimiteCritico from '../components/WidgetLimiteCritico';
import SeccionChatInicio from '../components/SeccionChatInicio';
import SeccionMovimientosInicio from '../components/SeccionMovimientosInicio';
import SeccionAhorros from '../components/SeccionAhorros';
import ModalIngresoDashboard from '../components/ModalIngresoDashboard';
import ModalGastoDashboard from '../components/ModalGastoDashboard';
import './DashboardPage.css';

const aNumero = (v) => Number(v) || 0;

const DashboardPage = () => {
  const { user } = useAuth();
  const ingreso = useIngreso();
  const { transacciones } = useMovimientosRecientes(4);

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

  const metasOrdenadas = [...metas].sort(
    (a, b) => aNumero(b.porcentaje_completado) - aNumero(a.porcentaje_completado)
  );

  const saludo = obtenerSaludoSegunHora();

  const handleIngresoCerrado = (nuevoSaldo) => {
    ingreso.cerrarIngreso();
    if (nuevoSaldo !== undefined) setSaldoCuenta(nuevoSaldo);
  };

  return (
    <div className="pagina-inicio">
      <div className="encabezado-dashboard">
        <h1 className="titulo-dashboard">
          <span className="saludo-dashboard">{saludo},</span>{' '}
          <strong className="nombre-dashboard">{user?.nombres}</strong>
        </h1>
      </div>

      <div className="fila-saldos">
        <TarjetasSaldoInicio
          saldoCuenta={saldoCuenta}
          onIngreso={ingreso.abrirIngreso}
          onGasto={() => setModalGasto(true)}
        />
        <WidgetLimiteCritico limites={limites} limiteCritico={limitesCriticos[0]} />
      </div>

      <SeccionChatInicio />

      <div className="cuerpo-inicio">
        <SeccionMovimientosInicio transacciones={transacciones} />
        <SeccionAhorros
          limites={limites}
          metas={metas}
          limitesCriticos={limitesCriticos}
          metasOrdenadas={metasOrdenadas}
        />
      </div>

      <ModalIngresoDashboard
        open={ingreso.modalIngresoAbierto}
        onClose={handleIngresoCerrado}
        saldoCuenta={saldoCuenta}
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