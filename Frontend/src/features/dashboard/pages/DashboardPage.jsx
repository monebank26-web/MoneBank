import React, { useEffect, useState } from 'react';
import { useAuth } from '../../../core/context/AuthContext';
import { useBolsillos } from '../../bolsillos/hooks/useBolsillos';
import { useIngreso } from '../hooks/useIngreso';
import { useRegistrarGasto } from '../hooks/useRegistrarGasto';
import { useMovimientosRecientes } from '../hooks/useMovimientosRecientes';
import { obtenerSaludoSegunHora } from '../../../core/utils/saludo';
import { limitesService } from '../../limites/services/limitesService';
import { metasService } from '../../metas/services/metasService';
import { authService } from '../../auth/services/authService';
import TarjetasSaldoInicio from '../components/TarjetasSaldoInicio';
import SeccionBolsillosInicio from '../components/SeccionBolsillosInicio';
import SeccionMovimientosInicio from '../components/SeccionMovimientosInicio';
import WidgetLimiteCritico from '../components/WidgetLimiteCritico';
import SeccionAhorros from '../components/SeccionAhorros';
import ModalIngresoDashboard from '../components/ModalIngresoDashboard';
import ModalGastoDashboard from '../components/ModalGastoDashboard';
import './DashboardPage.css';

const aNumero = (v) => Number(v) || 0;

const DashboardPage = () => {
  const { user } = useAuth();
  const { bolsillos, loading } = useBolsillos();
  const ingreso = useIngreso();
  const { transacciones } = useMovimientosRecientes();

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


  const handleIngresoCerrado = (nuevoSaldo) => {
    ingreso.cerrarIngreso();
    if (nuevoSaldo !== undefined) setSaldoCuenta(nuevoSaldo);
  };

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
          onIngreso={ingreso.abrirIngreso}
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
