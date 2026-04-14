import { create } from 'zustand';
import { questService } from '../services/questService';
import { Quest } from '../types/quest';

interface QuestState {
  quests: Quest[];
  isLoading: boolean;
  isProcessing: boolean; // ИСПРАВЛЕНИЕ: Добавлено поле
  error: string | null;

  fetchQuests: () => Promise<void>;
  cancelQuest: (questId: string) => Promise<void>;
  clearError: () => void;
}

export const useQuestStore = create<QuestState>((set, get) => ({
  quests: [],
  isLoading: false,
  isProcessing: false, // ИСПРАВЛЕНИЕ: Инициализация
  error: null,

  fetchQuests: async () => {
    set({ isLoading: true, error: null });
    try {
      const quests = await questService.getQuests();
      set({ quests, isLoading: false });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка загрузки квестов';
      set({ error: message, isLoading: false });
      throw err;
    }
  },

  cancelQuest: async (questId) => {
    set({ isProcessing: true, error: null }); // ИСПРАВЛЕНИЕ: Используем isProcessing
    try {
      await questService.cancelQuest(questId);
      // Обновляем список
      await get().fetchQuests();
      set({ isProcessing: false });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка отмены квеста';
      set({ error: message, isProcessing: false });
      throw err;
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));