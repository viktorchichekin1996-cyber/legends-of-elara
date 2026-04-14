import { create } from 'zustand';
import { localStorageUtil } from '../utils/localStorage';
import { authService, TokenResponse, UserResponse } from '../services/authService';

interface AuthState {
  token: string | null;
  refreshToken: string | null;
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  setTokens: (tokens: TokenResponse) => void;
  setUser: (user: UserResponse) => void;
  login: (initData: string) => Promise<void>;
  checkAuth: () => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export const authStore = create<AuthState>((set, get) => ({
  token: localStorageUtil.get<string>('token') || null,
  refreshToken: localStorageUtil.get<string>('refreshToken') || null,
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  setTokens: (tokens) => {
    localStorageUtil.set('token', tokens.access_token);
    localStorageUtil.set('refreshToken', tokens.refresh_token);
    set({
      token: tokens.access_token,
      refreshToken: tokens.refresh_token,
      isAuthenticated: true,
    });
  },

  setUser: (user) => {
    set({ user, isAuthenticated: true });
  },

  login: async (initData) => {
    set({ isLoading: true, error: null });
    try {
      const tokens = await authService.loginWithVk(initData);
      get().setTokens(tokens);
      
      // Загружаем данные пользователя
      const user = await authService.getCurrentUser();
      get().setUser(user);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка авторизации';
      set({ error: message, isAuthenticated: false });
      get().logout();
      throw err;
    } finally {
      set({ isLoading: false });
    }
  },

  checkAuth: async () => {
    const token = get().token;
    if (!token) {
      set({ isAuthenticated: false, isLoading: false });
      return;
    }

    set({ isLoading: true });
    try {
      const user = await authService.getCurrentUser();
      get().setUser(user);
    } catch (err) {
      // Токен невалиден — очищаем
      console.warn('Auth check failed:', err);
      get().logout();
    } finally {
      set({ isLoading: false });
    }
  },

  logout: () => {
    localStorageUtil.remove('token');
    localStorageUtil.remove('refreshToken');
    set({
      token: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      error: null,
    });
  },

  clearError: () => {
    set({ error: null });
  },
}));