import { create } from 'zustand';
import { eventService, ActionRequest } from '../services/eventService';
import { GameEvent, EventActionResult } from '../types/event';
import { useCharacterStore } from './characterStore';

interface GameState {
  currentEvent: GameEvent | null;
  isLoading: boolean;
  isProcessing: boolean;
  error: string | null;
  lastResult: EventActionResult | null;

  fetchEvent: () => Promise<void>;
  handleAction: (request: ActionRequest) => Promise<void>;
  handleChoice: (choiceId: string) => Promise<void>;
  clearError: () => void;
  clearResult: () => void;
}

export const useGameStore = create<GameState>((set, get) => ({
  currentEvent: null,
  isLoading: false,
  isProcessing: false,
  error: null,
  lastResult: null,

  fetchEvent: async () => {
    set({ isLoading: true, error: null });
    try {
      const event = await eventService.getCurrentEvent();
      set({ currentEvent: event, isLoading: false });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка загрузки события';
      set({ error: message, isLoading: false });
      throw err;
    }
  },

  handleAction: async (request) => {
    set({ isProcessing: true, error: null, lastResult: null });
    try {
      const result = await eventService.performAction(request);
      
      // Обновляем персонажа если есть изменения
      if (result.character_updates) {
        useCharacterStore.getState().fetchCharacter();
      }

      set({ 
        lastResult: result, 
        isProcessing: false,
        currentEvent: result.next_event || get().currentEvent,
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка выполнения действия';
      set({ error: message, isProcessing: false });
      throw err;
    }
  },

  handleChoice: async (choiceId) => {
    set({ isProcessing: true, error: null, lastResult: null });
    try {
      const result = await eventService.makeChoice(choiceId);
      
      if (result.character_updates) {
        useCharacterStore.getState().fetchCharacter();
      }

      set({ 
        lastResult: result, 
        isProcessing: false,
        currentEvent: result.next_event || get().currentEvent,
      });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка выбора';
      set({ error: message, isProcessing: false });
      throw err;
    }
  },

  clearError: () => {
    set({ error: null });
  },

  clearResult: () => {
    set({ lastResult: null });
  },
}));