import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Wrench, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent8 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-red-600/20 rounded-2xl"><Wrench className="w-12 h-12 text-red-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 8: Remediation Engine</h1>
              <p className="text-gray-400 text-lg">AI-Generated Compliance Fixes</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-red-900/30 to-orange-900/30 border border-red-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-red-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First <span className="font-bold text-red-400">AI-powered remediation engine</span> that generates actionable compliance fixes,
            not just identifies problems.
          </p>
          <div className="bg-red-500/10 border-l-4 border-red-500 p-4 rounded">
            <p className="text-sm text-red-300 font-semibold">
              💡 Why It Matters: Provides concrete solutions and implementation templates, dramatically reducing time-to-compliance.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 8 automatically generates remediation suggestions for compliance gaps, providing code snippets,
              policy templates, and implementation guidance.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-red-500 rounded-full mt-2" /><span><strong>Automated Fix Generation:</strong> AI-generated solutions</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-red-500 rounded-full mt-2" /><span><strong>Code/Policy Suggestions:</strong> Concrete implementation examples</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-red-500 rounded-full mt-2" /><span><strong>Risk-Prioritized:</strong> Addresses highest-risk gaps first</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-red-500 rounded-full mt-2" /><span><strong>Implementation Templates:</strong> Ready-to-use frameworks</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-red-500 rounded-full mt-2" /><span><strong>Validation Workflows:</strong> Verify fix effectiveness</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Remediation Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Fixes Generated</span><span className="font-bold">847</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Implementation Rate</span><span className="font-bold text-green-400">76%</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Time Saved</span><span className="font-bold text-green-400">1,200hrs</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 8: Operational & Remediating</span>
          </div>
        </div>
      </div>
    </div>
  );
};
