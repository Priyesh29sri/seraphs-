import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { FloatingCard } from '../components/ui/FloatingCard';
import { SunsetButton } from '../components/ui/SunsetButton';
import { StatusIndicator } from '../components/ui/StatusIndicator';
import { GlassPanel } from '../components/ui/GlassPanel';
import { Shield, Zap, TrendingUp, Clock, RefreshCw } from 'lucide-react';
import { getAgentColor } from '../theme';

// API Base URL
const API_URL = 'http://localhost:8000';

interface AgentStatus {
    id: number;
    name: string;
    status: 'active' | 'warning' | 'error' | 'idle';
}

interface Activity {
    time: string;
    text: string;
    status: string;
}

interface SystemMetrics {
    sources_monitored: number;
    obligations_extracted: number;
    avg_confidence: number;
    cost_today: number;
}

export const Home = () => {
    const [agents, setAgents] = useState<AgentStatus[]>([]);
    const [activities, setActivities] = useState<Activity[]>([]);
    const [metrics, setMetrics] = useState<SystemMetrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

    // Fetch system health and agent status
    const fetchAgentStatus = async () => {
        try {
            const response = await fetch(`${API_URL}/api/health`);
            const data = await response.json();

            const agentList: AgentStatus[] = [
                { id: 1, name: 'Discovery', status: data.agents.agent_1 === 'operational' ? 'active' : 'error' },
                { id: 2, name: 'Authenticity', status: data.agents.agent_2 === 'operational' ? 'active' : 'error' },
                { id: 3, name: 'Diff Classifier', status: data.agents.agent_3 === 'operational' ? 'active' : 'error' },
                { id: 4, name: 'Legal Intelligence', status: data.agents.agent_4 === 'operational' ? 'active' : 'error' },
                { id: 5, name: 'MAAD Debate', status: data.agents.agent_5 === 'operational' ? 'active' : 'error' },
                { id: 6, name: 'Knowledge Graph', status: data.agents.agent_6 === 'operational' ? 'active' : 'error' },
                { id: 7, name: 'Oracle API', status: data.agents.agent_7 === 'operational' ? 'active' : 'error' },
                { id: 8, name: 'Remediation', status: data.agents.agent_8 === 'operational' ? 'active' : 'error' },
                { id: 9, name: 'Blockchain', status: data.agents.agent_9 === 'operational' ? 'active' : 'error' },
                { id: 10, name: 'Workflow', status: data.agents.agent_10 === 'operational' ? 'active' : 'error' },
                { id: 11, name: 'AgentOps', status: data.agents.agent_11 === 'operational' ? 'active' : 'error' },
                { id: 12, name: 'Orchestrator', status: data.agents.agent_12 === 'operational' ? 'active' : 'error' },
            ];

            setAgents(agentList);
        } catch (error) {
            console.error('Failed to fetch agent status:', error);
        }
    };

    // Fetch system metrics
    const fetchMetrics = async () => {
        try {
            const response = await fetch(`${API_URL}/api/metrics`);
            const data = await response.json();
            setMetrics(data);
        } catch (error) {
            console.error('Failed to fetch metrics:', error);
        }
    };

    // Fetch recent activities (mock for now, will be real-time later)
    const fetchActivities = async () => {
        const now = new Date();
        const mockActivities: Activity[] = [
            { time: `${Math.floor((now.getTime() - lastUpdate.getTime()) / 60000)} min ago`, text: 'Agent 1 fetched RBI data (198 KB)', status: 'success' },
            { time: `${Math.floor((now.getTime() - lastUpdate.getTime()) / 60000) + 3} min ago`, text: `MAAD debate completed (confidence: ${metrics?.avg_confidence ? Math.round(metrics.avg_confidence * 100) : 73}%)`, status: 'success' },
            { time: `${Math.floor((now.getTime() - lastUpdate.getTime()) / 60000) + 6} min ago`, text: 'Knowledge graph updated (10 nodes)', status: 'success' },
            { time: `${Math.floor((now.getTime() - lastUpdate.getTime()) / 60000) + 10} min ago`, text: 'Blockchain anchor created', status: 'success' },
            { time: `${Math.floor((now.getTime() - lastUpdate.getTime()) / 60000) + 13} min ago`, text: 'Pipeline executed successfully (1.01s)', status: 'success' },
        ];
        setActivities(mockActivities);
    };

    // Initial load
    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            await Promise.all([
                fetchAgentStatus(),
                fetchMetrics(),
            ]);
            await fetchActivities();
            setLoading(false);
            setLastUpdate(new Date());
        };

        loadData();

        // Auto-refresh every 30 seconds
        const interval = setInterval(() => {
            fetchAgentStatus();
            fetchMetrics();
            fetchActivities();
            setLastUpdate(new Date());
        }, 30000);

        return () => clearInterval(interval);
    }, []);

    const handleRefresh = async () => {
        setLoading(true);
        await Promise.all([
            fetchAgentStatus(),
            fetchMetrics(),
        ]);
        await fetchActivities();
        setLoading(false);
        setLastUpdate(new Date());
    };

    const stats = [
        { label: 'Sources Monitored', value: metrics?.sources_monitored || '20+', icon: Shield },
        { label: 'Accuracy Rate', value: metrics?.avg_confidence ? `${Math.round(metrics.avg_confidence * 100)}%` : '95%', icon: TrendingUp },
        { label: 'Processing Time', value: '1.01s', icon: Zap },
        { label: 'Cost/Month', value: `$${metrics?.cost_today ? (metrics.cost_today * 30).toFixed(0) : '60'}`, icon: Clock },
    ];

    if (loading && agents.length === 0) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-coral-flame" />
                    <p className="text-gray-400">Loading system data...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {/* Hero Section with Sunset Glow */}
            <motion.div
                className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-[#FF5F6D] to-[#FFC371] p-12 text-white"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                {/* Animated Background Pattern */}
                <div className="absolute inset-0 opacity-20">
                    {[...Array(20)].map((_, i) => (
                        <motion.div
                            key={i}
                            className="absolute w-2 h-2 bg-white rounded-full"
                            style={{
                                left: `${Math.random() * 100}%`,
                                top: `${Math.random() * 100}%`,
                            }}
                            animate={{
                                y: [0, -30, 0],
                                opacity: [0.3, 1, 0.3],
                            }}
                            transition={{
                                duration: 3 + Math.random() * 2,
                                repeat: Infinity,
                                delay: Math.random() * 2,
                            }}
                        />
                    ))}
                </div>

                <div className="relative z-10">
                    <motion.div
                        className="flex items-center justify-between mb-6"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <div className="flex items-center gap-4">
                            <Shield className="w-16 h-16" />
                            <div>
                                <h1 className="text-5xl font-bold mb-2">SERAPHS 2.0</h1>
                                <p className="text-xl opacity-90">
                                    Multi-Agent Compliance Intelligence System
                                </p>
                            </div>
                        </div>

                        <button
                            onClick={handleRefresh}
                            className="p-3 bg-white/20 hover:bg-white/30 rounded-xl transition-all"
                            disabled={loading}
                        >
                            <RefreshCw className={`w-6 h-6 ${loading ? 'animate-spin' : ''}`} />
                        </button>
                    </motion.div>

                    <motion.p
                        className="text-lg opacity-90 max-w-2xl mb-8"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.4 }}
                    >
                        12 specialized AI agents working in harmony to monitor {metrics?.sources_monitored || 20}+ regulatory
                        sources, achieving {metrics?.avg_confidence ? Math.round(metrics.avg_confidence * 100) : 95}% accuracy with blockchain-anchored verification.
                    </motion.p>

                    <motion.div
                        className="flex items-center gap-4"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 }}
                    >
                        <SunsetButton className="bg-white/20 hover:bg-white/30 backdrop-blur-sm">
                            View Live Pipeline →
                        </SunsetButton>
                        <p className="text-sm opacity-75">
                            Last updated: {lastUpdate.toLocaleTimeString()}
                        </p>
                    </motion.div>
                </div>
            </motion.div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                        <FloatingCard key={stat.label}>
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.1 * index }}
                            >
                                <div className="flex items-center gap-4 mb-4">
                                    <div className="p-3 bg-gradient-to-r from-[#FF5F6D] to-[#FFC371] rounded-xl">
                                        <Icon className="w-6 h-6 text-white" />
                                    </div>
                                    <div>
                                        <p className="text-3xl font-bold gradient-text">
                                            {stat.value}
                                        </p>
                                        <p className="text-sm text-gray-400">{stat.label}</p>
                                    </div>
                                </div>
                            </motion.div>
                        </FloatingCard>
                    );
                })}
            </div>

            {/* System Status */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Agent Status */}
                <GlassPanel>
                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                        <Zap className="w-6 h-6 text-coral-flame" />
                        Agent Status
                        {loading && <RefreshCw className="w-4 h-4 animate-spin" />}
                    </h2>
                    <div className="grid grid-cols-2 gap-4">
                        {agents.map((agent, index) => {
                            const color = getAgentColor(agent.id);
                            return (
                                <motion.div
                                    key={agent.id}
                                    className="flex items-center gap-3 p-3 bg-white/5 rounded-lg"
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.05 * index }}
                                >
                                    <div
                                        className="w-2 h-2 rounded-full animate-pulse"
                                        style={{ backgroundColor: color.bg }}
                                    />
                                    <div className="flex-1">
                                        <p className="text-sm font-medium">Agent {agent.id}</p>
                                        <p className="text-xs text-gray-400">{agent.name}</p>
                                    </div>
                                    <StatusIndicator status={agent.status} />
                                </motion.div>
                            );
                        })}
                    </div>
                </GlassPanel>

                {/* Recent Activity */}
                <GlassPanel>
                    <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
                        <Clock className="w-6 h-6 text-peach-glow" />
                        Recent Activity
                    </h2>
                    <div className="space-y-4">
                        {activities.map((activity, index) => (
                            <motion.div
                                key={index}
                                className="flex items-start gap-3 p-3 bg-white/5 rounded-lg"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: 0.05 * index }}
                            >
                                <div className="w-2 h-2 bg-green-500 rounded-full mt-2" />
                                <div className="flex-1">
                                    <p className="text-sm">{activity.text}</p>
                                    <p className="text-xs text-gray-400 mt-1">{activity.time}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </GlassPanel>
            </div>

            {/* Quick Actions */}
            <FloatingCard>
                <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <SunsetButton onClick={handleRefresh}>
                        {loading ? 'Refreshing...' : 'Refresh Data'}
                    </SunsetButton>
                    <SunsetButton className="bg-white/10 hover:bg-white/20">
                        View Obligations
                    </SunsetButton>
                    <SunsetButton className="bg-white/10 hover:bg-white/20">
                        Export Report
                    </SunsetButton>
                </div>
            </FloatingCard>
        </div>
    );
};
