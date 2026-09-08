
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ROUTES, ROLES } from '../constants';
import HomePage from '../../features/Home/pages/HomePage';
import LoginPage from '../../features/auth/pages/LoginPage';
import RegisterPage from '../../features/auth/pages/RegisterPage';
import DashboardPage from '../../features/dashboard/pages/DashboardPage';
import ChatPage from '../../features/chat/pages/ChatPage';
import MetasPage from '../../features/metas/pages/MetasPage';
import LimitesPage from '../../features/limites/pages/LimitesPage';
import TransaccionesPage from '../../features/transacciones/pages/TransaccionesPage';
import AdminPage from '../../features/admin/pages/AdminPage';
import PerfilPage from '../../features/perfil/pages/PerfilPage';
import MainLayout from '../../shared/layouts/MainLayout';
import ControlParentalDashboardPage from '../../features/controlParental/pages/ControlParentalDashboardPage';

import { GraficasPage } from '../../features/analytics/pages/GraficasPage';
import { ResumenSemanalPage } from '../../features/analytics/pages/ResumenSemanalPage';
import { ReportesPage } from '../../features/analytics/pages/ReportesPage';

const RutaPrivada = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div style={{ color: 'white', padding: 40 }}>Cargando...</div>;
  return isAuthenticated
    ? <MainLayout>{children}</MainLayout>
    : <Navigate to={ROUTES.LOGIN} replace />;
};

const RutaAdmin = ({ children }) => {
  const { isAuthenticated, user, loading } = useAuth();
  if (loading) return <div style={{ color: 'white', padding: 40 }}>Cargando...</div>;
  if (!isAuthenticated) return <Navigate to={ROUTES.LOGIN} replace />;
  if (user?.rol !== ROLES.ADMIN) return <Navigate to={ROUTES.DASHBOARD} replace />;
  return <MainLayout>{children}</MainLayout>;
};


const RutaPublica = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  return !isAuthenticated ? children : <Navigate to={ROUTES.DASHBOARD} replace />;
};

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      {/* Página principal: SIEMPRE accesible, tengas sesión o no.
          A diferencia de RutaPublica, esta NO redirige si ya estás logueado,
          porque justamente queremos poder volver aquí desde adentro de la app. */}
      <Route path={ROUTES.HOME} element={<HomePage />} />

      {/* Públicas */}
      <Route path="/login" element={<RutaPublica><LoginPage /></RutaPublica>} />
      <Route path="/register" element={<RutaPublica><RegisterPage /></RutaPublica>} />

      {/* Privadas generales */}
      <Route path="/dashboard" element={<RutaPrivada><DashboardPage /></RutaPrivada>} />
      <Route path="/chat" element={<RutaPrivada><ChatPage /></RutaPrivada>} />
      <Route path="/metas" element={<RutaPrivada><MetasPage /></RutaPrivada>} />
      <Route path="/limites" element={<RutaPrivada><LimitesPage /></RutaPrivada>} />
      <Route path="/transacciones" element={<RutaPrivada><TransaccionesPage /></RutaPrivada>} />
      <Route path="/perfil" element={<RutaPrivada><PerfilPage /></RutaPrivada>} />
      <Route path="/control-parental"element={<RutaPrivada><ControlParentalDashboardPage /></RutaPrivada>}/>

      <Route path={ROUTES.GRAFICAS} element={<RutaPrivada><GraficasPage /></RutaPrivada>} />
      <Route path={ROUTES.RESUMEN_SEMANAL} element={<RutaPrivada><ResumenSemanalPage /></RutaPrivada>} />
      <Route path={ROUTES.REPORTES} element={<RutaPrivada><ReportesPage /></RutaPrivada>} />
      

      {/* Solo admin */}
      <Route path="/admin" element={<RutaAdmin><AdminPage /></RutaAdmin>} />

      {/* Cualquier ruta desconocida */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
