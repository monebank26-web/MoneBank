// core/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { STORAGE_KEYS } from '../constants';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem(STORAGE_KEYS.USER);
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = (userData) => {
    const userToSave = { ...userData, id: userData.id || Date.now().toString() };
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(userToSave));
    localStorage.setItem(STORAGE_KEYS.TOKEN, 'local-token-' + userToSave.id);
    setUser(userToSave);
  };

  const logout = () => {
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.TOKEN);
    setUser(null);
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return ctx;
};
