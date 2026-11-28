import React, { createContext, useContext, useState, useEffect } from 'react';
import { STORAGE_KEYS } from '../constants';
import {
  guardarToken,
  leerExp,
  limpiarSesion,
  obtenerToken,
  redirigirAlLogin,
  suscribirse,
  tokenVigente,
} from '../utils/tokenSesion';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [motivo, setMotivo] = useState(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    const unsubscribe = suscribirse((evento) => {
      if (evento.tipo === 'logout') {
        setUser(null);
        setMotivo(evento.motivo);
      } else {
        setMotivo(null);
        setVersion((v) => v + 1);
      }
    });

    const guardado = localStorage.getItem(STORAGE_KEYS.USER);
    if (guardado && tokenVigente()) {
      setUser(JSON.parse(guardado));
    } else {
      limpiarSesion();
    }
    setLoading(false);

    return unsubscribe;
  }, []);

  useEffect(() => {
    if (!user) return undefined;

    const expirar = () => {
      limpiarSesion({ motivo: 'expirada' });
      redirigirAlLogin('expirada');
    };

    const restante =
      leerExp(obtenerToken()) * 1000 - Date.now();
    if (restante <= 0) {
      expirar();
      return undefined;
    }

    const timer = setTimeout(expirar, restante);
    const revisar = () => {
      if (!tokenVigente()) expirar();
    };
    document.addEventListener('visibilitychange', revisar);

    return () => {
      clearTimeout(timer);
      document.removeEventListener('visibilitychange', revisar);
    };
  }, [user, version]);

  const login = (userData) => {
    const { access_token, ...userInfo } = userData;
    const userToSave = {
      ...userInfo,
      id: userInfo.id || userInfo.usuario_id || Date.now().toString(),
    };
    localStorage.setItem(
      STORAGE_KEYS.USER,
      JSON.stringify(userToSave)
    );
    if (access_token) {
      guardarToken(access_token);
    }
    setUser(userToSave);
  };

  const logout = () => {
    limpiarSesion({
      borrarChat: true,
      userId: user?.id,
    });
    setUser(null);
  };

  const isAuthenticated = !!user && tokenVigente();

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated,
        loading,
        motivo,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de AuthProvider');
  return ctx;
};
