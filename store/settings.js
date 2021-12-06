const { join } = require("path");
const { createReadStream, createWriteStream } = require("fs");
const { app, ipcMain, ipcRenderer } = require("electron");
const { SETTINGS_PATH } = require("../src/modules/constants/appconfig.js")
const concat = require("concat-stream");
const toml = require("toml");

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

const initStoreListener = () => {
	if (!ipcMain || !app) {
		throw new Error(`initStoreListener() must be called from the main process!`);
	}
  ipcMain.on("get-settings", function (event, args) {
    event.returnValue = SETTINGS;
  });
  ipcMain.on("set-settings", function (event, args) {
    console.log("set-settings invoked!");
    SETTINGS.user.theme = args;
    console.log("set-settings finished invoked!");
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
