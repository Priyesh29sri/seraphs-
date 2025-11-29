import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { animations } from '../../theme';

interface FloatingCardProps {
    children: ReactNode;
    className?: string;
    onClick?: () => void;
    animate?: boolean;
}

export const FloatingCard = ({
    children,
    className = '',
    onClick,
    animate = true
}: FloatingCardProps) => {
    return (
        <motion.div
            className={`floating-card ${className}`}
            onClick={onClick}
            {...(animate ? animations.fadeInUp : {})}
            whileHover={{ y: -5, transition: { duration: 0.2 } }}
        >
            {children}
        </motion.div>
    );
};
