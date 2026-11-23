import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../services/authService';
import { ROUTES } from '../../../core/constants';
import { esAdministrador } from '../../../core/utils/permisos';

export const useAuthForm = (mode = 'login') => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const submit = async (formData) => {
    setLoading(true);
    setError('');
    try {
      let user;
      if (mode === 'login') {
        user = await authService.login(formData);
      } else {
        await authService.register(formData);
        user = await authService.login({ 
          email: formData.email, 
          password: formData.password 
        });
      }
      login(user);
      navigate(esAdministrador(user) ? ROUTES.ADMIN : ROUTES.DASHBOARD);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { submit, loading, error };
};
