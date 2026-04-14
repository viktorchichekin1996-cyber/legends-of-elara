import { View, Panel, PanelHeader, Group, Div, Text, ScreenSpinner, SimpleCell, Avatar } from '@vkontakte/vkui';
import { useEffect } from 'react';
import { useInventoryStore } from '../store/inventoryStore';
import { useCharacterStore } from '../store/characterStore';
import { ItemCard } from '../components/inventory/ItemCard';
import { Icon28CoinsOutline } from '@vkontakte/icons';

interface InventoryScreenProps {
  id: string;
}

export function InventoryScreen({ id }: InventoryScreenProps) {
  const { items, fetchInventory, isLoading, error } = useInventoryStore();
  const { character } = useCharacterStore();

  useEffect(() => {
    fetchInventory();
  }, [fetchInventory]);

  const equippedItems = items.filter((i) => i.is_equipped);
  const inventoryItems = items.filter((i) => !i.is_equipped);

  return (
    <View activePanel={id}>
      <Panel id={id}>
        <PanelHeader style={{ background: '#0b1020', color: '#e2e8f0' }}>
          🎒 Инвентарь
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
          <SimpleCell
            before={
              <Avatar size={36} style={{ background: '#1e2945', border: '1px solid #60a5fa' }}>
                <Icon28CoinsOutline width={20} height={20} fill="#60a5fa" />
              </Avatar>
            }
            subtitle={`Слоты: ${inventoryItems.length}/${character?.inventory_slots || 10}`}
            style={{ background: '#151e38', borderBottom: '1px solid #2d3755', borderRadius: '12px', marginBottom: 12 }}
          >
            <Text weight="2" style={{ color: '#60a5fa' }}>
              {character?.gold || 0} золота
            </Text>
          </SimpleCell>

          <Div>
            <Text weight="2" style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>
              ⚔️ Экипировка
            </Text>
            {equippedItems.length === 0 ? (
              <Div style={{ background: '#151e38', borderRadius: 12, padding: 16, textAlign: 'center', border: '1px dashed #2d3755' }}>
                <Text style={{ color: '#64748b', fontSize: 13 }}>Нет экипированных предметов</Text>
              </Div>
            ) : (
              <Div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {equippedItems.map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </Div>
            )}
          </Div>

          <Div>
            <Text weight="2" style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>
              📦 Предметы
            </Text>
            {inventoryItems.length === 0 ? (
              <Div style={{ background: '#151e38', borderRadius: 12, padding: 16, textAlign: 'center', border: '1px dashed #2d3755' }}>
                <Text style={{ color: '#64748b', fontSize: 13 }}>Инвентарь пуст</Text>
              </Div>
            ) : (
              <Div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 8 }}>
                {inventoryItems.map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </Div>
            )}
          </Div>
        </Group>
      </Panel>
    </View>
  );
}