import type { Launch, Stats } from './types';

const getApiBaseUrl = () => {
  if (import.meta.env.PROD) {
    return window.location.origin;
  }
  return import.meta.env.VITE_API_URL || 'http://localhost:8000';
};

export const api = {
  async getLaunches(limit = 500): Promise<Launch[]> {
    const response = await fetch(`${getApiBaseUrl()}/launches?limit=${limit}`);
    if (!response.ok) throw new Error('Failed to fetch launches');
    return response.json();
  },

  async getLaunch(id: string): Promise<Launch> {
    const response = await fetch(`${getApiBaseUrl()}/launches/${id}`);
    if (!response.ok) throw new Error('Failed to fetch launch');
    return response.json();
  },

  async getStats(): Promise<Stats> {
    const response = await fetch(`${getApiBaseUrl()}/stats/summary`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  },
};
