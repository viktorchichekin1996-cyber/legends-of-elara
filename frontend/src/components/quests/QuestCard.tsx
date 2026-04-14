import { Text, Button, Progress } from '@vkontakte/vkui';
// ИСПРАВЛЕНИЕ: Удалён неиспользуемый импорт Icon28CheckCircleOutline
import { Icon28CancelOutline } from '@vkontakte/icons';
import { FantasyCard } from '../ui/FantasyCard';
import { Quest } from '../../types/quest';
import { useQuestStore } from '../../store/questStore';

interface QuestCardProps {
  quest: Quest;
}

const statusColors: Record<string, string> = {
  active: '#d4af37',
  completed: '#4a7c4a',
  failed: '#8b2a2a',
  cancelled: '#5a5a5a',
};

const statusLabels: Record<string, string> = {
  active: 'Активен',
  completed: 'Завершён',
  failed: 'Провален',
  cancelled: 'Отменён',
};

export function QuestCard({ quest }: QuestCardProps) {
  const { cancelQuest, isProcessing } = useQuestStore();

  const totalProgress = quest.objectives.length > 0
    ? quest.objectives.reduce((sum, obj) => sum + (obj.current / obj.required), 0) / quest.objectives.length * 100
    : 0;

  const handleCancel = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (quest.status === 'active') {
      await cancelQuest(quest.id);
    }
  };

  return (
    <FantasyCard variant="gold">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <Text weight="2" style={{ fontSize: 16, color: '#e8d5b7' }}>
          {quest.title}
        </Text>
        <Text style={{ fontSize: 12, color: statusColors[quest.status], fontWeight: 600 }}>
          {statusLabels[quest.status]}
        </Text>
      </div>

      <Text style={{ fontSize: 14, color: '#c9b896', marginBottom: 12, lineHeight: 1.4 }}>
        {quest.description}
      </Text>

      {/* Цели */}
      <div style={{ marginBottom: 12 }}>
        {quest.objectives.map((obj, idx) => (
          <div key={idx} style={{ marginBottom: 6 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
              <Text style={{ fontSize: 12, color: '#a89878' }}>{obj.description}</Text>
              <Text style={{ fontSize: 12, color: '#d4af37' }}>{obj.current}/{obj.required}</Text>
            </div>
            <div style={{ height: 4, background: '#2a2414', borderRadius: 2 }}>
              <div
                style={{
                  width: `${Math.min(100, (obj.current / obj.required) * 100)}%`,
                  height: '100%',
                  background: obj.current >= obj.required ? '#4a7c4a' : '#d4af37',
                  borderRadius: 2,
                  transition: 'width 0.3s',
                }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Общий прогресс */}
      <div style={{ marginBottom: 12 }}>
        <Progress value={totalProgress} style={{ height: 6 }} />
      </div>

      {/* Награды */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 12, flexWrap: 'wrap' }}>
        {quest.rewards.xp && (
          <div style={{ background: '#1a1a1a', padding: '4px 8px', borderRadius: 4 }}>
            <Text style={{ fontSize: 12, color: '#87ceeb' }}>+{quest.rewards.xp} XP</Text>
          </div>
        )}
        {quest.rewards.gold && (
          <div style={{ background: '#1a1a1a', padding: '4px 8px', borderRadius: 4 }}>
            <Text style={{ fontSize: 12, color: '#ffd700' }}>+{quest.rewards.gold} золота</Text>
          </div>
        )}
      </div>

      {/* Кнопка отмены */}
      {quest.status === 'active' && (
        <Button
          mode="secondary"
          size="s"
          stretched
          before={<Icon28CancelOutline width={16} height={16} />}
          onClick={handleCancel}
          disabled={isProcessing}
          style={{ background: '#2a1414', color: '#c9a8a8', border: '1px solid #4a2a2a' }}
        >
          Отменить квест
        </Button>
      )}
    </FantasyCard>
  );
}