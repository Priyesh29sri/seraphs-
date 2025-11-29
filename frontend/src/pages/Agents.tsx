import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Database, Shield, GitCompare, Brain, Users, Network,
    Cloud, Wrench, Lock, Layout, BarChart, Cpu, ArrowLeft
} from 'lucide-react';

const agents = [
    { id: 1, name: 'Discovery & Ingestion', icon: Database, desc: 'Monitors 20+ regulatory sources in real-time', color: '#3B82F6' },
    { id: 2, name: 'Authenticity Oracle', icon: Shield, desc: 'Verifies document authenticity and integrity', color: '#8B5CF6' },
    { id: 3, name: 'Diff & Change Classifier', icon: GitCompare, desc: 'Classifies document changes and diffs', color: '#EC4899' },
    { id: 4, name: 'Legal Intelligence LLM', icon: Brain, desc: 'Extracts obligations using AI', color: '#F59E0B' },
    { id: 5, name: 'MAAD Adversarial Debate', icon: Users, desc: 'Multi-agent debate for verification', color: '#10B981' },
    { id: 6, name: 'Knowledge Graph', icon: Network, desc: 'Builds compliance knowledge graph', color: '#06B6D4' },
    { id: 7, name: 'Oracle API', icon: Cloud, desc: 'External data integration', color: '#6366F1' },
    { id: 8, name: 'Remediation Engine', icon: Wrench, desc: 'Generates compliance fixes', color: '#EF4444' },
    { id: 9, name: 'Blockchain Anchor', icon: Lock, desc: 'Immutable audit trail', color: '#F97316' },
    { id: 10, name: 'Workflow UI', icon: Layout, desc: 'User interface and workflow', color: '#14B8A6' },
    { id: 11, name: 'AgentOps Monitor', icon: BarChart, desc: 'Performance monitoring', color: '#A855F7' },
    { id: 12, name: 'Orchestrator', icon: Cpu, desc: 'Coordinates all agents', color: '#FF5F6D' },
];

export const AgentsPage = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-black text-white">
            {/* Header */}
            <div className="bg-black border-b border-gray-800">
                <div className="max-w-7xl mx-auto px-6 py-8">
                    <motion.button
                        onClick={() => navigate('/dashboard')}
                        className="mb-6 flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
                        whileHover={{ x: -5 }}
                    >
                        <ArrowLeft className="w-5 h-5" />
                        Back to Dashboard
                    </motion.button>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <h1 className="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
                            Our 12 AI Agents
                        </h1>
                        <p className="text-xl text-gray-400 font-light">
                            Explore each specialized agent and their unique capabilities
                        </p>
                    </motion.div>
                </div>
            </div>

            {/* Agents Grid */}
            <div className="max-w-7xl mx-auto px-6 py-16">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {agents.map((agent, index) => {
                        const Icon = agent.icon;
                        return (
                            <motion.div
                                key={agent.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.4, delay: index * 0.05 }}
                                className="group relative bg-gray-900/50 border border-gray-800 rounded-2xl p-8 hover:bg-gray-900/70 hover:border-gray-700 transition-all cursor-pointer hover:scale-105"
                                onClick={() => navigate(`/agent/${agent.id}`)}
                            >
                                {/* Icon */}
                                <div
                                    className="w-16 h-16 mb-6 rounded-xl flex items-center justify-center"
                                    style={{ backgroundColor: `${agent.color}20` }}
                                >
                                    <Icon className="w-8 h-8" style={{ color: agent.color }} />
                                </div>

                                {/* Content */}
                                <div>
                                    <div className="flex items-center gap-3 mb-3">
                                        <span className="text-sm font-semibold text-gray-500">
                                            Agent {agent.id}
                                        </span>
                                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                                    </div>
                                    <h3 className="text-xl font-bold text-white mb-3">
                                        {agent.name}
                                    </h3>
                                    <p className="text-gray-400 text-sm leading-relaxed">
                                        {agent.desc}
                                    </p>
                                </div>

                                {/* Hover Arrow */}
                                <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                    </svg>
                                </div>
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* Footer */}
            <div className="bg-black border-t border-gray-800 py-8 text-center text-gray-500">
                <p>© 2024 Seraphs - Multi-Agent Compliance Intelligence</p>
            </div>
        </div>
    );
};
