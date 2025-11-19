import type { Launch, Stats } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || window.location.origin;

export const api = {
  async getLaunches(limit = 500): Promise<Launch[]> {
    const response = await fetch(`${API_BASE_URL}/launches?limit=${limit}`);
    if (!response.ok) throw new Error('Failed to fetch launches');
    return response.json();
  },

  async getLaunch(id: string): Promise<Launch> {
    const response = await fetch(`${API_BASE_URL}/launches/${id}`);
    if (!response.ok) throw new Error('Failed to fetch launch');
    return response.json();
  },

  async getStats(): Promise<Stats> {
    const response = await fetch(`${API_BASE_URL}/stats/summary`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },
};
