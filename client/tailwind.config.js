/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        primary: '#042642',
        primaryLight: '#183A56',
        accent: '#d93a00',
        success: '#4faf64',
        warning: '#f4b942',
        error: '#d72638',
        bgDarkBlue: '#111827',
      },
      fontFamily: {
        avenir: ['Avenir', 'Helvetica', 'Arial', 'sans-serif'],
      },
    },
    container: {
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
        '2xl': '6rem',
      },
    },
  },
  plugins: [],
}
