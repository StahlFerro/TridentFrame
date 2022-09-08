"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.TEMP_PATH = exports.APP_SETTINGS_PATH = exports.PYTHON_PATH = exports.PREVIEWS_PATH = exports.ENGINE_EXEC_PATH = exports.PRESETS_DIR = exports.ENGINE_DIR = void 0;

var { ipcMain, ipcRenderer, app } = require("electron");

var _process = require("process");

var { join } = require("path");

var { readFileSync } = require("fs");

let appPath;

if (ipcMain != null && app != null)
  appPath = app.getAppPath();
else if (ipcRenderer)
  appPath = ipcRenderer.sendSync("get-app-path-sync");
else
  throw new Error("Cannot get appPath for common/paths.js");

let python_path;
let engine_dir;
let engine_exec_path;
let previews_path;
let temp_path;
let app_settings_path;
let criterion_presets_dir;
let settings;

if (_process.env.DEPLOY_ENV == "DEV") {
  engine_exec_path = "main.py";
  app_settings_path = join(appPath, "config", "app.toml");
  criterion_presets_dir = join(appPath, "presets");
  temp_path = join(appPath, "temp");
  previews_path = join(temp_path, "previews");
} else {
  if (_process.platform == "win32") {
    python_path = "python.exe";
    engine_dir = join(appPath, "engine", "windows");
    engine_exec_path = join(engine_dir, "tridentengine.exe");
  } else if (_process.platform == "linux") {
    python_path = "python3.7";
    engine_dir = join(appPath, "engine", "linux");
    engine_exec_path = join(engine_dir, "tridentengine");
  }
  app_settings_path = join(appPath, "config", "app.toml");
  criterion_presets_dir = join(appPath, "presets");
  temp_path = join(engine_dir, "temp");
  previews_path = join(temp_path, "previews");
}

console.log(settings);
const APP_SETTINGS_PATH = app_settings_path;
exports.APP_SETTINGS_PATH = APP_SETTINGS_PATH;
const PREVIEWS_PATH = previews_path;
exports.PREVIEWS_PATH = PREVIEWS_PATH;
const TEMP_PATH = temp_path;
exports.TEMP_PATH = TEMP_PATH;
const PRESETS_DIR = criterion_presets_dir;
exports.PRESETS_DIR = PRESETS_DIR;
const ENGINE_DIR = engine_dir;
exports.ENGINE_DIR = ENGINE_DIR;
const ENGINE_EXEC_PATH = engine_exec_path;
exports.ENGINE_EXEC_PATH = ENGINE_EXEC_PATH;
const PYTHON_PATH = python_path;
exports.PYTHON_PATH = PYTHON_PATH;