import { defineConfig } from 'vite';
export default defineConfig({base:'/static/',build:{outDir:'static',emptyOutDir:false,rollupOptions:{input:'src/main.jsx',output:{entryFileNames:'assets/app.js',assetFileNames:'assets/[name][extname]'}}}});
