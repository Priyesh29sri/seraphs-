import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Network, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent6 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-cyan-600/20 rounded-2xl"><Network className="w-12 h-12 text-cyan-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 6: Knowledge Graph</h1>
              <p className="text-gray-400 text-lg">Dynamic Compliance Relationship Mapping</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-cyan-900/30 to-blue-900/30 border border-cyan-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-cyan-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            First <span className="font-bold text-cyan-400">dynamic compliance knowledge graph</span> using Neo4j to map relationships
            between regulations, entities, and obligations with temporal versioning.
          </p>
          <div className="bg-cyan-500/10 border-l-4 border-cyan-500 p-4 rounded">
            <p className="text-sm text-cyan-300 font-semibold">
              💡 Why It Matters: Enables intelligent querying of compliance relationships and impact analysis across interconnected regulations.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 6 builds and maintains a knowledge graph of compliance data, mapping relationships between
              regulations, obligations, entities, and changes over time.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-cyan-500 rounded-full mt-2" /><span><strong>Neo4j Graph Database:</strong> Optimized for relationship queries</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-cyan-500 rounded-full mt-2" /><span><strong>Entity Relationship Mapping:</strong> Connects regulations to entities</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-cyan-500 rounded-full mt-2" /><span><strong>Temporal Versioning:</strong> Tracks changes over time</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-cyan-500 rounded-full mt-2" /><span><strong>Cross-Regulation Linking:</strong> Identifies related requirements</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-cyan-500 rounded-full mt-2" /><span><strong>Query-Based Insights:</strong> Cypher queries for analysis</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Graph Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Nodes</span><span className="font-bold">12,847</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Relationships</span><span className="font-bold">34,521</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Query Performance</span><span className="font-bold text-green-400">&lt;50ms</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 6: Operational & Mapping</span>
          </div>
        </div>
      </div>
    </div>
  );
};
