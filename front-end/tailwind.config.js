/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        main_primary: "#1B73E8",
        main_secondary: "#1B73E8",
        light_primary: "#F3F4F6",
        dark_primary: "#323639",
        dark_secondary: "#525659",
        light_secondary: "#E5E7EB",
        darkHoverColor: "#525659",
        lightHoverColor: "#F3F4F6",
      },
      boxShadow: {
        white:
          "0 1px 1px 0 rgba(255, 255, 255, 0.1), 0 1px 2px 0 rgba(255, 255, 255, 0.06)",
      },
      extend: {
        zIndex: {
          60: "60",
          70: "70",
          80: "80",
          90: "90",
          100: "100",
        },
      },
    },
  },
};
