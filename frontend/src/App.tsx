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
  Tabbar,
  TabbarItem,
} from '@vkontakte/vkui';
import '@vkontakte/vkui/dist/vkui.css';
import { useState, useEffect } from 'react';
import { useVkBridge } from './hooks/useVkBridge';
import { useAuth } from './hooks/useAuth';
import { 
  Icon28GameOutline, 
  Icon28NewsfeedOutline,
  Icon28InboxOutline,
  Icon28LocationOutline,
  Icon28BookOutline 
} from '@vkontakte/icons';
import { Icon28WarningTriangleOutline } from '@vkontakte/icons';
import { GameScreen } from './screens/GameScreen';
import { CreateCharacterScreen } from './screens/CreateCharacterScreen';
import { QuestsScreen } from './screens/QuestsScreen';
import { InventoryScreen } from './screens/InventoryScreen';
import { MemoriesScreen } from './screens/MemoriesScreen';
import { useCharacterStore } from './store/characterStore';

type ActivePanel = 'game' | 'quests' | 'inventory' | 'map' | 'memories';

function App() {
  const { isInitialized: bridgeReady, vkUser, appearance, platform, error: bridgeError, initData } = useVkBridge();
  const { isAuthenticated, isLoading: authLoading, error: authError, clearError } = useAuth();
  const { character, fetchCharacter, needsCreation, isLoading: charLoading } = useCharacterStore();
  const [activePanel, setActivePanel] = useState<ActivePanel>('game');

  useEffect(() => {
    if (isAuthenticated && !character && !needsCreation && !charLoading) {
      fetchCharacter();
    }
  }, [isAuthenticated, character, needsCreation, charLoading, fetchCharacter]);

  if (!bridgeReady || authLoading || (isAuthenticated && charLoading && !needsCreation)) {
    return (
      // ИСПРАВЛЕНО: Удалён проп appearance
      <AppRoot>
        <ScreenSpinner style={{ backgroundColor: 'rgba(11, 16, 32, 0.8)' }} />
      </AppRoot>
    );
  }

  if (bridgeError) {
    return (
      // ИСПРАВЛЕНО: Удалён проп appearance
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

  if (!initData) {
    return (
      // ИСПРАВЛЕНО: Удалён проп appearance
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

  const hasAuthError = !!authError;

  if (hasAuthError) {
    return (
      // ИСПРАВЛЕНО: Удалён проп appearance из ConfigProvider и AppRoot
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

  if (isAuthenticated) {
    if (needsCreation || !character) {
      return (
        // ИСПРАВЛЕНО: Удалён проп appearance
        <ConfigProvider platform={platform}>
          <AdaptivityProvider>
            <AppRoot>
              <CreateCharacterScreen id="create-character" />
            </AppRoot>
          </AdaptivityProvider>
        </ConfigProvider>
      );
    }

    return (
      // ИСПРАВЛЕНО: Удалён проп appearance
      <ConfigProvider platform={platform}>
        <AdaptivityProvider>
          <AppRoot>
            <SplitLayout>
              <SplitCol>
                <View activePanel={activePanel}>
                  <GameScreen id="game" />
                  <QuestsScreen id="quests" />
                  <InventoryScreen id="inventory" />
                  <MemoriesScreen id="memories" />
                  <View activePanel="map">
                    <Panel id="map">
                      <PanelHeader>🗺️ Карта мира</PanelHeader>
                      <Group>
                        <div style={{ padding: 40, textAlign: 'center' }}>
                          <Text style={{ fontSize: 48, marginBottom: 16 }}>🗺️</Text>
                          <Text weight="2" style={{ fontSize: 18, color: '#94a3b8' }}>
                            Карта в разработке
                          </Text>
                        </div>
                      </Group>
                    </Panel>
                  </View>
                </View>
              </SplitCol>
            </SplitLayout>

            <Tabbar style={{ background: '#0b1020', borderTop: '1px solid #2d3755' }}>
              <TabbarItem
                selected={activePanel === 'game'}
                onClick={() => setActivePanel('game')}
                style={{ color: activePanel === 'game' ? '#60a5fa' : '#94a3b8' }}
              >
                <Icon28GameOutline fill={activePanel === 'game' ? '#60a5fa' : '#94a3b8'} />
                Игра
              </TabbarItem>
              <TabbarItem
                selected={activePanel === 'quests'}
                onClick={() => setActivePanel('quests')}
                style={{ color: activePanel === 'quests' ? '#60a5fa' : '#94a3b8' }}
              >
                <Icon28NewsfeedOutline fill={activePanel === 'quests' ? '#60a5fa' : '#94a3b8'} />
                Квесты
              </TabbarItem>
              <TabbarItem
                selected={activePanel === 'inventory'}
                onClick={() => setActivePanel('inventory')}
                style={{ color: activePanel === 'inventory' ? '#60a5fa' : '#94a3b8' }}
              >
                <Icon28InboxOutline fill={activePanel === 'inventory' ? '#60a5fa' : '#94a3b8'} />
                Инвентарь
              </TabbarItem>
              <TabbarItem
                selected={activePanel === 'memories'}
                onClick={() => setActivePanel('memories')}
                style={{ color: activePanel === 'memories' ? '#60a5fa' : '#94a3b8' }}
              >
                <Icon28BookOutline fill={activePanel === 'memories' ? '#60a5fa' : '#94a3b8'} />
                Память
              </TabbarItem>
              <TabbarItem
                selected={activePanel === 'map'}
                onClick={() => setActivePanel('map')}
                style={{ color: activePanel === 'map' ? '#60a5fa' : '#94a3b8' }}
              >
                <Icon28LocationOutline fill={activePanel === 'map' ? '#60a5fa' : '#94a3b8'} />
                Карта
              </TabbarItem>
            </Tabbar>
          </AppRoot>
        </AdaptivityProvider>
      </ConfigProvider>
    );
  }

  return (
    // ИСПРАВЛЕНО: Удалён проп appearance
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