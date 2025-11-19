import type { Launch } from '../types';
import { StatusBadge } from './StatusBadge';

interface LaunchModalProps {
  launch: Launch | null;
  onClose: () => void;
}

export function LaunchModal({ launch, onClose }: LaunchModalProps) {
  if (!launch) return null;

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-gray-200" onClick={(e) => e.stopPropagation()}>
        <div className="p-6">
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-2xl font-bold text-gray-900">{launch.mission_name}</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-full p-2 transition-all"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-600">Rocket</p>
              <p className="text-lg font-medium text-gray-900">{launch.rocket_id}</p>
            </div>

            <div>
              <p className="text-sm text-gray-600">Launch Date</p>
              <p className="text-lg text-gray-900">{formatDate(launch.launch_date_utc)}</p>
            </div>

            <div>
              <p className="text-sm text-gray-600">Status</p>
              <div className="mt-1">
                <StatusBadge status={launch.status} />
              </div>
            </div>

            {launch.launchpad_id && (
              <div>
                <p className="text-sm text-gray-600">Launchpad</p>
                <p className="text-lg text-gray-900">{launch.launchpad_id}</p>
              </div>
            )}

            {launch.details && (
              <div>
                <p className="text-sm text-gray-600">Details</p>
                <p className="text-gray-900 leading-relaxed">{launch.details}</p>
              </div>
            )}

            {(launch.article_link || launch.wikipedia || launch.video_link) && (
              <div>
                <p className="text-sm text-gray-600 mb-3">Links</p>
                <div className="flex flex-wrap gap-3">
                  {launch.article_link && (
                    <a
                      href={launch.article_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-all shadow-sm"
                    >
                      📄 Article
                    </a>
                  )}
                  {launch.wikipedia && (
                    <a
                      href={launch.wikipedia}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-all shadow-sm"
                    >
                      📖 Wikipedia
                    </a>
                  )}
                  {launch.video_link && (
                    <a
                      href={launch.video_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 px-4 py-2.5 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-all shadow-sm"
                    >
                      🎥 Video
                    </a>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
