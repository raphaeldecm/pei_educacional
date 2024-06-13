/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./sistema_pei/**/*.{html,js}"],
  theme: {
    extend: {
      animation: {
        fade: 'fadeOut 5s ease-in-out',
      },
      keyframes: theme => ({
        fadeOut: {
          '0%': { opacity: '1' },
          '100%': { opacity: '0'},
        },
      }),
      fontFamily: {
        poppins: ["Poppins", "sans-serif"]
      }
    },
  },
  plugins: [],
}

