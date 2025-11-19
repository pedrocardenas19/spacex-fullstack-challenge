export interface Launch {
  launch_id: string;
  mission_name: string;
  rocket_id: string;
  launch_date_utc: string;
  launch_date_unix: number;
  status: 'success' | 'failed' | 'upcoming';
  launchpad_id?: string;
  details?: string;
  article_link?: string;
  wikipedia?: string;
  video_link?: string;
}

export interface Stats {
  total: number;
  by_status: Record<string, number>;
  by_year: Record<string, number>;
}
