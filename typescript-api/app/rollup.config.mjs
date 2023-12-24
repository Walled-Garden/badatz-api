import typescript from "@rollup/plugin-typescript";
// import { nodeResolve } from "@rollup/plugin-node-resolve";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import pluginJson from "@rollup/plugin-json";
// import autoExternal from "rollup-plugin-auto-external";
import currentPackageJson from "./package.json" assert { type: "json" };
import fs from "fs-extra";

const distDir = "./dist";

let currentDependencies = Object.keys(currentPackageJson.dependencies);
// remove 100match-backend
const external = [...currentDependencies];

// include any subdirectories of each dependency, e.g. firebase-admin/app
// const externalRegex = external.map((dep) => new RegExp(`^${dep}(/.+)?$`));

// console.log("external", externalRegex);

// import typescript from "rollup-plugin-typescript2";
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

// copy package.json to lib without workspace dependency
import { log } from "console";
import path from "path";
const packageJson = currentPackageJson;
const packageJsonFinal = { ...packageJson };
packageJsonFinal.dependencies = {
  ...packageJson.dependencies,
};
// // filter workspace dependencies
// for (const dep in packageJsonFinal.dependencies) {
//   if (packageJsonFinal.dependencies[dep].startsWith("workspace:")) {
//     delete packageJsonFinal.dependencies[dep];
//   }
// }

packageJsonFinal.main = "index.js";

// delete lib folder if exists
if (fs.pathExistsSync(distDir)) fs.removeSync(distDir);
// create lib folder
fs.mkdirSync(distDir);

// // clear lib folder
// fs.readdirSync("./lib").forEach((file) => {
//   fs.unlinkSync(path.join("./lib", file));
// });

// create package.json in lib folder
fs.writeFileSync(
  `${distDir}/package.json`,
  JSON.stringify(packageJsonFinal, null, 2),
);

// copy .env of db to lib
// const RUN_ENV = process.env.RUN_ENV;
// const envName = `.env.${RUN_ENV}`;
// const envFilePath = path.resolve(`../env/${envName}`);
// console.log("loading env file: ", envFilePath);
// fs.copyFileSync(envFilePath, `./lib/${envName}`);
// fs.copyFileSync(envFilePath, `./lib/.env`);

// copy prisma folder to lib/prisma folder
fs.copySync("./prisma", `${distDir}/prisma`, { overwrite: true });
fs.copySync("./node_modules/prisma/libquery_engine-rhel-openssl-1.0.x.so.node", `${distDir}/prisma/libquery_engine-rhel-openssl-1.0.x.so.node`, { overwrite: true });

// create lib/prisma folder if not exists
// copy prisma folder to lib/prisma folder
// if (!fs.existsSync("./lib/prisma")) fs.mkdirSync("./lib/prisma");
// fs.readdirSync("../prisma").forEach((file) => {
//   fs.copyFileSync(path.join("../prisma", file), `./lib/prisma/${file}`);
// });

export default config;
