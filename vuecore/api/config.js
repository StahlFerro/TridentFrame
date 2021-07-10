const { ipcRenderer, app } = require("electron");
const { env, cwd, platform } = require("process");
const { resolve, join } = require("path");
const { readFileSync } = require('fs');

let appPath;
let python_path;
let engine_dir;
let engine_exec_path;

let previews_path;
let temp_path;

let settings_path;
let settings;

appPath = ipcRenderer.sendSync("get-app-path");
console.log(appPath);
console.log(`current appPath: ${appPath}`);
console.log(`current dirname -> ${__dirname}`);
console.log(`current process.cwd() -> ${cwd()}`);
console.log(`current dot -> ${resolve(".")}`);

if (env.DEPLOY_ENV == "DEV") {
  engine_exec_path = "main.py"
  settings_path = join(appPath, "config", "settings.json");
  settings = JSON.parse(readFileSync(settings_path));
  previews_path = join(appPath, "previews");
  temp_path = join(appPath, "temp");
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
  previews_path = join(engine_dir, "previews");
  temp_path = join(engine_dir, "temp");
}

console.log(settings);

module.exports = {
  SETTINGS: settings,
  PREVIEWS_PATH: previews_path,
  TEMP_PATH: temp_path,
  ENGINE_DIR: engine_dir,
  ENGINE_EXEC_PATH: engine_exec_path,
  PYTHON_PATH: python_path,
}
