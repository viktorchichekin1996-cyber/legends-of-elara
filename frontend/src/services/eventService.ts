import { api } from './api';
import { GameEvent, EventActionResult } from '../types/event';

export interface ActionRequest {
  action: string;
  choice_id?: string;
  item_id?: string;
}

export const eventService = {
  async getCurrentEvent(): Promise<GameEvent> {
    const response = await api.get<GameEvent>('/event/current');
    return response.data;
  },

  async performAction(request: ActionRequest): Promise<EventActionResult> {
    const response = await api.post<EventActionResult>('/event/action', request);
    return response.data;
  },

  async makeChoice(choiceId: string): Promise<EventActionResult> {
    const response = await api.post<EventActionResult>('/event/choice', { choice_id: choiceId });
    return response.data;
  },
};