import { Group, Text, Button, Card, Snackbar, Div } from '@vkontakte/vkui';
import { Icon28CheckCircleOutline, Icon28ErrorCircleOutline } from '@vkontakte/icons';
import { useGameStore } from '../../store/gameStore';
import { useEffect } from 'react';

export function EventCard() {
  const { 
    currentEvent, 
    fetchEvent, 
    isLoading, 
    isProcessing, 
    error, 
    lastResult,
    handleChoice,
    clearError,
    clearResult 
  } = useGameStore();

  useEffect(() => {
    if (!currentEvent) {
      fetchEvent();
    }
  }, [currentEvent, fetchEvent]);

  if (isLoading) {
    return (
      <Group>
        <Div style={{ textAlign: 'center', padding: 40 }}>
          <Text style={{ color: 'var(--vkui--color_text_secondary)' }}>
            Генерация события...
          </Text>
        </Div>
      </Group>
    );
  }

  if (error) {
    return (
      <Group>
        <Snackbar
          before={<Icon28ErrorCircleOutline fill="var(--vkui--color_icon_negative)" />}
          onClose={clearError}
          onClosed={clearError}
        >
          {error}
        </Snackbar>
      </Group>
    );
  }

  if (!currentEvent) {
    return null;
  }

  return (
    <Group>
      {/* Результат действия */}
      {lastResult && (
        <Snackbar
          mode={lastResult.success ? 'default' : 'default'}
          before={
            lastResult.success 
              ? <Icon28CheckCircleOutline fill="var(--vkui--color_icon_positive)" />
              : <Icon28ErrorCircleOutline fill="var(--vkui--color_icon_negative)" />
          }
          onClose={clearResult}
          onClosed={clearResult}
        >
          {lastResult.message}
        </Snackbar>
      )}

      <Card mode="shadow" style={{ margin: 8 }}>
        <div style={{ padding: 16 }}>
          <Text weight="2" style={{ fontSize: 18, marginBottom: 8 }}>
            {currentEvent.title}
          </Text>
          
          <Text style={{ fontSize: 15, lineHeight: 1.5, marginBottom: 16 }}>
            {currentEvent.description}
          </Text>

          {/* Варианты выбора */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {currentEvent.choices.map((choice) => (
              <Button
                key={choice.id}
                size="m"
                stretched
                disabled={isProcessing}
                loading={isProcessing}
                onClick={() => handleChoice(choice.id)}
              >
                {choice.text}
              </Button>
            ))}
          </div>
        </div>
      </Card>
    </Group>
  );
}