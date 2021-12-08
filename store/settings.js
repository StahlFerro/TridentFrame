const { join } = require("path");
const { createReadStream } = require("fs");
const { writeFileSync } = require("atomically");
const { app, ipcMain, ipcRenderer } = require("electron");
const { SETTINGS_PATH } = require("../src/common/paths.js")
const concat = require("concat-stream");
const toml = require("@iarna/toml");

let SETTINGS;

function loadSettingsFromFile() {
  const readStream = createReadStream(SETTINGS_PATH, "utf-8");
  const concatStream = concat(readSettings);
  readStream.on("error", readSettingsError)
  readStream.pipe(concatStream)
}


function readSettings(settingsBuffer) {
  console.log(`TOML settingsBuffer:`);
  console.log(settingsBuffer);
  SETTINGS = toml.parse(settingsBuffer);
  console.log(`Parsed settings TOML:`);
  console.log(SETTINGS);
}

function readSettingsError(err){
  console.error(err);
  process.exit(1);
}

function writeSettings(){
  let tomlStr = toml.stringify(SETTINGS);
  writeFileSync(SETTINGS_PATH, tomlStr, {
    tmpPurge: false,
  });
}

const initStoreListener = () => {
	if (!ipcMain || !app) {
		throw new Error(`initStoreListener() must be called from the main process!`);
	}
  ipcMain.on("get-settings", function (event, args) {
    console.log(SETTINGS);
    event.returnValue = SETTINGS;
  });
  ipcMain.on("set-settings", function (event, args) {
    console.log("set-settings invoked with args:");
    console.log(args);
    SETTINGS.user = args;
    console.log("set-settings finished invoked!");
    writeSettings();
    console.log("settings written to toml!");
    event.returnValue = null;
  });
}

class SettingStore {
  static initialize() {
    loadSettingsFromFile();
    initStoreListener();
  }
}

console.log("----------- ./store/settings.js initialized!!! -----------");

module.exports = SettingStore;
