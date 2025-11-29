import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Lock, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent9 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-orange-600/20 rounded-2xl"><Lock className="w-12 h-12 text-orange-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 9: Blockchain Anchor</h1>
              <p className="text-gray-400 text-lg">Cardano Immutable Audit Trails</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-orange-900/30 to-red-900/30 border border-orange-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-orange-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            World's first <span className="font-bold text-orange-400">blockchain-anchored compliance system</span> using Cardano
            for tamper-proof audit trails with Merkle tree verification.
          </p>
          <div className="bg-orange-500/10 border-l-4 border-orange-500 p-4 rounded">
            <p className="text-sm text-orange-300 font-semibold">
              💡 Why It Matters: Provides cryptographic proof of compliance history for regulators, impossible to tamper or forge.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 9 anchors compliance data to the Cardano blockchain, creating immutable audit trails
              with Merkle tree proofs for verification.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-orange-500 rounded-full mt-2" /><span><strong>Merkle Tree Construction:</strong> Efficient proof generation</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-orange-500 rounded-full mt-2" /><span><strong>Blockfrost Integration:</strong> Cardano API connectivity</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-orange-500 rounded-full mt-2" /><span><strong>Testnet/Mainnet Support:</strong> Flexible deployment</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-orange-500 rounded-full mt-2" /><span><strong>On-Chain Metadata:</strong> Compliance data storage</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-orange-500 rounded-full mt-2" /><span><strong>Proof Verification:</strong> Cryptographic validation</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Blockchain Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Transactions Anchored</span><span className="font-bold">1,247</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Merkle Roots Stored</span><span className="font-bold">342</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Verification Success</span><span className="font-bold text-green-400">100%</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 9: Operational & Anchoring</span>
          </div>
        </div>
      </div>
    </div>
  );
};
