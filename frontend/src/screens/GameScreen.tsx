import { View, Panel, PanelHeader, ScreenSpinner } from '@vkontakte/vkui';
import { StatsPanel } from '../components/game/StatsPanel';
import { EventCard } from '../components/game/EventCard';
import { useGameStore } from '../store/gameStore';

interface GameScreenProps {
  id: string;
}

export function GameScreen({ id }: GameScreenProps) {
  const { isLoading, isProcessing } = useGameStore();

  return (
    <View activePanel={id}>
      <Panel id={id}>
        <PanelHeader>Легенды Элары</PanelHeader>
        
        {(isLoading || isProcessing) && <ScreenSpinner />}
        
        <StatsPanel />
        <EventCard />
      </Panel>
    </View>
  );
}