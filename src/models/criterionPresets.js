

class CriterionPresetCollection {
  constructor(presets){
    this.presets = presets;
  }

  static loadFromDirectory(dir) {
    
    console.debug("Start loading preset collection from presets folder...");
    try {
      // If app.toml file doesn't exist
      if (!existsSync(dir)) {
        console.warn("WARNING: presets directory file doesn't exist, creating")
        this.createPresetDir(dir);
      }
    } catch(err) {
      console.error(err)
    }
    
  }

  static createPresetDir(dir) {
    
  }
}

class CriterionPreset {
}

class CreationCriteriaPreset extends CriterionPreset {
  constructor(presetName, creationCriteria){
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