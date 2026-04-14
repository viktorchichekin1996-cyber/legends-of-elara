export type QuestStatus = 'active' | 'completed' | 'failed' | 'cancelled';

export interface QuestObjective {
  type: 'kill' | 'collect' | 'visit' | 'talk';
  description: string;
  target_id?: string;
  target_name?: string;
  required: number;
  current: number;
}

export interface QuestReward {
  xp?: number;
  gold?: number;
  items?: string[];
}

export interface Quest {
  id: string;
  title: string;
  description: string;
  status: QuestStatus;
  objectives: QuestObjective[];
  rewards: QuestReward;
  accepted_at: string;
  completed_at?: string;
}