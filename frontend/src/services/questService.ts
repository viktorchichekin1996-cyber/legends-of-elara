import { api } from './api';
import { Quest } from '../types/quest';

export const questService = {
  async getQuests(): Promise<Quest[]> {
    const response = await api.get<Quest[]>('/quests');
    return response.data;
  },

  async cancelQuest(questId: string): Promise<void> {
    await api.post(`/quests/${questId}/cancel`);
  },
};