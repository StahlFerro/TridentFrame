const { v4: uuidV4 } = require('uuid');
const { VueI18n } = require('vue-i18n');
// const { globalTranslate } = require('../locales/i18n.js');



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

/**
 * Root object to contain all presets
 */
class PresetCollection {
  /**
   * Represents the entire collection of presets
   * @param {Object} presets Dictionary of presets, with key as each preset id and value being the preset.
   */
  constructor(presets){
    this.presets = presets? presets : {};
  }
  static fromJson(json) {
    let presetCollection = new PresetCollection();
    Object.assign(presetCollection, json);
    return presetCollection;
  }
}


/**
 * Object that stores preselected attributes to apply to UI forms
 */
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
  
  /**
   * Create from PresetDraft object
   * @param {string} name Name of the preset
   * @param {PresetType} presetType Type of the preset
   * @param {PresetDraft} draft PresetDraft object to be converted into Preset
   */
  static createFromDraft(name, presetType, draft) {
    let preset = new Preset();
    preset.name = name;
    preset.presetType = presetType;
    const obj = draft.draftAttributes.filter(attr => attr.include).reduce((aggr, attr) => (aggr[attr.pKey] = attr.pValue, aggr) ,{});
    preset.presetObject = obj;
    return preset;
  }
  // static createfromJson(json){
  //   let preset = new Preset();
  //   Object.assign(preset, json);
  //   return preset;
  // }
}

/**
 * Draft object for presets for users to evaluate before creating the actual Preset object.
 */
class PresetDraft {
  /**
   * Create new PresetDraft object with attribute list
   * @param {PresetType} presetType
   * @param {PresetDraftAttribute[]} draftAttributes 
   */
  constructor(presetType, draftAttributes) {
    this.presetType = presetType;
    this.draftAttributes = draftAttributes;
  }
  
  /**
   * Create preset draft from preset object
   * @param {PresetType} presetType Type of preset
   * @param {object} presetObject POJO object
   * @param {Boolean} defaultInclude Set include property of all attributes
   * @returns 
   */
  static createFromAttributesObject(presetType, presetObject, defaultInclude=false){
    let draftAttributes = [];
    for (const[k, v] of Object.entries(presetObject)){
      const pdAttr = new PresetDraftAttribute(k, v, defaultInclude);
      draftAttributes.push(pdAttr);
    }
    return new PresetDraft(presetType, draftAttributes);
  }

  /**
   * Create PresetDraft object for the purpose of updating an existing Preset object
   * @param {Preset} currentPreset Current Preset info to create draft attributes from
   * @param {object} attributesObj POJO object of new attributes
   */
  static buildUpdatePresetDraft(currentPreset, attributesObj) {
    console.log(currentPreset.presetObject);
    let draft = PresetDraft.createFromAttributesObject(currentPreset.presetType, currentPreset.presetObject, true);
    console.log(draft.draftAttributes);
    draft.populateUpdateAttributes(attributesObj);
    return draft;
  }

  /**
   * Populate attributes needed for the Preset to be updated by the user
   * newAttributeJson will always include the full set of attributes 
   * @param {object} attributesObj New preset object to update from.
   */
  populateUpdateAttributes(attributesObj){
    console.log(attributesObj);
    for (const[k, v] of Object.entries(attributesObj)){
      const currAttr = this.draftAttributes.find(attr => attr.pKey == k);
      if (currAttr) {
        currAttr.pValueNew = v;
        currAttr.updateValue = true;
      }
      else {
        // Initialize draft attribute that is null of value for a key that doesn't exist on the current preset
        const pdAttr = new PresetDraftAttribute(k, null, false);
        pdAttr.pValueNew = v;
        pdAttr.updateValue = false;
        this.draftAttributes.push(pdAttr);
      }
    }
  }

  /**
   * Update each of preset draft attribute's pLabel value using an i18n translator 
   * @param {VueI18n} translator
   * @param {string} localeStem 
   */
  nameAttributesUsingTranslator(translator, localeStem){
    for (const attr of this.draftAttributes){
      const attrLocaleKey = `${localeStem}.${attr.pKey}`
      const label = "";
      label = translator(attrLocaleKey);
      attr.pLabel = label;
    }
  }
}

/**
 * Intermediary object for users to modify a single preset's attribute before creating the preset
 */
class PresetDraftAttribute{
  /**
   * Create preset draft 
   * @param {string} key Preset attribute key
   * @param {string} value Value of the preset
   * @param {Boolean} include To include into the preset
   */
  constructor(key, value, include){
    this.pKey = key;
    this.pValue = value;
    this.pValueNew = null;
    this.updateValue = false
    this.include = include;
    this.pLabel = "";
  }
}


module.exports.PresetCollection = PresetCollection;
module.exports.Preset = Preset;
module.exports.PresetType = PresetType;
module.exports.PresetDraft = PresetDraft;
