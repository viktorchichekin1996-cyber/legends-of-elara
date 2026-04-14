import { create } from 'zustand';
import { characterService } from '../services/characterService';
import { Character, CharacterCreateRequest } from '../types/character';
import { AxiosError } from 'axios';

interface CharacterState {
  character: Character | null;
  isLoading: boolean;
  error: string | null;
  needsCreation: boolean;

  fetchCharacter: () => Promise<void>;
  createCharacter: (request: CharacterCreateRequest) => Promise<void>;
  updateCharacter: (updates: Partial<Character>) => void;
  clearError: () => void;
}

export const useCharacterStore = create<CharacterState>((set) => ({
  character: null,
  isLoading: false,
  error: null,
  needsCreation: false,

  fetchCharacter: async () => {
    set({ isLoading: true, error: null });
    try {
      const character = await characterService.getCharacter();
      set({ character, isLoading: false, needsCreation: false });
    } catch (err) {
      const axiosError = err as AxiosError;
      // Если 404 — персонажа нет, нужно создать
      if (axiosError.response?.status === 404) {
        set({ character: null, isLoading: false, needsCreation: true, error: null });
        return;
      }
      const message = axiosError.message || 'Ошибка загрузки персонажа';
      set({ error: message, isLoading: false, needsCreation: false });
      throw err;
    }
  },

  createCharacter: async (request) => {
    set({ isLoading: true, error: null });
    try {
      const character = await characterService.createCharacter(request);
      set({ character, isLoading: false, needsCreation: false });
    } catch (err) {
      const axiosError = err as AxiosError;
      // ИСПРАВЛЕНИЕ: Приведение типа для доступа к detail
      const responseData = axiosError.response?.data as { detail?: string } | undefined;
      const message = responseData?.detail || axiosError.message || 'Ошибка создания персонажа';
      set({ error: message, isLoading: false });
      throw err;
    }
  },

  updateCharacter: (updates) => {
    set((state) => ({
      character: state.character ? { ...state.character, ...updates } : null,
    }));
  },

  clearError: () => {
    set({ error: null });
  },
}));