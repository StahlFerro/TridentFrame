const { v4: uuidV4 } = require('uuid');
const { VueI18n } = require('vue-i18n');
const { Enumeration } = require('./enum.js');
// const { globalTranslate } = require('../locales/i18n.js');


/**
 * Different types of presets for categorization
 */
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
  static fromJSON(json) {
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
    this.lastModifiedDateTime = Date.now();
    this.name = "";
    this.presetType = null;
    this.presetObject = null;
  }
  
  /**
   * Create Preset instance from POJO object
   * @param {object} json POJO object
   * @returns {Preset} Preset class instance
   */
  static fromJSON(json){
    let preset = Object.assign(new Preset(), json);
    preset.name = json.name;
    return preset;
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
    preset.lastModifiedDateTime = Date.now();
    return preset;
  }

  /**
   * Update Preset from PresetDraft object
   * @param {string} newName New preset name
   * @param {PresetDraft} draft Draft with updated values
   */
  updateFromDraft(newName, draft){
    this.name = newName;
    for (const draftAttr of draft.draftAttributes) {
      const attrKey = draftAttr.pKey;
      if (draftAttr.conclusion().name == AttributeConclusion.ExcludeAttribute.name ) {
        delete this.presetObject[attrKey];
      }
      else if (draftAttr.conclusion().name == AttributeConclusion.IncludeNull.name) {
        this.presetObject[attrKey] = draftAttr.pValue;
      }
      else if (draftAttr.conclusion().name == AttributeConclusion.IncludeValue.name) {
        this.presetObject[attrKey] = draftAttr.pValueNew;
      }
      else if (draftAttr.conclusion().name == AttributeConclusion.UpdateValue.name) {
        this.presetObject[attrKey] = draftAttr.pValueNew;
      }
      else if (draftAttr.conclusion().name == AttributeConclusion.DoNothing.name) {

      }
    }
  }
  // static createfromJSON(json){
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



class AttributeConclusion extends Enumeration {
  static DoNothing = new AttributeConclusion(
    "DO_NOTHING", "Do nothing", "Do no changes to the existing attribute")
  static ExcludeAttribute = new AttributeConclusion(
    "EXCLUDE_ATTRIBUTE", "Exclude attribute", "Remove the attribute from the preset")
  static IncludeNull = new AttributeConclusion(
    "INCLUDE_NULL", "Include empty", "Add the attribute to the preset with empty value")
  static IncludeValue = new AttributeConclusion(
    "INCLUDE_VALUE", "Include value", "Add the attribute to the preset with new value")
  static UpdateValue = new AttributeConclusion(
    "UPDATE_VALUE", "Update value", "Update existing attribute's value with new value")
  constructor(name, label, description=""){
    super(name, label, description);
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
    this.currentlyIncluded = include
    this.pLabel = "";
  }

  // /**
  //  * Get conclusion in the event that only the plain object representation of a PresetDraftAttribute is obtained
  //  * @param {PresetDraftAttribute} draftAttr Preset draft attribute
  //  * @returns {string}
  //  */
  // static getConclusion(draftAttrJson) {
  //   const draftAttr = PresetDraftAttribute.fromJSON(draftAttrJson);
  //   return draftAttr.conclusion();
  // }

  /**
   * Recreate PresetDraftAttribute from plain object
   * @param {object} json Plain object
   * @returns {PresetDraftAttribute}
   */
  static fromJSON(json) {
    let draftAttr = new PresetDraftAttribute("", "", false);
    draftAttr = Object.assign(draftAttr, json);
    return draftAttr;
  }

  /**
   * Get the conclusion of the draft attribute's operation
   * @returns {AttributeConclusion}
   */
  conclusion() {
    if (!this.include && this.currentlyIncluded) {
      return AttributeConclusion.ExcludeAttribute;
    }
    else if (!this.currentlyIncluded && this.include) {
      if (this.pValueNew != null && this.updateValue)
        return AttributeConclusion.IncludeValue;
      else
        return AttributeConclusion.IncludeNull;
    }
    else if (this.include && this.currentlyIncluded && this.updateValue) {
      return AttributeConclusion.UpdateValue
    }
    else {
      return AttributeConclusion.DoNothing;
    }
  }
}


module.exports.PresetCollection = PresetCollection;
module.exports.Preset = Preset;
module.exports.PresetType = PresetType;
module.exports.PresetDraft = PresetDraft;
module.exports.PresetDraftAttribute = PresetDraftAttribute;
