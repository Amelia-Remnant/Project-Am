/** @type {import('tailwindcss').Config} */
module.exports = {
  
  //Looks for any html file in templates to compile
  content: ["./templates/*.html"],
  theme: {
    
    //setting breakpoints
    screens: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },

    extend: {
      
      //Adding custom colours
      colors: {
        cherry: '#CD0F56',
        iris: '#5D3fD3',
        lilac: '#CF9FFF',
        lightGrey: '#978C90',
        lightRed: '#F98C9C',
        gold: '#FFD700',
        silver: '#C0C0C0',
        bronze: '#CD7F32'
      }

    },
  },
  plugins: [],
}
