import typescript from "@rollup/plugin-typescript";
// import { nodeResolve } from "@rollup/plugin-node-resolve";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import pluginJson from "@rollup/plugin-json";
import currentPackageJson from "./package.json" assert { type: "json" };
import fs from "fs-extra";

const distDir = "./dist";

/**
 * @type {import('rollup').RollupOptions}
 */
const config = {
  input: "src/handler.ts",
  output: {
    dir: distDir,
    format: "cjs",
  },
  plugins: [pluginJson(), commonjs(), resolve(), typescript()],
  // external: externalRegex,
};

// // copy package.json to lib without workspace dependency
const packageJson = currentPackageJson;
const packageJsonFinal = { ...packageJson };
// packageJsonFinal.dependencies = {
//   ...packageJson.dependencies,
// };
// // // filter workspace dependencies
// // for (const dep in packageJsonFinal.dependencies) {
// //   if (packageJsonFinal.dependencies[dep].startsWith("workspace:")) {
// //     delete packageJsonFinal.dependencies[dep];
// //   }
// // }
// packageJsonFinal.main = "index.js";

// delete lib folder if exists
if (fs.pathExistsSync(distDir)) fs.removeSync(distDir);
// create lib folder
fs.mkdirSync(distDir);

// create package.json in lib folder
fs.writeFileSync(
  `${distDir}/package.json`,
  JSON.stringify(packageJsonFinal, null, 2),
);

// copy .env of db to dist folder
fs.ensureDirSync(`${distDir}/prisma`);
fs.copyFileSync('./prisma/.env', `${distDir}/prisma/.env`);

// copy prisma folder to lib/prisma folder
fs.copySync("./prisma", `${distDir}/prisma`, { overwrite: true });
fs.copySync("./node_modules/prisma/libquery_engine-rhel-openssl-1.0.x.so.node", `${distDir}/prisma/libquery_engine-rhel-openssl-1.0.x.so.node`, { overwrite: true });

export default config;
