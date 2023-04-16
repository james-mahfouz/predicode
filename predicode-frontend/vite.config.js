import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import replace from '@rollup/plugin-replace';
import dotenv from 'dotenv';

dotenv.config(); // load environment variables from .env file

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    replace({
      'process.env.API_URL': JSON.stringify(process.env.API_URL),
      preventAssignment: true,
    }),
  ],
})
