import { api } from './api';
import { InventoryItem } from '../types/item';

export interface EquipResponse {
  success: boolean;
  message: string;
}

export const inventoryService = {
  async getInventory(): Promise<InventoryItem[]> {
    const response = await api.get<InventoryItem[]>('/inventory');
    return response.data;
  },

  async equipItem(inventoryId: string): Promise<EquipResponse> {
    const response = await api.post<EquipResponse>('/inventory/equip', { inventory_id: inventoryId });
    return response.data;
  },

  async unequipItem(slot: string): Promise<EquipResponse> {
    const response = await api.post<EquipResponse>('/inventory/unequip', { slot });
    return response.data;
  },
};