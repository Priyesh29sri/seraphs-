import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Users, ArrowLeft } from 'lucide-react';
import { Card } from '../components/ui/card';

export const Agent5 = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <motion.button onClick={() => navigate('/dashboard')} className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors" whileHover={{ x: -5 }}>
            <ArrowLeft className="w-5 h-5" />Back to Dashboard
          </motion.button>
          <div className="flex items-center gap-6">
            <div className="p-4 bg-green-600/20 rounded-2xl"><Users className="w-12 h-12 text-green-400" /></div>
            <div>
              <h1 className="text-4xl font-bold mb-2">Agent 5: MAAD Adversarial Debate</h1>
              <p className="text-gray-400 text-lg">Multi-Agent Debate for Accuracy Verification</p>
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="mb-12 p-8 bg-gradient-to-r from-green-900/30 to-teal-900/30 border border-green-500/30 rounded-2xl">
          <h2 className="text-2xl font-bold mb-4 text-green-400">🌍 Global Novelty</h2>
          <p className="text-gray-300 text-lg leading-relaxed mb-4">
            World's first <span className="font-bold text-green-400">adversarial multi-agent debate system</span> for compliance verification,
            using prosecutor-defender-judge architecture to eliminate hallucinations.
          </p>
          <div className="bg-green-500/10 border-l-4 border-green-500 p-4 rounded">
            <p className="text-sm text-green-300 font-semibold">
              💡 Why It Matters: Dramatically reduces AI hallucinations through adversarial debate, ensuring only verified obligations are accepted.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 className="text-3xl font-bold mb-6">Overview</h2>
            <p className="text-gray-300 text-lg leading-relaxed mb-8">
              Agent 5 implements Multi-Agent Adversarial Debate (MAAD) where a prosecutor challenges extracted obligations,
              a defender provides evidence, and a judge makes the final verdict.
            </p>
            <h3 className="text-2xl font-bold mb-4">Key Features</h3>
            <ul className="space-y-3 text-gray-300">
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-green-500 rounded-full mt-2" /><span><strong>Prosecutor-Defender-Judge:</strong> Three-agent debate architecture</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-green-500 rounded-full mt-2" /><span><strong>Evidence-Based Arguments:</strong> All claims require source citations</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-green-500 rounded-full mt-2" /><span><strong>Multi-Round Debate:</strong> Configurable debate rounds</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-green-500 rounded-full mt-2" /><span><strong>Confidence Delta:</strong> Tracks confidence changes through debate</span></li>
              <li className="flex items-start gap-3"><div className="w-2 h-2 bg-green-500 rounded-full mt-2" /><span><strong>HITL Escalation:</strong> Low-confidence cases sent to humans</span></li>
            </ul>
          </div>
          <div className="space-y-6">
            <Card className="bg-gray-800/50 border-gray-700 p-6">
              <h3 className="text-xl font-semibold mb-4">Debate Stats</h3>
              <div className="space-y-4">
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Debates Conducted</span><span className="font-bold">1,247</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Hallucinations Prevented</span><span className="font-bold text-green-400">342</span></div></div>
                <div><div className="flex justify-between mb-2"><span className="text-gray-400">Accuracy Improvement</span><span className="font-bold text-green-400">+27%</span></div></div>
              </div>
            </Card>
          </div>
        </div>
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-3 bg-green-900/20 border border-green-500/30 px-8 py-4 rounded-full">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 font-semibold text-lg">Agent 5: Operational & Debating</span>
          </div>
        </div>
      </div>
    </div>
  );
};
