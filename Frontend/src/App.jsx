import React from 'react';
import { AuthProvider } from './core/context/AuthContext';
import { ThemeProvider } from './core/context/ThemeContext';
import AppRouter from './core/routes/router';
import './shared/styles/global.css';

const App = () => (
  <ThemeProvider>
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  </ThemeProvider>
);

export default App;

