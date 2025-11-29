import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface SunsetButtonProps {
    children: ReactNode;
    onClick?: () => void;
    className?: string;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
}

export const SunsetButton = ({
    children,
    onClick,
    className = '',
    disabled = false,
    type = 'button'
}: SunsetButtonProps) => {
    return (
        <motion.button
            type={type}
            className={`sunset-button ${className} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
            onClick={onClick}
            disabled={disabled}
            whileHover={!disabled ? { scale: 1.05 } : {}}
            whileTap={!disabled ? { scale: 0.95 } : {}}
        >
            {children}
        </motion.button>
    );
};
