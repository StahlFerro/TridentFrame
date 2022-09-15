const { v4: uuidV4 } = require('uuid');



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
    this.id = uuidV4();
    this.createdDateTime = Date.now();
    this.name = "";
    this.presetType = null;
    this.presetObject = null;
  }
  static createFromCriteria(criteriaType, presetName, criteria) {
    let preset = new Preset();
    preset.name = presetName;
    if (criteriaType == "CreationCriteria")
      preset.presetType = PresetType.CreationCriteria;
    else if (criteriaType == "ModificationCriteria")
      preset.presetType = PresetType.ModificationCriteria;
    let criteriaJson = JSON.parse(JSON.stringify(criteria));
    preset.presetObject = criteriaJson;
    return preset;
  }
  // static createfromJson(json){
  //   let preset = new Preset();
  //   Object.assign(preset, json);
  //   return preset;
  // }
}

class PresetDraft {
  constructor(draftAttributes) {
    this.draftAttributes = draftAttributes
  }
  static fromPresetObject(presetObject, defaultInclude=false){
    let draftAttributes = [];
    for (const[k, v] of Object.entries(presetObject)){
      const pdAttr = new PresetDraftAttribute(k, v, defaultInclude);
      draftAttributes.push(pdAttr);
    }
    return new PresetDraft(draftAttributes);
  }
}

class PresetDraftAttribute{
  constructor(key, value, include){
    this.pKey = key;
    this.pValue = value;
    this.include = include;
  }
}


module.exports.PresetCollection = PresetCollection;
module.exports.Preset = Preset;
module.exports.PresetType = PresetType;
module.exports.PresetDraft = PresetDraft;
