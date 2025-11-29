import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { Card } from '../components/ui/card';
import { ContainerScroll } from '../components/ui/container-scroll-animation';
import { BackgroundPaths } from '../components/ui/background-paths';
import { LiquidButton } from '../components/ui/liquid-glass-button';
import { GlowCard } from '../components/ui/spotlight-card';
import { InteractiveRobotSpline } from '../components/ui/interactive-3d-robot';
import {
    Database, Shield, GitCompare, Brain, Users, Network,
    Cloud, Wrench, Lock, Layout, BarChart, Cpu, ArrowLeft
} from 'lucide-react';

const API_URL = 'http://localhost:8000';

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

export const Dashboard = () => {
    const navigate = useNavigate();
    const [metrics, setMetrics] = useState({ sources: 20, accuracy: 95, obligations: 7 });

    useEffect(() => {
        fetch(`${API_URL}/api/metrics`)
            .then(res => res.json())
            .then(data => {
                setMetrics({
                    sources: data.sources_monitored || 20,
                    accuracy: data.avg_confidence ? Math.round(data.avg_confidence * 100) : 95,
                    obligations: data.obligations_extracted || 7
                });
            })
            .catch(err => console.error('Failed to fetch metrics:', err));
    }, []);

    return (
        <div className="min-h-screen bg-gray-900 text-white">
            {/* Background Paths Hero Section */}
            <BackgroundPaths
                title="Stored on Cardano blockchain"
                subtitle="The Future of Regulatory Compliance is Here"
            />

            {/* Scroll Animation Section */}
            <div className="bg-black">
                <ContainerScroll
                    titleComponent={
                        <>
                            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
                                Unleash the power of{" "}
                                <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                                    AI-Powered Compliance
                                </span>
                            </h2>
                            <p className="text-gray-400 text-lg mt-4">
                                Scroll to explore our intelligent agent ecosystem
                            </p>
                        </>
                    }
                >
                    <div className="w-full h-full bg-gray-800 rounded-2xl p-8 flex flex-col">
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 flex-1">
                            {agents.map((agent) => {
                                const Icon = agent.icon;
                                return (
                                    <div
                                        key={agent.id}
                                        className="bg-gray-700/50 p-4 rounded-xl text-center hover:bg-gray-700 transition-all cursor-pointer"
                                        onClick={() => navigate(`/agent/${agent.id}`)}
                                    >
                                        <div
                                            className="w-12 h-12 mx-auto mb-3 rounded-lg flex items-center justify-center"
                                            style={{ backgroundColor: `${agent.color}20` }}
                                        >
                                            <Icon className="w-6 h-6" style={{ color: agent.color }} />
                                        </div>
                                        <p className="text-xs font-semibold text-white mb-1">Agent {agent.id}</p>
                                        <p className="text-xs text-gray-400">{agent.name}</p>
                                    </div>
                                );
                            })}
                        </div>

                        {/* Explore Agents Button - Inside Container */}
                        <div className="mt-8 flex items-center justify-center">
                            <LiquidButton
                                size="xxl"
                                className="text-white text-xl font-bold px-16"
                                onClick={() => navigate('/agents')}
                            >
                                Explore Agents
                            </LiquidButton>
                        </div>
                    </div>
                </ContainerScroll>
            </div>

            {/* Real-Time Monitoring Section */}
            <div className="bg-black py-16">
                <div className="max-w-7xl mx-auto px-6">
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                        className="text-4xl md:text-5xl font-bold text-center mb-12 bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
                    >
                        Real-Time Monitoring
                    </motion.h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: 0.1 }}
                        >
                            <GlowCard glowColor="blue" customSize className="w-full h-48">
                                <div className="flex flex-col justify-between h-full">
                                    <div>
                                        <p className="text-gray-400 text-sm font-medium mb-2">Active Updates</p>
                                        <p className="text-4xl font-bold text-white">{metrics.sources}</p>
                                    </div>
                                    <p className="text-xs text-gray-500">Regulatory Updates</p>
                                </div>
                            </GlowCard>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: 0.2 }}
                        >
                            <GlowCard glowColor="purple" customSize className="w-full h-48">
                                <div className="flex flex-col justify-between h-full">
                                    <div>
                                        <p className="text-gray-400 text-sm font-medium mb-2">Urgent Deadlines</p>
                                        <p className="text-4xl font-bold text-white">3</p>
                                    </div>
                                    <p className="text-xs text-gray-500">Time-Sensitive</p>
                                </div>
                            </GlowCard>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: 0.3 }}
                        >
                            <GlowCard glowColor="green" customSize className="w-full h-48">
                                <div className="flex flex-col justify-between h-full">
                                    <div>
                                        <p className="text-gray-400 text-sm font-medium mb-2">Open Obligations</p>
                                        <p className="text-4xl font-bold text-white">{metrics.obligations}</p>
                                    </div>
                                    <p className="text-xs text-gray-500">Pending Review</p>
                                </div>
                            </GlowCard>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.4, delay: 0.4 }}
                        >
                            <GlowCard glowColor="orange" customSize className="w-full h-48">
                                <div className="flex flex-col justify-between h-full">
                                    <div>
                                        <p className="text-gray-400 text-sm font-medium mb-2">System Health</p>
                                        <p className="text-4xl font-bold text-white">{metrics.accuracy}%</p>
                                    </div>
                                    <p className="text-xs text-gray-500">Overall Accuracy</p>
                                </div>
                            </GlowCard>
                        </motion.div>
                    </div>
                </div>
            </div>

            {/* Whobee Robot Section */}
            <div className="relative w-full h-screen bg-black overflow-hidden">
                <InteractiveRobotSpline
                    scene="https://prod.spline.design/PyzDhpQ9E5f1E3MT/scene.splinecode"
                    className="absolute inset-0 z-0"
                />

                <div className="absolute top-0 left-0 right-0 z-10 pt-16 md:pt-20 px-4 md:px-8 pointer-events-none">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, delay: 0.5 }}
                        className="text-center text-white drop-shadow-2xl w-full max-w-4xl mx-auto"
                    >
                        <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent leading-tight">
                            One brain can make mistakes.<br />Twelve minds working together don't.
                        </h2>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};
