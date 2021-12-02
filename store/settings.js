const { join } = require("path");
const { parse } = require("toml");
const concat = require("concat-stream");
const { createReadStream } = require("fs");
const { app, ipcMain, ipcRenderer } = require("electron");
const { SETTINGS_PATH } = require("../src/modules/constants/appconfig.js")

// const SETTINGS_PATH = join(app.getAppPath(), "config", "settings.toml");
const readStream = createReadStream(SETTINGS_PATH, "utf-8");
const concatStream = concat(readSettingsBytes);

let SETTINGS;

readStream.on("error", readSettingsError)
readStream.pipe(concatStream)

function readSettingsBytes(settingsBuffer) {
  console.log(`TOML settingsBuffer:`);
  console.log(settingsBuffer);
  SETTINGS = parse(settingsBuffer);
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
    initStoreListener();
  }
}

console.log("----------- ./store/settings.js initialized!!! -----------");

module.exports = SettingStore;
