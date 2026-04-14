import { Group, Text, SimpleCell, Avatar } from '@vkontakte/vkui';
import { Icon28FireOutline, Icon28CoinsOutline } from '@vkontakte/icons';
import { ResourceBar } from './ResourceBar';
import { useCharacterStore } from '../../store/characterStore';
import { useEffect } from 'react';

export function StatsPanel() {
  const { character, fetchCharacter, isLoading } = useCharacterStore();

  useEffect(() => {
    if (!character) {
      fetchCharacter();
    }
  }, [character, fetchCharacter]);

  if (isLoading || !character) {
    return (
      <Group>
        <Text style={{ color: 'var(--vkui--color_text_secondary)', padding: 12 }}>
          Загрузка персонажа...
        </Text>
      </Group>
    );
  }

  const { resources, level, name, character_class } = character;

  return (
    <Group mode="plain" style={{ margin: 0 }}>
      <SimpleCell
        before={<Avatar size={40} style={{ background: 'var(--vkui--color_accent)' }}>{name[0]}</Avatar>}
        subtitle={`Уровень ${level} • ${character_class}`}
      >
        {name}
      </SimpleCell>

      <div style={{ padding: '0 12px 12px' }}>
        <ResourceBar
          label="Здоровье"
          value={resources.hp_current}
          max={resources.hp_max}
          color="red"
        />
        <ResourceBar
          label="Мана"
          value={resources.mana_current}
          max={resources.mana_max}
          color="blue"
        />
        <ResourceBar
          label="Выносливость"
          value={resources.stamina_current}
          max={resources.stamina_max}
          color="green"
        />
        
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <Icon28FireOutline width={16} height={16} fill="var(--vkui--color_icon_secondary)" />
            <Text style={{ fontSize: 13, color: 'var(--vkui--color_text_secondary)' }}>
              Усталость: {resources.fatigue}%
            </Text>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <Icon28CoinsOutline width={16} height={16} fill="var(--vkui--color_icon_secondary)" />
            <Text style={{ fontSize: 13, color: 'var(--vkui--color_text_secondary)' }}>
              {resources.gold} золота
            </Text>
          </div>
        </div>
      </div>
    </Group>
  );
}