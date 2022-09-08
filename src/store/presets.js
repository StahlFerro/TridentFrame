
const { APP_SETTINGS_PATH, PRESETS_DIR } = require("../common/paths.js");
const { readdirSync } = require("fs");
const { CriterionPresetCollection } = require("../models/criterionPresets.js");
let PRESETS_COLLECTION;

/**
 * Utility class for bootstrapping the app settings functionalities
 */
 class PresetsStore {
  static initialize() {
    loadAllPresets();
    initStoreListener();
    return PRESETS_COLLECTION;
  }
}


/**
 * Read all json preset files and parse it as list of objects
 */
 function loadAllPresets() {
  let collection = CriterionPresetCollection.loadFromDirectory(PRESETS_DIR);
  
}