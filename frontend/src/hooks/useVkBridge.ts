import { useEffect, useState } from 'react';
import vkBridgeRaw, {
  AppearanceType,
  VKBridgeEvent,
  AnyReceiveMethodName,
  GetLaunchParamsResponse,
} from '@vkontakte/vk-bridge';
import { authStore } from '../store/authStore';

// === FIX: Robust bridge instance resolution ===
// Используем 'as any' для обхода статической проверки типов.
// Это позволяет корректно определить инстанс моста в рантайме,
// даже если бандлер изменил структуру экспорта (default vs named).
const bridgeRaw = vkBridgeRaw as any;
const bridge = bridgeRaw.send ? bridgeRaw : (bridgeRaw.default ?? bridgeRaw);

export interface VkUser {
  id: number;
  first_name: string;
  last_name: string;
  photo_100?: string;
  photo_200?: string;
}

export interface VkBridgeState {
  isInitialized: boolean;
  vkUser: VkUser | null;
  initData: string | null;
  appearance: AppearanceType;
  platform: 'android' | 'ios' | 'vkcom';
  error: string | null;
}

const getInitDataFromUrl = (): string => {
  const search = window.location.search;
  return search.startsWith('?') ? search.slice(1) : search;
};

const mapPlatform = (vkPlatform?: string): 'android' | 'ios' | 'vkcom' => {
  switch (vkPlatform) {
    case 'android':
      return 'android';
    case 'iphone':
    case 'ipad':
      return 'ios';
    case 'desktop':
    case 'mobile':
    case 'mvk':
    default:
      return 'vkcom';
  }
};

export function useVkBridge(): VkBridgeState {
  const [state, setState] = useState<VkBridgeState>({
    isInitialized: false,
    vkUser: null,
    initData: null,
    appearance: 'light',
    platform: 'vkcom',
    error: null,
  });

  useEffect(() => {
    let isMounted = true;

    const init = async () => {
      try {
        // Проверка доступности bridge в рантайме
        if (!bridge || typeof bridge.send !== 'function') {
          throw new Error('VK Bridge not available');
        }

        // 1. Инициализация
        await bridge.send('VKWebAppInit');

        // 2. Получение данных пользователя
        const userInfo = await bridge.send('VKWebAppGetUserInfo');

        // 3. Получение параметров запуска и платформы
        const launchParams = await bridge.send('VKWebAppGetLaunchParams');
        const platform = mapPlatform((launchParams as GetLaunchParamsResponse & { vk_platform?: string }).vk_platform);
        
        // 4. Получение initData из URL
        const initData = getInitDataFromUrl();

        if (isMounted) {
          setState((prev) => ({
            ...prev,
            isInitialized: true,
            vkUser: {
              id: userInfo.id,
              first_name: userInfo.first_name,
              last_name: userInfo.last_name,
              photo_100: userInfo.photo_100,
              photo_200: userInfo.photo_200,
            },
            initData,
            platform,
          }));
        }

        // 5. Авто-авторизация
        if (initData) {
          const { token, isAuthenticated } = authStore.getState();
          if (!token || !isAuthenticated) {
            try {
              await authStore.getState().login(initData);
            } catch (err) {
              console.error('Auto-login failed:', err);
            }
          }
        }

        // 6. Подписка на смену темы
        const handleBridgeEvent = (event: VKBridgeEvent<AnyReceiveMethodName>) => {
          if (event.detail.type === 'VKWebAppUpdateConfig') {
            const config = event.detail.data;
            if (config.scheme) {
              setState((prev) => ({
                ...prev,
                appearance: config.scheme === 'vkcom_dark' ? 'dark' : 'light',
              }));
            }
          }
        };

        bridge.subscribe(handleBridgeEvent);

        return () => {
          bridge.unsubscribe(handleBridgeEvent);
        };
      } catch (err) {
        console.error('VK Bridge init error:', err);
        if (isMounted) {
          setState((prev) => ({
            ...prev,
            isInitialized: true,
            error: err instanceof Error ? err.message : 'VK Bridge initialization failed',
          }));
        }
      }
    };

    init();

    return () => {
      isMounted = false;
    };
  }, []);

  return state;
}