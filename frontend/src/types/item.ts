export type ItemType = 'weapon' | 'armor' | 'accessory' | 'consumable' | 'quest_item' | 'bag';
export type ItemRarity = 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
export type EquipmentSlot = 'weapon' | 'armor' | 'helmet' | 'gloves' | 'boots' | 'accessory' | 'ring1' | 'ring2';

export interface Item {
  id: string;
  name: string;
  item_type: ItemType;
  rarity: ItemRarity;
  description?: string;
  base_cost: number;
  damage_min?: number;
  damage_max?: number;
  armor?: number;
  slot?: EquipmentSlot;
  is_stackable: boolean;
  modifiers?: Record<string, number>;
  requirements?: {
    level?: number;
    strength?: number;
    agility?: number;
    intelligence?: number;
  };
}

export interface InventoryItem {
  id: string;
  item_id: string;
  item: Item;
  quantity: number;
  durability?: number;
  max_durability?: number;
  is_equipped: boolean;
  equipped_slot?: EquipmentSlot;
}