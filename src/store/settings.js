const { join } = require("path");
const { createReadStream, readFileSync } = require("fs");
const { writeFileSync } = require("atomically");
const { app, ipcMain, ipcRenderer } = require("electron");
const { APP_SETTINGS_PATH } = require("../common/paths.js")
const concat = require("concat-stream");
const toml = require("@iarna/toml");

let SETTINGS;
const SETTINGS_PATH = APP_SETTINGS_PATH;

/**
 * Read the TOML settings file and parse it as an object
 */
function loadSettingsFromFile() {
  console.debug("Start loading data from settings file...");
  const tomlStr = readFileSync(SETTINGS_PATH, { encoding: "utf-8"});
  SETTINGS = toml.parse(tomlStr);
  console.debug("Finished reading and parsing TOML...");
}

// function loadSettingsFromFileStream() {
//   console.log("Start loading data from settings file...");
//   const readStream = createReadStream(SETTINGS_PATH, "utf-8");
//   const concatStream = concat(readSettings);
//   readStream.on("error", readSettingsError)
//   readStream.pipe(concatStream)
//   console.log("Piping data from settings file...");
// }

// function readSettings(settingsBuffer) {
//   console.log("Reading TOML settings buffer...");
//   console.log(settingsBuffer);
//   SETTINGS = toml.parse(settingsBuffer);
//   console.log(SETTINGS);
//   console.log(`Finished reading and parsing settings TOML`);
// }

// function readSettingsError(err){
//   console.error(err);
//   process.exit(1);
// }

/**
 * Serializes the TOML object and writes it to the file
 */
function writeSettings(){
  let tomlStr = toml.stringify(SETTINGS);
  writeFileSync(SETTINGS_PATH, tomlStr, {
    tmpPurge: false,
  });
}

/**
 * Initializes IPC listeners for manipulating the app settings from renderer processes
 */
const initStoreListener = () => {
  console.debug("Start attaching store IPC listeners...");
	if (!ipcMain || !app) {
		throw new Error(`initStoreListener() must be called from the main process!`);
	}
  ipcMain.on("get-settings", function (event, args) {
    console.debug(SETTINGS);
    event.returnValue = SETTINGS;
  });
  ipcMain.on("set-user-settings", function (event, args) {
    console.debug("set-user-settings invoked with args:");
    console.debug(args);
    SETTINGS.user = args;
    console.debug("set-user-settings finished invoked!");
    writeSettings();
    console.debug("settings written to toml!");
    event.returnValue = null;
  });
  console.debug("Finished attaching store IPC listeners");
}

/**
 * Utility class for bootstrapping the app settings functionalities
 */
class SettingStore {
  static initialize() {
    loadSettingsFromFile();
    initStoreListener();
    return SETTINGS;
  }
}

console.debug("----------- ./store/settings.js initialized!!! -----------");

module.exports = SettingStore;
