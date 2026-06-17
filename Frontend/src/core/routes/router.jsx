// core/routes/router.jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ROUTES } from '../constants';

// Pages
import LoginPage from '../../features/auth/pages/LoginPage';
import RegisterPage from '../../features/auth/pages/RegisterPage';
import DashboardPage from '../../features/dashboard/pages/DashboardPage';
import BolsillosPage from '../../features/bolsillos/pages/BolsillosPage';
import TransaccionesPage from '../../features/transacciones/pages/TransaccionesPage';

// Layout
import MainLayout from '../../shared/layouts/MainLayout';

// Rutas protegidas
const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <div style={{ color: 'white', padding: 40 }}>Cargando...</div>;
  return isAuthenticated ? <MainLayout>{children}</MainLayout> : <Navigate to={ROUTES.LOGIN} replace />;
};

// Rutas públicas (redirige si ya está autenticado)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  return !isAuthenticated ? children : <Navigate to={ROUTES.DASHBOARD} replace />;
};

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      {/* Públicas */}
      <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />

      {/* Privadas */}
      <Route path="/dashboard" element={<PrivateRoute><DashboardPage /></PrivateRoute>} />
      <Route path="/bolsillos" element={<PrivateRoute><BolsillosPage /></PrivateRoute>} />
      <Route path="/transacciones" element={<PrivateRoute><TransaccionesPage /></PrivateRoute>} />

      {/* Redirección raíz */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
