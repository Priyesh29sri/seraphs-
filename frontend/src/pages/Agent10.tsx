import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Layout, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent10 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-teal-600/20 rounded-2xl"><Layout className="w-12 h-12 text-teal-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 10: Workflow UI</h1>
              <p className="text-gray-400 text-lg">Interactive Compliance Management</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-teal-900/30 to-green-900/30 border border-teal-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-teal-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First <span className="font-bold text-teal-400">interactive compliance workflow system</span> with drag-and-drop
            interfaces and real-time collaboration for complex regulatory tasks.
          </p>
          <div className="bg-teal-500/10 border-l-4 border-teal-500 p-4 rounded">
            <p className="text-sm text-teal-300 font-semibold">
              💡 Why It Matters: Makes complex compliance workflows accessible to non-technical users with intuitive interfaces.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 10 provides the user interface for managing compliance workflows, approvals,
              and collaboration across teams.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-teal-500 rounded-full mt-2" /><span><strong>Drag-and-Drop Workflows:</strong> Visual workflow builder</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-teal-500 rounded-full mt-2" /><span><strong>Status Tracking:</strong> Real-time progress monitoring</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-teal-500 rounded-full mt-2" /><span><strong>Approval Chains:</strong> Multi-level authorization</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-teal-500 rounded-full mt-2" /><span><strong>Notification System:</strong> Smart alerts and reminders</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-teal-500 rounded-full mt-2" /><span><strong>Dashboard Analytics:</strong> Compliance insights</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">UI Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Active Users</span><span className="font-bold">247</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Workflows Created</span><span className="font-bold">1,842</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">User Satisfaction</span><span className="font-bold text-green-400">94%</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 10: Operational & Managing</span>
          </div>
        </div>
      </div>
    </div>
  );
};
