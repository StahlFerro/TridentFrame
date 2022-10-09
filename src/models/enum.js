class Enumeration {
  constructor(name, label, description="") {
    this.name = name;
    this.label = label;
    this.description = description;
  }
  static getAll() {
    return Object.keys(this).map(k => this[k]);
  }
  static fromName(name) {
    return this.getAll().filter(pt => pt.name === name)[0];
  }
}

module.exports.Enumeration = Enumeration;