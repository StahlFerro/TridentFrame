// const { join } = require("path");
const { createReadStream, readFileSync, existsSync } = require("fs");
const { writeFileSync } = require("atomically");
const { app, ipcMain, ipcRenderer } = require("electron");
const { APP_SETTINGS_PATH } = require("../common/paths.js")
// const concat = require("concat-stream");
const toml = require("@iarna/toml");

const _DEFAULT_SETTINGS = {
  "statistics": { "last_backup": "" },
  "startup": {
      "fullscreen": false,
      "open_debugger": false,
      "open_devtools": false
  },
  "locale": {
    "lang": "en"
  },
  "preview_image": {
      "name_save_behaviour": "auto_generated"
  },
  "directories": {
      "default_out_dir": {
          "create_panel": "",
          "split_panel": "",
          "modify_panel": ""
      }
  },
  "inspect_panel": {
      "image_attributes": [
          {
              "category": "general_info",
              "label": "General Info",
              "attributes": [
                  "name",
                  "width",
                  "height",
                  "format",
                  "fsize_hr",
                  "absolute_url",
                  "creation_datetime",
                  "modification_datetime",
                  "comments",
                  "has_transparency",
                  "color_mode",
                  "color_profile",
                  "bit_depth",
                  "exif",
                  "is_animated"
              ]
          },
          {
              "category": "animation_info",
              "label": "Animation Info",
              "attributes": [
                  "frame_count",
                  "average_delay",
                  "delays_are_even",
                  "delays",
                  "fps",
                  "loop_duration",
                  "loop_count"
              ]
          }
      ]
  }
};

let SETTINGS;
// const SETTINGS_PATH = APP_SETTINGS_PATH;

/**
 * Read the TOML settings file and parse it as an object
 */
function loadSettingsFromFile() {
  console.debug("Start loading data from settings file...");
  try {
    // If app.toml file doesn't exist
    if (!existsSync(APP_SETTINGS_PATH)) {
      console.warn("WARNING: app.toml settings file doesn't exist, creating")
      createSettingsFile();
    }
  } catch(err) {
    console.error(err)
  }
  const tomlStr = readFileSync(APP_SETTINGS_PATH, { encoding: "utf-8"});
  SETTINGS = toml.parse(tomlStr);
  console.debug("Finished reading and parsing TOML...");
}

/**
 * In the event that the settings file (app.toml) is missing, create the file with default settings
 */
function createSettingsFile() {
  let tomlStr = toml.stringify(_DEFAULT_SETTINGS);
  writeFileSync(APP_SETTINGS_PATH, tomlStr, {
    tmpPurge: false,
  });
}

/**
 * Update main SETTINGS based on
 * @param {Any} newSettings 
 */
function updateSettings(newSettings) {
  SETTINGS = { ...newSettings };
}

/**
 * Serializes the TOML object and writes it to the file
 */
function writeSettings(){
  console.debug("writeSettings called")
  let tomlStr = toml.stringify(SETTINGS);
  writeFileSync(APP_SETTINGS_PATH, tomlStr, {
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
  ipcMain.on("IPC-GET-SETTINGS", function (event, args) {
    console.debug(SETTINGS);
    event.returnValue = SETTINGS;
  });
  ipcMain.on("IPC-SET-SETTINGS", function (event, args) {
    console.debug("IPC-SET-SETTINGS invoked with args:");
    console.debug(args);
    updateSettings(args);
    console.debug("IPC-SET-SETTINGS finished invoked!");
    writeSettings();
    console.debug("settings written to toml!");
    event.returnValue = null;
  });
  console.debug("Finished attaching store IPC listeners");
}

/**
 * Utility class for bootstrapping the app settings functionalities
 */
class SettingsStore {
  static initialize() {
    loadSettingsFromFile();
    initStoreListener();
    return SETTINGS;
  }
}

console.debug("----------- ./store/settingsStore.js initialized!!! -----------");

module.exports = SettingsStore;
