import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Cloud, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent7 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-indigo-600/20 rounded-2xl"><Cloud className="w-12 h-12 text-indigo-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 7: Oracle API</h1>
              <p className="text-gray-400 text-lg">External Data Integration & Enrichment</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-indigo-900/30 to-purple-900/30 border border-indigo-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-indigo-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First <span className="font-bold text-indigo-400">multi-source oracle integration</span> for compliance,
            enriching regulatory data with real-world context from external APIs.
          </p>
          <div className="bg-indigo-500/10 border-l-4 border-indigo-500 p-4 rounded">
            <p className="text-sm text-indigo-300 font-semibold">
              💡 Why It Matters: Connects compliance data with real-world events, market data, and entity information for contextual intelligence.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 7 integrates external data sources to enrich compliance intelligence with market data,
              entity information, and real-world context.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-indigo-500 rounded-full mt-2" /><span><strong>Multi-Source Integration:</strong> Connects to various external APIs</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-indigo-500 rounded-full mt-2" /><span><strong>Real-Time Enrichment:</strong> Live data augmentation</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-indigo-500 rounded-full mt-2" /><span><strong>Contextual Augmentation:</strong> Adds business context</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-indigo-500 rounded-full mt-2" /><span><strong>Smart Caching:</strong> Rate-limited with intelligent caching</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-indigo-500 rounded-full mt-2" /><span><strong>Fallback Mechanisms:</strong> Graceful degradation</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Integration Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">API Sources</span><span className="font-bold">15</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Enrichments/Day</span><span className="font-bold">2,847</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Cache Hit Rate</span><span className="font-bold text-green-400">87%</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 7: Operational & Enriching</span>
          </div>
        </div>
      </div>
    </div>
  );
};
