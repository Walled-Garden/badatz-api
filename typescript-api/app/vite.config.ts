import { defineConfig } from "vite";
import { nodePolyfills } from "vite-plugin-node-polyfills";
import path from "node:path";

export default defineConfig({
  build: {
    target: "node18",
    lib: {
      entry: "src/handler.ts",
      fileName: "handler",
      formats: ["cjs"],
    },
    minify: false,
  },
  // plugins: [nodePolyfills()],
  resolve: {
    alias: {
      // Alias for .prisma folder within node_modules
      // Adjust the path according to your project structure
      ".prisma": path.resolve(__dirname, "node_modules", ".prisma"),
    },
  },
});
