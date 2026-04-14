import { View, Panel, PanelHeader, Group, Text, Div, ScreenSpinner } from '@vkontakte/vkui';
import { useEffect } from 'react';
import { useQuestStore } from '../store/questStore';
import { QuestCard } from '../components/quests/QuestCard';

interface QuestsScreenProps {
  id: string;
}

export function QuestsScreen({ id }: QuestsScreenProps) {
  const { quests, fetchQuests, isLoading, error } = useQuestStore();

  useEffect(() => {
    fetchQuests();
  }, [fetchQuests]);

  return (
    <View activePanel={id}>
      <Panel id={id}>
        <PanelHeader style={{ background: '#0b1020', color: '#e2e8f0' }}>
          📜 Книга квестов
        </PanelHeader>

        {isLoading && <ScreenSpinner style={{ backgroundColor: 'rgba(11, 16, 32, 0.8)' }} />}

        {error && (
          <Group>
            <Div>
              <Text style={{ color: '#ef4444' }}>{error}</Text>
            </Div>
          </Group>
        )}

        <Group style={{ background: 'transparent', margin: 0 }}>
          {quests.length === 0 ? (
            <Div style={{ textAlign: 'center', padding: 40 }}>
              <Text style={{ fontSize: 48, marginBottom: 16 }}>📭</Text>
              <Text weight="2" style={{ fontSize: 18, color: '#94a3b8' }}>
                Нет активных квестов
              </Text>
              <Text style={{ color: '#64748b', marginTop: 8 }}>
                Исследуйте мир, чтобы получить новые задания.
              </Text>
            </Div>
          ) : (
            <Div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {quests.map((quest) => (
                <QuestCard key={quest.id} quest={quest} />
              ))}
            </Div>
          )}
        </Group>
      </Panel>
    </View>
  );
}