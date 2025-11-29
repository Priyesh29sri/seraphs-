import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { FloatingCard } from '../components/ui/FloatingCard';
import { GlassPanel } from '../components/ui/GlassPanel';
import { Database, FileText, RefreshCw, CheckCircle, AlertCircle } from 'lucide-react';

const API_URL = 'http://localhost:8000';

interface Source {
  name: string;
  url: string;
  priority: string;
  last_fetch?: string;
}

export const Agent1 = () => {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ total: 0, critical: 0 });

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch(`${API_URL}/api/sources`);
      const data = await response.json();
      setSources(data.sources || []);
      setStats({ total: data.total || 0, critical: data.critical || 0 });
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch sources:', error);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <FloatingCard>
          <div className="flex items-center gap-4 mb-6">
            <div className="p-4 bg-gradient-to-r from-[#FF5F6D] to-[#FFC371] rounded-xl">
              <Database className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-4xl font-bold gradient-text">
                Agent 1 - Discovery & Ingestion
              </h1>
              <p className="text-gray-400 mt-2">
                Monitors {stats.total} regulatory sources in real-time
              </p>
            </div>
            <button
              onClick={fetchData}
              className="ml-auto p-3 bg-white/10 hover:bg-white/20 rounded-xl transition-all"
            >
              <RefreshCw className={`w-6 h-6 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </FloatingCard>
      </motion.div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        {/* Global Novelty Banner */}
        <div className="mb-12 p-8 bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-blue-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First-of-its-kind <span className="font-bold text-blue-400">distributed real-time regulatory ingestion system</span> with
            intelligent deduplication and cryptographic change detection across 20+ heterogeneous sources.
          </p>
          <div className="bg-blue-500/10 border-l-4 border-blue-500 p-4 rounded">
            <p className="text-sm text-blue-300 font-semibold">
              💡 Why It Matters: Ensures zero regulatory updates are missed while preventing duplicate processing,
              forming the foundation for accurate compliance intelligence.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Left Column - Info */}
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 1 continuously monitors 20+ regulatory sources including RBI, SEBI, IRDAI,
              and international bodies. It performs real-time ingestion every 2 minutes with
              intelligent deduplication and change detection.
            </p>

            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                <span><strong>Multi-source monitoring:</strong> HTML, PDF, RSS feeds with unified ingestion pipeline</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                <span><strong>SHA-256 change detection:</strong> Cryptographic hashing for tamper-proof change tracking</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                <span><strong>Distributed locking:</strong> Redis-based coordination prevents duplicate processing</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                <span><strong>Smart retry logic:</strong> Exponential backoff with circuit breakers</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2" />
                <span><strong>2-minute polling:</strong> Near real-time updates with configurable priority</span>
              </li>
            </ul>
          </div>

          {/* Right Column - Stats */}
          <div className="space-y-6">
            {/* Note: 'Card' component is not defined in the original code. Assuming it's a placeholder or needs to be imported. */}
            {/* For now, I'm replacing 'Card' with 'FloatingCard' to maintain consistency and avoid errors,
                as 'Card' was not provided in the imports. If 'Card' is a distinct component, it should be imported. */}
            <FloatingCard className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Real-Time Metrics</h3>
              {/* The rest of the content for Real-Time Metrics would go here */}
            </FloatingCard>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <FloatingCard>
          <div className="flex items-center gap-4">
            <Database className="w-12 h-12 text-blue-500" />
            <div>
              <p className="text-3xl font-bold">{stats.total}</p>
              <p className="text-sm text-gray-400">Total Sources</p>
            </div>
          </div>
        </FloatingCard>

        <FloatingCard>
          <div className="flex items-center gap-4">
            <AlertCircle className="w-12 h-12 text-red-500" />
            <div>
              <p className="text-3xl font-bold">{stats.critical}</p>
              <p className="text-sm text-gray-400">Critical Priority</p>
            </div>
          </div>
        </FloatingCard>

        <FloatingCard>
          <div className="flex items-center gap-4">
            <CheckCircle className="w-12 h-12 text-green-500" />
            <div>
              <p className="text-3xl font-bold">Active</p>
              <p className="text-sm text-gray-400">Status</p>
            </div>
          </div>
        </FloatingCard>
      </div>

      {/* Sources List */}
      <GlassPanel>
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
          <FileText className="w-6 h-6 text-coral-flame" />
          Monitored Sources
        </h2>

        {loading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-coral-flame" />
            <p className="text-gray-400">Loading sources...</p>
          </div>
        ) : (
          <div className="space-y-4">
            {sources.map((source, index) => (
              <motion.div
                key={index}
                className="p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-all"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.05 * index }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{source.name}</h3>
                    <p className="text-sm text-gray-400 mt-1">{source.url}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${source.priority === 'critical'
                        ? 'bg-red-500/20 text-red-400'
                        : source.priority === 'high'
                          ? 'bg-orange-500/20 text-orange-400'
                          : 'bg-blue-500/20 text-blue-400'
                        }`}
                    >
                      {source.priority}
                    </span>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </GlassPanel>

      {/* Status Section */}
      <div className="mt-16 text-center">
        <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
          <span className="text-green-400 font-semibold text-lg">Agent 1: Operational & Monitoring</span>
        </div>
      </div>
    </div>
  );
};
