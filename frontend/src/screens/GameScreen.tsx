import { View, Panel, PanelHeader, ScreenSpinner, Group, Div, Text } from '@vkontakte/vkui';
import { StatsPanel } from '../components/game/StatsPanel';
import { EventCard } from '../components/game/EventCard';
import { useGameStore } from '../store/gameStore';
import { useEffect } from 'react';
import { FantasyCard } from '../components/ui/FantasyCard';

interface GameScreenProps {
  id: string;
}

export function GameScreen({ id }: GameScreenProps) {
  const { isLoading, isProcessing, currentEvent, fetchEvent } = useGameStore();

  useEffect(() => {
    if (!currentEvent) {
      fetchEvent();
    }
  }, [currentEvent, fetchEvent]);

  return (
    <View activePanel={id}>
      <Panel id={id}>
        <PanelHeader style={{ background: '#0b1020', color: '#e2e8f0' }}>
          🐉 Легенды Элары
        </PanelHeader>
        
        {(isLoading || isProcessing) && <ScreenSpinner style={{ backgroundColor: 'rgba(11, 16, 32, 0.8)' }} />}
        
        <Group style={{ background: 'transparent', margin: 0 }}>
          <StatsPanel />
          
          <Div>
            <FantasyCard variant="narrative">
              <div style={{ marginBottom: 12 }}>
                <Text weight="2" style={{ fontSize: 14, color: '#60a5fa', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  ✨ AI Повествование
                </Text>
                <Text style={{ fontSize: 16, color: '#e2e8f0', lineHeight: 1.6, fontStyle: 'italic' }}>
                  {currentEvent?.description || "Мир замер в ожидании вашего действия..."}
                </Text>
              </div>
            </FantasyCard>
          </Div>

          <EventCard />
        </Group>
      </Panel>
    </View>
  );
}