import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { GitCompare, ArrowLeft, TrendingUp, FileText, AlertCircle } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent3 = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button
            onClick={() => navigate('/dashboard')}
            className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
            whileHover={{ x: -5 }}
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Dashboard
          </motion.button>

          <div className="flex items-center gap-6">
            <div className="p-4 bg-pink-600/20 rounded-2xl">
              <GitCompare className="w-12 h-12 text-pink-400" />
            </div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 3: Diff & Change Classifier</h1>
              <p className="text-gray-400 text-lg">AI-Powered Semantic Change Analysis</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-pink-900/30 to-red-900/30 border border-pink-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-pink-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First <span className="font-bold text-pink-400">AI-powered semantic diff analysis system</span> that distinguishes
            material regulatory changes from cosmetic updates using NLP and impact scoring.
          </p>
          <div className="bg-pink-500/10 border-l-4 border-pink-500 p-4 rounded">
            <p className="text-sm text-pink-300 font-semibold">
              💡 Why It Matters: Automatically identifies critical regulatory changes requiring action,
              saving compliance teams from manual document comparison.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 3 performs intelligent diff analysis on regulatory documents, classifying changes by
              severity and impact. It uses NLP to understand semantic meaning, not just text differences.
            </p>

            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-pink-500 rounded-full mt-2" />
                <span><strong>Semantic Diff Analysis:</strong> NLP-based understanding of change meaning</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-pink-500 rounded-full mt-2" />
                <span><strong>Severity Classification:</strong> Critical, Major, Minor, Cosmetic</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-pink-500 rounded-full mt-2" />
                <span><strong>Impact Assessment:</strong> Automated scoring of business impact</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-pink-500 rounded-full mt-2" />
                <span><strong>Historical Tracking:</strong> Change timeline and patterns</span>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-2 h-2 bg-pink-500 rounded-full mt-2" />
                <span><strong>Smart Notifications:</strong> Alerts for material changes only</span>
              </li>
            </ul>
          </div>

          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-pink-500" />
                Change Analysis
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Changes Analyzed</span>
                    <span className="font-bold">342</span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Critical Changes</span>
                    <span className="font-bold text-red-400">12</span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-400">Accuracy Rate</span>
                    <span className="font-bold text-green-400">94%</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>

        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 3: Operational & Analyzing</span>
          </div>
        </div>
      </div>
    </div>
  );
};
