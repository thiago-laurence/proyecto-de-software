/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/web/templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

/*
  Start the Tailwind CLI build process.
  Run the CLI tool to scan your template files for classes and build your CSS.
  --> npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css --watch
*/