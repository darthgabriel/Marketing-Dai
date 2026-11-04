import { defineConfig } from "vite";

export default defineConfig({
  root: "entregables",
  server: {
    port: 5173,
    open: "/special-dai-unificado.html",
  },
  build: {
    outDir: "../dist",
    emptyOutDir: true,
  },
});
