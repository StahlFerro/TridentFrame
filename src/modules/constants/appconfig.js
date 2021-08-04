import { ipcRenderer, app } from "electron";
import { env, cwd, platform } from "process";
import { resolve, join } from "path";
import { readFileSync } from 'fs';

const appPath = ipcRenderer.sendSync("get-app-path");

let python_path;
let engine_dir;
let engine_exec_path;

let previews_path;
let temp_path;

let settings_path;
let settings;


// console.log(appPath);
// console.log(`current appPath: ${appPath}`);
// console.log(`current dirname -> ${__dirname}`);
// console.log(`current process.cwd() -> ${cwd()}`);
// console.log(`current dot -> ${resolve(".")}`);

if (env.DEPLOY_ENV == "DEV") {
  engine_exec_path = "main.py"
  settings_path = join(appPath, "config", "settings.json");
  settings = JSON.parse(readFileSync(settings_path));
  temp_path = join(appPath, "temp");
  previews_path = join(temp_path, "previews");
} else {
  if (platform == "win32") {
    python_path = "python.exe";

    engine_dir = join(appPath, "engine", "windows");
    engine_exec_path = join(engine_dir, "tridentengine.exe");
  } else if (platform == "linux") {
    python_path = "python3.7";

    engine_dir = join(appPath, "engine", "linux");
    engine_exec_path = join(engine_dir, "tridentengine");
  }
  settings_path = join(engine_dir, "config", "settings.json");
  settings = JSON.parse(readFileSync(settings_path));
  temp_path = join(engine_dir, "temp");
  previews_path = join(temp_path, "previews");
}

console.log(settings);

export const SETTINGS = settings;
export const PREVIEWS_PATH = previews_path;
export const TEMP_PATH = temp_path;
export const ENGINE_DIR = engine_dir;
export const ENGINE_EXEC_PATH = engine_exec_path;
export const PYTHON_PATH = python_path;
