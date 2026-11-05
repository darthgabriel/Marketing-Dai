import { defineConfig } from "vite";

export default defineConfig({
  root: "special-dai/entregables",
  server: {
    port: 5173,
    open: "/special-dai-unificado.html",
  },
  build: {
    outDir: "../../dist",
    emptyOutDir: true,
  },
});
