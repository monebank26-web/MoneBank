// App.jsx
import React from 'react';
import { AuthProvider } from './core/context/AuthContext';
import AppRouter from './core/routes/router';
import './shared/styles/global.css';

const App = () => (
  <AuthProvider>
    <AppRouter />
  </AuthProvider>
);

export default App;
