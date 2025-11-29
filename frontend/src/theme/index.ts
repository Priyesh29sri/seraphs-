// Sunset Glow Gradient Colors
export const colors = {
    sunset: {
        coral: '#FF5F6D',
        peach: '#FFC371',
    },
    dark: {
        bg: '#0F0F0F',
        card: '#1A1A1A',
        border: '#2A2A2A',
    },
    status: {
        active: '#22C55E',
        warning: '#EAB308',
        error: '#EF4444',
        info: '#3B82F6',
    },
};

// Animation Variants for Framer Motion
export const animations = {
    // Floating effect
    float: {
        initial: { y: 0 },
        animate: {
            y: [-10, 10, -10],
            transition: {
                duration: 6,
                repeat: Infinity,
                ease: 'easeInOut',
            },
        },
    },

    // Fade in from bottom
    fadeInUp: {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0 },
        exit: { opacity: 0, y: -20 },
        transition: { duration: 0.3 },
    },

    // Scale in
    scaleIn: {
        initial: { opacity: 0, scale: 0.9 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.9 },
        transition: { duration: 0.2 },
    },

    // Slide in from right
    slideInRight: {
        initial: { opacity: 0, x: 50 },
        animate: { opacity: 1, x: 0 },
        exit: { opacity: 0, x: -50 },
        transition: { duration: 0.3 },
    },

    // Stagger children
    staggerContainer: {
        animate: {
            transition: {
                staggerChildren: 0.1,
            },
        },
    },

    // Pulse glow
    pulseGlow: {
        animate: {
            boxShadow: [
                '0 0 20px rgba(255, 95, 109, 0.3)',
                '0 0 40px rgba(255, 195, 113, 0.5)',
                '0 0 20px rgba(255, 95, 109, 0.3)',
            ],
            transition: {
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
            },
        },
    },
};

// Agent Status Colors
export const agentColors = {
    1: { bg: '#3B82F6', glow: 'rgba(59, 130, 246, 0.3)' }, // Blue
    2: { bg: '#10B981', glow: 'rgba(16, 185, 129, 0.3)' }, // Green
    3: { bg: '#F59E0B', glow: 'rgba(245, 158, 11, 0.3)' }, // Amber
    4: { bg: '#8B5CF6', glow: 'rgba(139, 92, 246, 0.3)' }, // Purple
    5: { bg: '#EF4444', glow: 'rgba(239, 68, 68, 0.3)' }, // Red (MAAD)
    6: { bg: '#06B6D4', glow: 'rgba(6, 182, 212, 0.3)' }, // Cyan
    7: { bg: '#EC4899', glow: 'rgba(236, 72, 153, 0.3)' }, // Pink
    8: { bg: '#14B8A6', glow: 'rgba(20, 184, 166, 0.3)' }, // Teal
    9: { bg: '#F97316', glow: 'rgba(249, 115, 22, 0.3)' }, // Orange
    10: { bg: '#6366F1', glow: 'rgba(99, 102, 241, 0.3)' }, // Indigo
    11: { bg: '#A855F7', glow: 'rgba(168, 85, 247, 0.3)' }, // Violet
    12: { bg: '#FF5F6D', glow: 'rgba(255, 95, 109, 0.3)' }, // Coral (Orchestrator)
};

// Utility function to get agent color
export const getAgentColor = (agentId: number) => {
    return agentColors[agentId as keyof typeof agentColors] || agentColors[1];
};
