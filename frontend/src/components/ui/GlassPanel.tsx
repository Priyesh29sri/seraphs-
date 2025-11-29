import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { animations } from '../../theme';

interface GlassPanelProps {
    children: ReactNode;
    className?: string;
    animate?: boolean;
}

export const GlassPanel = ({
    children,
    className = '',
    animate = true
}: GlassPanelProps) => {
    return (
        <motion.div
            className={`glass-panel p-6 ${className}`}
            {...(animate ? animations.scaleIn : {})}
        >
            {children}
        </motion.div>
    );
};
