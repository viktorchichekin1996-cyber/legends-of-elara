import { create } from 'zustand';
import { inventoryService } from '../services/inventoryService';
import { InventoryItem } from '../types/item';
import { useCharacterStore } from './characterStore';

interface InventoryState {
  items: InventoryItem[];
  isLoading: boolean;
  isProcessing: boolean;
  error: string | null;

  fetchInventory: () => Promise<void>;
  equipItem: (inventoryId: string) => Promise<void>;
  unequipItem: (slot: string) => Promise<void>;
  clearError: () => void;
}

export const useInventoryStore = create<InventoryState>((set, get) => ({
  items: [],
  isLoading: false,
  isProcessing: false,
  error: null,

  fetchInventory: async () => {
    set({ isLoading: true, error: null });
    try {
      const items = await inventoryService.getInventory();
      set({ items, isLoading: false });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка загрузки инвентаря';
      set({ error: message, isLoading: false });
      throw err;
    }
  },

  equipItem: async (inventoryId) => {
    set({ isProcessing: true, error: null });
    try {
      await inventoryService.equipItem(inventoryId);
      // Обновляем инвентарь и персонажа
      await get().fetchInventory();
      await useCharacterStore.getState().fetchCharacter();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка экипировки';
      set({ error: message, isProcessing: false });
      throw err;
    }
  },

  unequipItem: async (slot) => {
    set({ isProcessing: true, error: null });
    try {
      await inventoryService.unequipItem(slot);
      await get().fetchInventory();
      await useCharacterStore.getState().fetchCharacter();
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Ошибка снятия предмета';
      set({ error: message, isProcessing: false });
      throw err;
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));