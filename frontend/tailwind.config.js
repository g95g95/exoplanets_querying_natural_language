/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          900: '#0a0a1a',
          800: '#12122a',
          700: '#1a1a3a',
          600: '#2a2a4a',
          500: '#3a3a5a',
        },
        accent: {
          blue: '#4f8fff',
          purple: '#8b5cf6',
          cyan: '#06b6d4',
          orange: '#f97316',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      }
    },
  },
  plugins: [],
}
