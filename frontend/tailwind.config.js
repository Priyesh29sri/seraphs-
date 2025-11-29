/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Sunset Glow Gradient
        coral: {
          flame: '#FF5F6D',
          DEFAULT: '#FF5F6D',
        },
        peach: {
          glow: '#FFC371',
          DEFAULT: '#FFC371',
        },
        // Dark Neo-Banking Theme
        dark: {
          bg: '#0F0F0F',
          card: '#1A1A1A',
          border: '#2A2A2A',
        },
      },
      backgroundImage: {
        'sunset-glow': 'linear-gradient(to bottom right, #FF5F6D, #FFC371)',
        'dark-gradient': 'linear-gradient(to bottom, #0F0F0F, #1A1A1A)',
      },
      boxShadow: {
        'float': '0 10px 40px rgba(0, 0, 0, 0.3)',
        'float-lg': '0 20px 60px rgba(0, 0, 0, 0.4)',
        'glow': '0 0 20px rgba(255, 95, 109, 0.3)',
        'glow-peach': '0 0 20px rgba(255, 195, 113, 0.3)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient': 'gradient 8s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
    },
  },
  plugins: [],
}
