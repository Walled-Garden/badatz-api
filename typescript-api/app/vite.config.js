"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var vite_1 = require("vite");
var node_path_1 = __importDefault(require("node:path"));
exports.default = (0, vite_1.defineConfig)({
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
            ".prisma": node_path_1.default.resolve(__dirname, "node_modules", ".prisma"),
        },
    },
});
//# sourceMappingURL=vite.config.js.map