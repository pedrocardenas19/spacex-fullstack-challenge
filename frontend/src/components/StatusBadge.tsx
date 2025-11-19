import type { Launch } from '../types';

interface StatusBadgeProps {
  status: Launch['status'];
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const colors = {
    success: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    upcoming: 'bg-blue-100 text-blue-800',
  };

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-medium ${colors[status]}`}>
      {status}
    </span>
  );
}
