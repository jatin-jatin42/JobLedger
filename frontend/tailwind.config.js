/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        stage: {
          applied: '#3B82F6',
          screening: '#F59E0B',
          interview: '#8B5CF6',
          offer: '#22C55E',
          rejected: '#EF4444',
          withdrawn: '#6B7280',
        },
      },
    },
  },
  plugins: [],
}
