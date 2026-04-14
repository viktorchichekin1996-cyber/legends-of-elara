import { useEffect } from 'react';
import { authStore } from '../store/authStore';

export function useAuth() {
  const { token, user, isAuthenticated, isLoading, error, login, checkAuth, logout, clearError } = authStore();

  // Авто-проверка при монтировании
  useEffect(() => {
    if (token && !user && !isLoading) {
      checkAuth();
    }
  }, [token, user, isLoading, checkAuth]);

  return {
    token,
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    clearError,
  };
}