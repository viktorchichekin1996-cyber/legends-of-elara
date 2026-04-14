import {
  AppRoot,
  SplitLayout,
  SplitCol,
  View,
  Panel,
  PanelHeader,
  ScreenSpinner,
  Text,
  Avatar,
  Group,
  Cell,
  AdaptivityProvider,
  ConfigProvider,
  Button,
  Snackbar,
  Link,
} from '@vkontakte/vkui';
import '@vkontakte/vkui/dist/vkui.css';
import { useVkBridge } from './hooks/useVkBridge';
import { useAuth } from './hooks/useAuth';
import { Icon28WarningTriangleOutline } from '@vkontakte/icons';
import { GameScreen } from './screens/GameScreen';
import { CreateCharacterScreen } from './screens/CreateCharacterScreen';
import { useCharacterStore } from './store/characterStore';
import { useEffect } from 'react';

function App() {
  const { isInitialized: bridgeReady, vkUser, appearance, platform, error: bridgeError, initData } = useVkBridge();
  const { isAuthenticated, isLoading: authLoading, error: authError, clearError } = useAuth();
  const { character, fetchCharacter, needsCreation, isLoading: charLoading } = useCharacterStore();

  // Загружаем персонажа после авторизации
  useEffect(() => {
    if (isAuthenticated && !character && !needsCreation && !charLoading) {
      fetchCharacter();
    }
  }, [isAuthenticated, character, needsCreation, charLoading, fetchCharacter]);

  // Состояние загрузки
  if (!bridgeReady || authLoading || (isAuthenticated && charLoading && !needsCreation)) {
    return (
      <AppRoot>
        <ScreenSpinner />
      </AppRoot>
    );
  }

  // Ошибка VK Bridge
  if (bridgeError) {
    return (
      <AppRoot>
        <View activePanel="error">
          <Panel id="error">
            <PanelHeader>Ошибка VK Bridge</PanelHeader>
            <Group>
              <Text style={{ color: 'var(--vkui--color_text_negative)', padding: 20 }}>
                {bridgeError}
              </Text>
            </Group>
          </Panel>
        </View>
      </AppRoot>
    );
  }

  // Нет initData — приложение открыто вне VK
  if (!initData) {
    return (
      <AppRoot>
        <View activePanel="no-vk">
          <Panel id="no-vk">
            <PanelHeader>Легенды Элары</PanelHeader>
            <Group>
              <div style={{ padding: 40, textAlign: 'center' }}>
                <Text style={{ fontSize: 48, marginBottom: 16 }}>🐉</Text>
                <Text weight="2" style={{ fontSize: 18, marginBottom: 8 }}>
                  Приложение работает только внутри ВКонтакте
                </Text>
                <Text style={{ color: 'var(--vkui--color_text_secondary)', marginBottom: 24 }}>
                  Откройте приложение через VK Mini Apps для авторизации.
                </Text>
                <Link href="https://vk.com/app54534430" target="_blank">
                  <Button size="l">Открыть в VK</Button>
                </Link>
              </div>
            </Group>
          </Panel>
        </View>
      </AppRoot>
    );
  }

  // Ошибка авторизации
  const hasAuthError = !!authError;

  if (hasAuthError) {
    return (
      <ConfigProvider platform={platform}>
        <AdaptivityProvider>
          <AppRoot>
            <View activePanel="auth-error">
              <Panel id="auth-error">
                <PanelHeader>Ошибка авторизации</PanelHeader>
                <Group>
                  <Snackbar
                    before={<Icon28WarningTriangleOutline fill="var(--vkui--color_icon_negative)" />}
                    onClose={clearError}
                    onClosed={clearError}
                  >
                    {authError}
                  </Snackbar>
                </Group>
              </Panel>
            </View>
          </AppRoot>
        </AdaptivityProvider>
      </ConfigProvider>
    );
  }

  // Если авторизован
  if (isAuthenticated) {
    // Если нужно создать персонажа — показываем экран создания
    if (needsCreation || !character) {
      return (
        <ConfigProvider platform={platform}>
          <AdaptivityProvider>
            <AppRoot>
              <CreateCharacterScreen id="create-character" />
            </AppRoot>
          </AdaptivityProvider>
        </ConfigProvider>
      );
    }

    // Иначе — игровой экран
    return (
      <ConfigProvider platform={platform}>
        <AdaptivityProvider>
          <AppRoot>
            <GameScreen id="game" />
          </AppRoot>
        </AdaptivityProvider>
      </ConfigProvider>
    );
  }

  // Ожидание авторизации
  return (
    <ConfigProvider platform={platform}>
      <AdaptivityProvider>
        <AppRoot>
          <SplitLayout>
            <SplitCol>
              <View activePanel="main">
                <Panel id="main">
                  <PanelHeader>Легенды Элары</PanelHeader>
                  <Group>
                    <Cell
                      before={
                        vkUser?.photo_100 ? (
                          <Avatar src={vkUser.photo_100} size={48} />
                        ) : undefined
                      }
                      subtitle={`ID: ${vkUser?.id} • Вход...`}
                    >
                      {vkUser?.first_name} {vkUser?.last_name}
                    </Cell>
                  </Group>
                  <Group>
                    <div style={{ padding: 20, textAlign: 'center' }}>
                      <Text style={{ fontSize: 48, marginBottom: 16 }}>🐉</Text>
                      <Text weight="2" style={{ fontSize: 18 }}>
                        Ожидание авторизации...
                      </Text>
                      <Text style={{ color: 'var(--vkui--color_text_secondary)', marginTop: 16 }}>
                        Тема: {appearance} | Платформа: {platform}
                      </Text>
                    </div>
                  </Group>
                </Panel>
              </View>
            </SplitCol>
          </SplitLayout>
        </AppRoot>
      </AdaptivityProvider>
    </ConfigProvider>
  );
}

export default App;