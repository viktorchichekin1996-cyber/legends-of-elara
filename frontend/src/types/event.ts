export interface GameEvent {
  id: string;
  type: 'story' | 'combat' | 'quest' | 'discovery';
  title: string;
  description: string;
  image_url?: string;
  choices: EventChoice[];
  created_at: string;
}

export interface EventChoice {
  id: string;
  text: string;
  action_type: 'continue' | 'attack' | 'defend' | 'use_item' | 'flee' | 'rest';
  requires?: {
    stamina?: number;
    mana?: number;
    item_id?: string;
  };
}

export interface EventActionResult {
  success: boolean;
  message: string;
  rewards?: {
    xp?: number;
    gold?: number;
    items?: string[];
  };
  next_event?: GameEvent;
  combat_started?: boolean;
  character_updates?: {
    hp_change?: number;
    mana_change?: number;
    stamina_change?: number;
  };
}