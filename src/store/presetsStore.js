
const { APP_SETTINGS_PATH, PRESETS_PATH } = require("../common/paths.js");
const { dirname } = require("path");
const { existsSync, readFileSync, writeFileSync, mkdirSync, mkdir } = require("fs");
const { PresetCollection, Preset, PresetType } = require("../models/presets.js");
const { app, ipcMain, ipcRenderer } = require("electron");
const { StoreOperation } = require("../models/storeOperation.js");

let PRESETS_COLLECTION = new PresetCollection();


function createPresetsFIle(path) {
  mkdirSync(dirname(path), { recursive: true }, (err) => {
    if (err) throw err;
  });
  let presetCollection = new PresetCollection();
  let presetCollStr = JSON.stringify(presetCollection);
  // let tomlStr = toml.stringify(_DEFAULT_SETTINGS);
  writeFileSync(path, presetCollStr, {
    tmpPurge: false,
  });
}


/**
 * Serializes the PRESETS_COLLECTION object and writes it to the file
 */
 function writePresetsToFile(){
  console.debug("writeSettings called")
  let presetsCollStr = JSON.stringify(PRESETS_COLLECTION, null, 2);
  writeFileSync(PRESETS_PATH, presetsCollStr, {
    tmpPurge: false,
  });
}


/**
 * Read all json preset files and parse it as list of objects
 */
 function loadPresetsFromFile() {
  console.debug("Start loading preset collection from presets folder...");
  try {
    // If app.toml file doesn't exist
    if (!existsSync(PRESETS_PATH)) {
      console.warn("WARNING: presets directory file doesn't exist, creating")
      createPresetsFIle(PRESETS_PATH);
    }
    const fileContent = readFileSync(PRESETS_PATH, { encoding: "utf-8"});
    const presetCollJson = JSON.parse(fileContent);
    const presetColl = PresetCollection.fromJSON(presetCollJson);
    PRESETS_COLLECTION = presetColl;
  } catch(err) {
    console.error(err)
  }
}

/**
 * 
 * @param {PresetType} presetType Type of preset to match for from the preset collections
 * @returns {[Preset]} List of presets that matches the presetType
 */
function getPresetsByCriteriaType(presetType) {
  let presets = PRESETS_COLLECTION.presets.filter(p => p.presetType.name == presetType.name);
  return presets;
}


/**
 * Add new preset to the collection in the main process
 * @param {Preset} newPreset The new preset to be added
 */
function addPresetToCollection(newPreset) {
  PRESETS_COLLECTION.presets[newPreset.id] = newPreset;
}


function updatePresetOnCollection(updatedPreset) {
  // let presetIndex = PRESETS_COLLECTION.presets.(p => p.id = newPreset.id);
  if (updatedPreset.id in PRESETS_COLLECTION.presets){
    PRESETS_COLLECTION.presets[updatedPreset.id] = updatedPreset;
    return true;
  }
  else return false;
}


function deletePresetFromCollection(id) {
  delete PRESETS_COLLECTION.presets[id];
  // let presetIndex = PRESETS_COLLECTION.presets.findIndex(p => p.id = newPreset.id);
  // PRESETS_COLLECTION.presets.splice(presetIndex, 1);
}

function ipcGetPresets() {

}


const initStoreListener = () => {
  console.debug("Start attaching store IPC listeners...");
	if (!ipcMain || !app) {
		throw new Error(`initStoreListener() must be called from the main process!`);
	}
  ipcMain.on("IPC-GET-PRESETS", function (event, args) {
    console.debug(PRESETS_COLLECTION);
    event.returnValue = PRESETS_COLLECTION;
  });
  ipcMain.handle("IPC-GET-PRESETS", async (event, args) => {
    return PRESETS_COLLECTION;
  });
  ipcMain.on("IPC-GET-PRESETS-CRITERION", function (event, criteriaType) {
    console.debug("IPC-GET-PRESETS-CRITERION invoked with args:");
    getPresetsByCriteriaType(criteriaType);
    console.debug(args);
  });
  ipcMain.on("IPC-SET-PRESETS", function (event, storeOp, args) {
    console.debug("IPC-SET-PRESETS invoked with args:");
    console.debug(args);
    if (storeOp.name == StoreOperation.Add.name) {
      addPresetToCollection(args);
    }
    else if (storeOp.name == StoreOperation.Update.name) {
      updatePresetOnCollection(args);
    }
    else if (storeOp.name == StoreOperation.Delete.name) {
      deletePresetFromCollection(args);
    }
    else{
      throw new Error(`Unknown StoreOperation ${storeOp}`);
    }
    console.debug("IPC-SET-PRESETS finished invoked!");
    writePresetsToFile();
    console.debug("presets written to json!");
    event.returnValue = null;
  });
  console.debug("Finished attaching store IPC listeners");
}

/**
 * Utility class for bootstrapping the app presets functionalities
 */
 class PresetsStore {
  static initialize() {
    loadPresetsFromFile();
    initStoreListener();
    return PRESETS_COLLECTION;
  }
}


console.debug("----------- ./store/presetsStore.js initialized!!! -----------");

module.exports = PresetsStore;
