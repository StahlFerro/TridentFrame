import { nanoid } from "nanoid";

const { readdirSync } = require("fs");


class CriterionPresetCollection {
  constructor(presets){
    this.presets = [];
  }

  static loadFromDirectory(dir) {
    
    console.debug("Start loading preset collection from presets folder...");
    try {
      // If app.toml file doesn't exist
      if (!existsSync(dir)) {
        console.warn("WARNING: presets directory file doesn't exist, creating")
        this.createPresetDir(dir);
      }
      const jsonFiles = readdirSync(dir).filter(file => path.extname(file) === '.json');
      jsonFiles.forEach(jsonPath => {
        const fileContent = readFileSync(join(dir, jsonPath), { encoding: "utf-8"});
        const preset = JSON.parse()
      });
    } catch(err) {
      console.error(err)
    }
    
  }

  static createPresetDir(dir) {
    
  }
}

class CriterionPreset {
  constructor(existingId) {
    this.id = existingId? existingId : nanoid()
    this.criteria = false;
  }
  static createfromJson(json){
    let criterionPreset = new CriterionPreset();
    Object.assign(criterionPreset, json)
  }
  updateFromCriteria(criteria){
    let criterionPreset = new CriterionPreset();
    Object.assign(this, )
  }
}

class CreationCriteriaPreset extends CriterionPreset {
  constructor(objc){
    this.presetName = presetName;
    this.creationCriteria = creationCriteria;
  }
}

class ModificiationCriteriaPreset extends CriterionPreset{
  constructor(presetName, modificationCriteria) {
    this.presetName = presetName;
    this.modificationCriteria = modificationCriteria;
  }
}

export {
  CriterionPresetCollection
}