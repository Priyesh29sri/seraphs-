import { motion } from 'framer-motion';

interface StatusIndicatorProps {
    status: 'active' | 'warning' | 'error' | 'idle';
    label?: string;
    showPulse?: boolean;
}

export const StatusIndicator = ({
    status,
    label,
    showPulse = true
}: StatusIndicatorProps) => {
    const statusClasses = {
        active: 'status-active',
        warning: 'status-warning',
        error: 'status-error',
        idle: 'bg-gray-500',
    };

    return (
        <div className="flex items-center gap-2">
            <motion.div
                className={`status-dot ${statusClasses[status]} ${showPulse ? '' : 'animate-none'}`}
                animate={showPulse ? {
                    scale: [1, 1.2, 1],
                    transition: { duration: 2, repeat: Infinity }
                } : {}}
            />
            {label && (
                <span className="text-sm font-medium text-gray-300">
                    {label}
                </span>
            )}
        </div>
    );
};
