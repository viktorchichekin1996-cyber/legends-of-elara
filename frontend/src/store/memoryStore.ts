import { create } from 'zustand';
import { memoryService, Memory } from '../services/memoryService';

interface MemoryState {
  memories: Memory[];
  isLoading: boolean;
  error: string | null;

  fetchMemories: () => Promise<void>;
  clearError: () => void;
}

export const useMemoryStore = create<MemoryState>((set) => ({
  memories: [],
  isLoading: false,
  error: null,

  fetchMemories: async () => {
    set({ isLoading: true, error: null });
    try {
      const memories = await memoryService.getMemories();
      set({ memories, isLoading: false });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка загрузки воспоминаний';
      set({ error: message, isLoading: false });
      throw err;
    }
  },

  clearError: () => set({ error: null }),
}));