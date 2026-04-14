export type CharacterClass =
  | 'воин'
  | 'жрец'
  | 'паладин'
  | 'маг'
  | 'призыватель'
  | 'некромант'
  | 'варвар'
  | 'охотник'
  | 'друид'
  | 'вор'
  | 'оборотень';

export const CHARACTER_CLASSES: { value: CharacterClass; label: string; description: string }[] = [
  { value: 'воин', label: 'Воин', description: 'Мастер ближнего боя, высокая защита и урон.' },
  { value: 'жрец', label: 'Жрец', description: 'Целитель и поддержка, магия света.' },
  { value: 'паладин', label: 'Паладин', description: 'Святой воин, сочетание боя и магии.' },
  { value: 'маг', label: 'Маг', description: 'Мощная стихийная магия, низкая защита.' },
  { value: 'призыватель', label: 'Призыватель', description: 'Призывает существ для помощи в бою.' },
  { value: 'некромант', label: 'Некромант', description: 'Магия смерти, управление нежитью.' },
  { value: 'варвар', label: 'Варвар', description: 'Яростный боец, высокий урон и здоровье.' },
  { value: 'охотник', label: 'Охотник', description: 'Дальний бой, ловушки и питомцы.' },
  { value: 'друид', label: 'Друид', description: 'Магия природы, превращения и лечение.' },
  { value: 'вор', label: 'Вор', description: 'Скрытность, критические удары, ловкость.' },
  { value: 'оборотень', label: 'Оборотень', description: 'Превращение в зверя, регенерация.' },
];

export interface CharacterStats {
  strength: number;
  agility: number;
  intelligence: number;
}

export interface CharacterResources {
  hp_current: number;
  hp_max: number;
  mana_current: number;
  mana_max: number;
  stamina_current: number;
  stamina_max: number;
  fatigue: number;
  gold: number;
}

export interface Character {
  id: string;
  name: string;
  character_class: CharacterClass;
  level: number;
  experience: number;
  stats: CharacterStats;
  resources: CharacterResources;
  status: 'alive' | 'dead' | 'resting';
  current_location_id: string;
  created_at: string;
  updated_at: string;
}

export interface CharacterCreateRequest {
  name: string;
  character_class: CharacterClass;
}