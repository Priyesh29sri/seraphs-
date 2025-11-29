import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { BarChart, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent11 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-purple-600/20 rounded-2xl"><BarChart className="w-12 h-12 text-purple-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 11: AgentOps Monitor</h1>
              <p className="text-gray-400 text-lg">Real-Time Performance Monitoring</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-purple-900/30 to-pink-900/30 border border-purple-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-purple-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First <span className="font-bold text-purple-400">multi-agent performance monitoring system</span> with
            Prometheus metrics and Grafana dashboards for compliance AI.
          </p>
          <div className="bg-purple-500/10 border-l-4 border-purple-500 p-4 rounded">
            <p className="text-sm text-purple-300 font-semibold">
              💡 Why It Matters: Ensures system health and SLA compliance with real-time monitoring and anomaly detection.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 11 monitors all system components in real-time, tracking performance metrics,
              detecting anomalies, and ensuring SLA compliance.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-purple-500 rounded-full mt-2" /><span><strong>Prometheus Metrics:</strong> Time-series data collection</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-purple-500 rounded-full mt-2" /><span><strong>Grafana Dashboards:</strong> Visual monitoring interfaces</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-purple-500 rounded-full mt-2" /><span><strong>Alert Management:</strong> Smart notification system</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-purple-500 rounded-full mt-2" /><span><strong>Performance Tracking:</strong> Per-agent metrics</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-purple-500 rounded-full mt-2" /><span><strong>Anomaly Detection:</strong> ML-based outlier identification</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Monitoring Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Metrics Collected</span><span className="font-bold">1.2M/day</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">System Uptime</span><span className="font-bold text-green-400">99.9%</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Anomalies Detected</span><span className="font-bold">12</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 11: Operational & Monitoring</span>
          </div>
        </div>
      </div>
    </div>
  );
};
