import { defineConfig } from "vite";
import { nodePolyfills } from "vite-plugin-node-polyfills";
import path from "node:path";
import fs from "fs-extra";

export default defineConfig({
  build: {
    target: "node18",
    lib: {
      entry: "src/handler.ts",
      fileName: "handler",
      formats: ["es"],
    },
    minify: false,
  },
  plugins: [nodePolyfills()],
  resolve: {
    alias: {
      // Alias for .prisma folder within node_modules
      // Adjust the path according to your project structure
      ".prisma": path.resolve(__dirname, "node_modules", ".prisma"),
    },
  },
});

try {
  // Specify the source and destination paths for copying
  const sourcePath = "./node_modules/.prisma/client/schema.prisma";
  const destinationPath = "./dist/schema.prisma"; // Change this path based on your output directory

  // Check if the source file exists before copying
  if (fs.pathExistsSync(sourcePath)) {
    // Copy the file to the destination path
    fs.copyFileSync(path.resolve(sourcePath), path.resolve(destinationPath));
    console.log(
      "File copied successfully from " +
        sourcePath +
        " to " +
        destinationPath +
        ".",
    );
  } else {
    console.error("Source file not found.");
  }
} catch (err) {
  console.error("Error copying file:", err);
}
