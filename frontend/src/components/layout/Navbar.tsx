import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shield, Bell, Settings, User } from 'lucide-react';
import { StatusIndicator } from '../ui/StatusIndicator';

export const Navbar = () => {
    return (
        <motion.nav
            className="fixed top-0 left-0 right-0 z-50 bg-dark-card/80 backdrop-blur-xl border-b border-dark-border"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.3 }}
        >
            <div className="container mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-3 group">
                        <div className="relative">
                            <Shield className="w-8 h-8 text-coral-flame group-hover:scale-110 transition-transform" />
                            <motion.div
                                className="absolute inset-0 bg-sunset-glow opacity-20 blur-xl"
                                animate={{
                                    scale: [1, 1.2, 1],
                                    opacity: [0.2, 0.4, 0.2],
                                }}
                                transition={{ duration: 2, repeat: Infinity }}
                            />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold gradient-text">
                                SERAPHS 2.0
                            </h1>
                            <p className="text-xs text-gray-400">
                                Compliance Intelligence
                            </p>
                        </div>
                    </Link>

                    {/* System Status */}
                    <div className="flex items-center gap-6">
                        <StatusIndicator status="active" label="System Operational" />

                        {/* Actions */}
                        <div className="flex items-center gap-3">
                            <button className="p-2 hover:bg-white/5 rounded-lg transition-colors relative">
                                <Bell className="w-5 h-5" />
                                <span className="absolute top-1 right-1 w-2 h-2 bg-coral-flame rounded-full" />
                            </button>

                            <button className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                                <Settings className="w-5 h-5" />
                            </button>

                            <button className="p-2 hover:bg-white/5 rounded-lg transition-colors">
                                <User className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </motion.nav>
    );
};
