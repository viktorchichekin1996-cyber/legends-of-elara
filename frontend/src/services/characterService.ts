import { api } from './api';
import { Character, CharacterCreateRequest } from '../types/character';

export const characterService = {
  async getCharacter(): Promise<Character> {
    const response = await api.get<Character>('/character');
    return response.data;
  },

  async createCharacter(request: CharacterCreateRequest): Promise<Character> {
    const response = await api.post<Character>('/character/create', request);
    return response.data;
  },

  async getStats(): Promise<Character> {
    const response = await api.get<Character>('/character/stats');
    return response.data;
  },

  async levelUp(): Promise<Character> {
    const response = await api.post<Character>('/character/levelup');
    return response.data;
  },
};