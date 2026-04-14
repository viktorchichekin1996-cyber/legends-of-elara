import { Text, Badge } from '@vkontakte/vkui';
// ИСПРАВЛЕНО: Используем Icon24 варианты, которые подтверждены компилятором.
// Icon24Shield и Icon24Box отсутствуют в данной версии, используем Icon24ArchiveOutline как стабильную замену.
import { Icon24KnifeOutline, Icon24ArchiveOutline } from '@vkontakte/icons';
import { FantasyCard } from '../ui/FantasyCard';
import { InventoryItem, ItemRarity } from '../../types/item';
import { useInventoryStore } from '../../store/inventoryStore';

interface ItemCardProps {
  item: InventoryItem;
}

const rarityColors: Record<ItemRarity, string> = {
  common: '#9e9e9e',
  uncommon: '#4caf50',
  rare: '#2196f3',
  epic: '#9c27b0',
  legendary: '#ff9800',
};

const rarityBgColors: Record<ItemRarity, string> = {
  common: 'rgba(158, 158, 158, 0.1)',
  uncommon: 'rgba(76, 175, 80, 0.1)',
  rare: 'rgba(33, 150, 243, 0.1)',
  epic: 'rgba(156, 39, 176, 0.1)',
  legendary: 'rgba(255, 152, 0, 0.1)',
};

const getItemIcon = (type: string) => {
  switch (type) {
    case 'weapon':
      return <Icon24KnifeOutline width={20} height={20} fill="#c9b896" />;
    case 'armor':
      // ИСПРАВЛЕНО: Icon24Shield отсутствует. Используем Icon24ArchiveOutline для стабильной сборки.
      return <Icon24ArchiveOutline width={20} height={20} fill="#c9b896" />;
    default:
      return <Icon24ArchiveOutline width={20} height={20} fill="#c9b896" />;
  }
};

export function ItemCard({ item }: ItemCardProps) {
  const { equipItem, unequipItem, isProcessing } = useInventoryStore();
  const rarity = item.item.rarity;

  const handleClick = async () => {
    if (isProcessing) return;
    
    if (item.is_equipped && item.equipped_slot) {
      await unequipItem(item.equipped_slot);
    } else if (item.item.slot) {
      await equipItem(item.id);
    }
  };

  return (
    <FantasyCard 
      variant={item.is_equipped ? 'gold' : 'default'} 
      onClick={item.item.slot ? handleClick : undefined}
    >
      <div style={{ position: 'relative' }}>
        <div
          style={{
            position: 'absolute',
            top: -6,
            right: -6,
            width: 16,
            height: 16,
            borderRadius: '50%',
            background: rarityColors[rarity],
            border: '2px solid #1a1a1a',
          }}
        />

        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <div
            style={{
              width: 40,
              height: 40,
              borderRadius: 6,
              background: rarityBgColors[rarity],
              border: `1px solid ${rarityColors[rarity]}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            {getItemIcon(item.item.item_type)}
          </div>

          <div style={{ flex: 1 }}>
            <Text
              weight="2"
              style={{
                fontSize: 14,
                color: item.is_equipped ? '#d4af37' : rarityColors[rarity],
                marginBottom: 2,
              }}
            >
              {item.item.name}
            </Text>
            <Text style={{ fontSize: 11, color: '#888' }}>
              {item.item.slot || item.item.item_type}
            </Text>
          </div>

          {item.quantity > 1 && (
            <Badge mode="prominent" style={{ background: '#2a2414', color: '#c9b896' }}>
              {item.quantity}
            </Badge>
          )}
        </div>

        {(item.item.damage_min || item.item.armor || item.item.modifiers) && (
          <div style={{ marginTop: 8, paddingTop: 8, borderTop: '1px solid #3a3025' }}>
            {item.item.damage_min && item.item.damage_max && (
              <Text style={{ fontSize: 11, color: '#c9b896' }}>
                Урон: {item.item.damage_min}-{item.item.damage_max}
              </Text>
            )}
            {item.item.armor && (
              <Text style={{ fontSize: 11, color: '#c9b896' }}>
                Защита: {item.item.armor}
              </Text>
            )}
            {item.item.modifiers && Object.entries(item.item.modifiers).map(([key, value]) => (
              <Text key={key} style={{ fontSize: 11, color: value > 0 ? '#4a7c4a' : '#8b2a2a' }}>
                {key}: {value > 0 ? '+' : ''}{value}
              </Text>
            ))}
          </div>
        )}

        {item.durability !== undefined && item.max_durability && (
          <div style={{ marginTop: 6 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
              <Text style={{ fontSize: 10, color: '#666' }}>Прочность</Text>
              <Text style={{ fontSize: 10, color: item.durability < item.max_durability * 0.3 ? '#8b2a2a' : '#666' }}>
                {item.durability}/{item.max_durability}
              </Text>
            </div>
            <div style={{ height: 3, background: '#2a2414', borderRadius: 1.5 }}>
              <div
                style={{
                  width: `${(item.durability / item.max_durability) * 100}%`,
                  height: '100%',
                  background: item.durability < item.max_durability * 0.3 ? '#8b2a2a' : '#4a7c4a',
                  borderRadius: 1.5,
                }}
              />
            </div>
          </div>
        )}

        {item.is_equipped && (
          <div style={{ marginTop: 6, textAlign: 'center' }}>
            <Text style={{ fontSize: 10, color: '#d4af37', fontWeight: 600 }}>
              Экипировано
            </Text>
          </div>
        )}
      </div>
    </FantasyCard>
  );
}