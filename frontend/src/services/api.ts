import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { localStorageUtil } from '../utils/localStorage';
import { authStore } from '../store/authStore';

const API_URL = import.meta.env.VITE_API_URL || 'https://api.chichekin-tech.ru/api/v1';

export const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Request interceptor: добавляем токен
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorageUtil.get<string>('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => Promise.reject(error)
);

// Response interceptor: обработка 401 и ошибок
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Если 401 и запрос не повторялся — разлогиниваем
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      // Очищаем состояние
      authStore.getState().logout();
      
      // Можно попробовать refresh токен, если реализован
      // Но для VK Mini App обычно проще перезапросить initData
      return Promise.reject(error);
    }

    return Promise.reject(error);
  }
);