import { useState, useEffect, useMemo } from 'react';
import { api } from './api';
import type { Launch, Stats } from './types';
import { StatsCard } from './components/StatsCard';
import { LaunchTable } from './components/LaunchTable';
import { Pagination } from './components/Pagination';
import { LaunchModal } from './components/LaunchModal';

function App() {
  const [launches, setLaunches] = useState<Launch[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLaunch, setSelectedLaunch] = useState<Launch | null>(null);
  
  // Filters
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [launchesData, statsData] = await Promise.all([
          api.getLaunches(),
          api.getStats(),
        ]);
        setLaunches(launchesData);
        setStats(statsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredLaunches = useMemo(() => {
    let filtered = launches;

    if (statusFilter !== 'all') {
      filtered = filtered.filter((launch) => launch.status === statusFilter);
    }

    if (searchQuery) {
      filtered = filtered.filter((launch) =>
        launch.mission_name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    return filtered;
  }, [launches, statusFilter, searchQuery]);

  const totalPages = Math.ceil(filteredLaunches.length / pageSize);
  const paginatedLaunches = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return filteredLaunches.slice(start, start + pageSize);
  }, [filteredLaunches, currentPage, pageSize]);

  useEffect(() => {
    setCurrentPage(1);
  }, [statusFilter, searchQuery, pageSize]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-2">Error loading data</p>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">SpaceX Launches</h1>

        <StatsCard stats={stats} loading={loading} />

        <div className="mb-6 flex flex-col sm:flex-row gap-3">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search missions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
            />
          </div>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white cursor-pointer transition-all hover:border-gray-400"
          >
            <option value="all">All Status</option>
            <option value="success">Success</option>
            <option value="failed">Failed</option>
            <option value="upcoming">Upcoming</option>
          </select>

          <select
            value={pageSize}
            onChange={(e) => setPageSize(Number(e.target.value))}
            className="px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white cursor-pointer transition-all hover:border-gray-400"
          >
            <option value="10">10 per page</option>
            <option value="20">20 per page</option>
            <option value="50">50 per page</option>
          </select>
        </div>

        {filteredLaunches.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <p className="text-gray-500 text-lg">No launches found</p>
          </div>
        ) : (
          <>
            <LaunchTable launches={paginatedLaunches} onLaunchClick={setSelectedLaunch} />
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}

        <LaunchModal launch={selectedLaunch} onClose={() => setSelectedLaunch(null)} />
      </div>
    </div>
  );
}

export default App;
