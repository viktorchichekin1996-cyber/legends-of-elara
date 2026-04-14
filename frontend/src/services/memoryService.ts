import { api } from './api';

export interface Memory {
  id: string;
  memory_type: string;
  title: string;
  description: string;
  importance: number;
  tags: string[];
  data: Record<string, any>;
  created_at: string;
}

export const memoryService = {
  async getMemories(): Promise<Memory[]> {
    const response = await api.get<Memory[]>('/memories');
    return response.data;
  },
};