import { View, Panel, PanelHeader, Group, Div, Text, ScreenSpinner } from '@vkontakte/vkui';
import { useEffect } from 'react';
import { useMemoryStore } from '../store/memoryStore';
import { FantasyCard } from '../components/ui/FantasyCard';

interface MemoriesScreenProps {
  id: string;
}

const getTypeColor = (type: string): string => {
  switch (type) {
    case 'boss_defeat': return '#d4af37';
    case 'quest_complete': return '#4a7c4a';
    case 'important_choice': return '#9c27b0';
    case 'discovery': return '#3b82f6';
    default: return '#94a3b8';
  }
};

const getTypeLabel = (type: string): string => {
  const map: Record<string, string> = {
    boss_defeat: 'Победа над боссом',
    quest_complete: 'Квест завершён',
    important_choice: 'Важный выбор',
    discovery: 'Открытие',
    level_up: 'Повышение уровня',
    unique_event: 'Уникальное событие',
  };
  return map[type] || type;
};

export function MemoriesScreen({ id }: MemoriesScreenProps) {
  const { memories, fetchMemories, isLoading, error } = useMemoryStore();

  useEffect(() => {
    fetchMemories();
  }, [fetchMemories]);

  return (
    <View activePanel={id}>
      <Panel id={id}>
        <PanelHeader style={{ background: '#0b1020', color: '#e2e8f0' }}>
          🧠 Книга Памяти
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
          {memories.length === 0 ? (
            <Div style={{ textAlign: 'center', padding: 40 }}>
              <Text style={{ fontSize: 48, marginBottom: 16 }}>📭</Text>
              <Text weight="2" style={{ fontSize: 18, color: '#94a3b8' }}>
                Память пуста
              </Text>
              <Text style={{ color: '#64748b', marginTop: 8 }}>
                Ваши значимые действия будут сохранены здесь.
              </Text>
            </Div>
          ) : (
            <Div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {memories.map((mem) => (
                <FantasyCard key={mem.id} variant="default">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                    <Text weight="2" style={{ fontSize: 16, color: '#e2e8f0' }}>
                      {mem.title}
                    </Text>
                    <Text style={{ fontSize: 12, color: getTypeColor(mem.memory_type), fontWeight: 600 }}>
                      {getTypeLabel(mem.memory_type)}
                    </Text>
                  </div>
                  
                  <Text style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8, lineHeight: 1.5 }}>
                    {mem.description}
                  </Text>

                  <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                    {mem.tags.map((tag) => (
                      <span key={tag} style={{ 
                        fontSize: 10, 
                        background: '#1e2945', 
                        color: '#60a5fa', 
                        padding: '2px 6px', 
                        borderRadius: 4,
                        border: '1px solid #2d3755'
                      }}>
                        #{tag}
                      </span>
                    ))}
                  </div>
                  
                  <div style={{ marginTop: 8, textAlign: 'right' }}>
                    <Text style={{ fontSize: 10, color: '#475569' }}>
                      {new Date(mem.created_at).toLocaleDateString('ru-RU')}
                    </Text>
                  </div>
                </FantasyCard>
              ))}
            </Div>
          )}
        </Group>
      </Panel>
    </View>
  );
}