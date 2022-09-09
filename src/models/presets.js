const { v5: uuidV5 } = require('uuid');


class PresetType {
  static CreationCriteria = new PresetType(
    "creation_criteria", "Creation criteria")
  static ModificationCriteria = new PresetType(
    "modification_criteria", "Modification criteria")
  constructor(name, label) {
    this.name = name;
    this.label = label;
  }
  static getAll() {
    return Object.keys(this).map(k => this[k]);
  }
  static fromName(name) {
    return this.getAll().filter(pt => pt.name === name)[0];
  }
}


class PresetCollection {
  /**
   * 
   * @param {[Preset]} presets List of presets
   */
  constructor(presets){
    this.presets = presets? presets : [];
  }

  static fromJson(json) {
    let presetCollection = new PresetCollection();
    Object.assign(presetCollection, json);
    return presetCollection;
  }
}


class Preset {
  constructor() {
    this.id = uuidV5();
    this.createdDateTime = Date.now();
    this.presetType = null;
    this.presetObject = null;
  }
  // static createfromJson(json){
  //   let preset = new Preset();
  //   Object.assign(preset, json);
  //   return preset;
  // }
}


module.exports.PresetCollection = PresetCollection;
module.exports.Preset = Preset;
module.exports.PresetType = PresetType;
