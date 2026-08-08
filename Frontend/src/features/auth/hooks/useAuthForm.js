import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../core/context/AuthContext';
import { authService } from '../services/authService';
import { ROUTES } from '../../../core/constants';

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
        user = await authService.register(formData);
      }
      login(user);
      navigate(ROUTES.DASHBOARD);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { submit, loading, error };
};
