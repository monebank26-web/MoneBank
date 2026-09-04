
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ROUTES, ROLES } from '../constants';
import LoginPage from '../../features/auth/pages/LoginPage';
import RegisterPage from '../../features/auth/pages/RegisterPage';
import DashboardPage from '../../features/dashboard/pages/DashboardPage';
import ChatPage from '../../features/chat/pages/ChatPage';
import MetasPage from '../../features/metas/pages/MetasPage';
import LimitesPage from '../../features/limites/pages/LimitesPage';
import TransaccionesPage from '../../features/transacciones/pages/TransaccionesPage';
import AdminPage from '../../features/admin/pages/AdminPage';
import ControlParentalPadrePage from '../../features/controlParental/pages/ControlParentalPadrePage';
import ControlParentalHijoPage from '../../features/controlParental/pages/ControlParentalHijoPage';
import PerfilPage from '../../features/perfil/pages/PerfilPage';
import MainLayout from '../../shared/layouts/MainLayout';

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

const RutaPadre = ({ children }) => {
  const { isAuthenticated, user, loading } = useAuth();
  if (loading) return <div style={{ color: 'white', padding: 40 }}>Cargando...</div>;
  if (!isAuthenticated) return <Navigate to={ROUTES.LOGIN} replace />;
  if (user?.rol !== ROLES.PADRE) return <Navigate to={ROUTES.DASHBOARD} replace />;
  return <MainLayout>{children}</MainLayout>;
};

const RutaHijo = ({ children }) => {
  const { isAuthenticated, user, loading } = useAuth();
  if (loading) return <div style={{ color: 'white', padding: 40 }}>Cargando...</div>;
  if (!isAuthenticated) return <Navigate to={ROUTES.LOGIN} replace />;
  if (user?.rol !== ROLES.HIJO) return <Navigate to={ROUTES.DASHBOARD} replace />;
  return <MainLayout>{children}</MainLayout>;
};

const ControlParentalRedirect = () => {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (user?.rol === ROLES.PADRE) return <Navigate to={ROUTES.CONTROL_PARENTAL_PADRE} replace />;
  if (user?.rol === ROLES.HIJO) return <Navigate to={ROUTES.CONTROL_PARENTAL_HIJO} replace />;
  return <Navigate to={ROUTES.DASHBOARD} replace />;
};

const RutaPublica = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  return !isAuthenticated ? children : <Navigate to={ROUTES.DASHBOARD} replace />;
};

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      {/* Públicas */}
      <Route path="/login" element={<RutaPublica><LoginPage /></RutaPublica>} />
      <Route path="/register" element={<RutaPublica><RegisterPage /></RutaPublica>} />

      {/* Privadas generales */}
      <Route path="/dashboard" element={<RutaPrivada><DashboardPage /></RutaPrivada>} />
      <Route path="/chat" element={<RutaPrivada><ChatPage /></RutaPrivada>} />
      <Route path="/metas" element={<RutaPrivada><MetasPage /></RutaPrivada>} />
      <Route path="/limites" element={<RutaPrivada><LimitesPage /></RutaPrivada>} />
      <Route path="/transacciones" element={<RutaPrivada><TransaccionesPage /></RutaPrivada>} />
      <Route path="/control-parental" element={<RutaPrivada><ControlParentalRedirect /></RutaPrivada>} />
      <Route path="/control-parental/padre" element={<RutaPadre><ControlParentalPadrePage /></RutaPadre>} />
      <Route path="/control-parental/hijo" element={<RutaHijo><ControlParentalHijoPage /></RutaHijo>} />
      <Route path="/perfil" element={<RutaPrivada><PerfilPage /></RutaPrivada>} />

      {/* Solo admin */}
      <Route path="/admin" element={<RutaAdmin><AdminPage /></RutaAdmin>} />

      {/* Redirección raíz */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
