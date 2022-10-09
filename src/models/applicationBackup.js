const { PresetCollection } = require("./presets");

class ApplicationBackup {
  /**
   * @param {string} appVersion Application version string
   * @param {object} settings Settings object
   * @param {PresetCollection} presetsCollection PresetCollection Object
   */
  constructor(appVersion, settings, presetsCollection) {
    this.createdDateTime = Date.now();
    this.appVersion = appVersion;
    this.settings = settings;
    this.presetsCollection = presetsCollection
  }
}

module.exports.ApplicationBackup = ApplicationBackup;
