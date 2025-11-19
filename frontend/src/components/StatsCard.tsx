import type { Stats } from '../types';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

interface StatsCardProps {
  stats: Stats | null;
  loading: boolean;
}

export function StatsCard({ stats, loading }: StatsCardProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <p className="text-gray-500">Loading stats...</p>
      </div>
    );
  }

  if (!stats) return null;

  const yearData = Object.entries(stats.by_year)
    .map(([year, count]) => ({ year, count }))
    .sort((a, b) => parseInt(a.year) - parseInt(b.year));

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-8 border border-gray-200">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Launch Statistics</h2>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-5 border border-gray-200">
          <p className="text-xs text-gray-500 mb-2 font-medium uppercase tracking-wide">Total Launches</p>
          <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-5 border border-green-200">
          <p className="text-xs text-green-700 mb-2 font-medium uppercase tracking-wide">Successful</p>
          <p className="text-3xl font-bold text-green-700">{stats.by_status.success || 0}</p>
        </div>
        
        <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-5 border border-red-200">
          <p className="text-xs text-red-700 mb-2 font-medium uppercase tracking-wide">Failed</p>
          <p className="text-3xl font-bold text-red-700">{stats.by_status.failed || 0}</p>
        </div>
        
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-5 border border-blue-200">
          <p className="text-xs text-blue-700 mb-2 font-medium uppercase tracking-wide">Upcoming</p>
          <p className="text-3xl font-bold text-blue-700">{stats.by_status.upcoming || 0}</p>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-medium mb-4">Launches by Year</h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={yearData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis dataKey="year" stroke="#6b7280" />
            <YAxis stroke="#6b7280" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #e5e7eb',
                borderRadius: '0.5rem'
              }} 
            />
            <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
