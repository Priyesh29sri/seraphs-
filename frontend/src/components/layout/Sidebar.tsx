import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
    Database, Shield, GitCompare, Brain, Swords,
    Network, Cloud, ListChecks, Blocks, Workflow,
    Activity, Cpu, Home
} from 'lucide-react';
import { getAgentColor } from '../../theme';

const agents = [
    { id: 0, name: 'Dashboard', path: '/', icon: Home },
    { id: 1, name: 'Discovery & Ingestion', path: '/agent-1', icon: Database },
    { id: 2, name: 'Authenticity & Oracle', path: '/agent-2', icon: Shield },
    { id: 3, name: 'Diff & Change Classifier', path: '/agent-3', icon: GitCompare },
    { id: 4, name: 'Legal Intelligence', path: '/agent-4', icon: Brain },
    { id: 5, name: 'MAAD Debate', path: '/agent-5', icon: Swords },
    { id: 6, name: 'Knowledge Graph', path: '/agent-6', icon: Network },
    { id: 7, name: 'Oracle API', path: '/agent-7', icon: Cloud },
    { id: 8, name: 'Remediation Planner', path: '/agent-8', icon: ListChecks },
    { id: 9, name: 'ZK + Cardano', path: '/agent-9', icon: Blocks },
    { id: 10, name: 'Workflow UI', path: '/agent-10', icon: Workflow },
    { id: 11, name: 'AgentOps', path: '/agent-11', icon: Activity },
    { id: 12, name: 'Master Orchestrator', path: '/agent-12', icon: Cpu },
];

export const Sidebar = () => {
    const location = useLocation();

    return (
        <motion.aside
            className="fixed left-0 top-[73px] bottom-0 w-64 bg-dark-card/80 backdrop-blur-xl border-r border-dark-border overflow-y-auto custom-scrollbar"
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
        >
            <div className="p-4 space-y-2">
                {agents.map((agent, index) => {
                    const isActive = location.pathname === agent.path;
                    const Icon = agent.icon;
                    const color = agent.id > 0 ? getAgentColor(agent.id) : { bg: '#FF5F6D', glow: 'rgba(255, 95, 109, 0.3)' };

                    return (
                        <Link
                            key={agent.id}
                            to={agent.path}
                            className="block"
                        >
                            <motion.div
                                className={`
                  flex items-center gap-3 p-3 rounded-xl transition-all
                  ${isActive
                                        ? 'bg-white/10 shadow-glow'
                                        : 'hover:bg-white/5'
                                    }
                `}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.05 }}
                                whileHover={{ x: 5 }}
                            >
                                <div
                                    className="p-2 rounded-lg"
                                    style={{
                                        backgroundColor: isActive ? color.bg : 'transparent',
                                        boxShadow: isActive ? `0 0 20px ${color.glow}` : 'none',
                                    }}
                                >
                                    <Icon className="w-5 h-5" />
                                </div>

                                <div className="flex-1 min-w-0">
                                    <p className={`text-sm font-medium truncate ${isActive ? 'text-white' : 'text-gray-300'}`}>
                                        {agent.id > 0 && `Agent ${agent.id}`}
                                    </p>
                                    <p className="text-xs text-gray-400 truncate">
                                        {agent.name}
                                    </p>
                                </div>

                                {isActive && (
                                    <motion.div
                                        className="w-1 h-8 bg-sunset-glow rounded-full"
                                        layoutId="activeIndicator"
                                    />
                                )}
                            </motion.div>
                        </Link>
                    );
                })}
            </div>
        </motion.aside>
    );
};
