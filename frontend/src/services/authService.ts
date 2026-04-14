import { api } from './api';

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserResponse {
  id: string;
  vk_user_id: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export const authService = {
  /** Авторизация через VK initData */
  async loginWithVk(initData: string): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/vk', { initData });
    return response.data;
  },

  /** Получение текущего пользователя */
  async getCurrentUser(): Promise<UserResponse> {
    const response = await api.get<UserResponse>('/auth/me');
    return response.data;
  },

  /** Обновление токена */
  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/refresh', { refresh_token: refreshToken });
    return response.data;
  },
};