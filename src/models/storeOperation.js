class StoreOperation {
  static Add = new StoreOperation(
    "add_entry", "Add")
  static Update = new StoreOperation(
    "update_entry", "Update")
  static Delete = new StoreOperation(
    "delete_entry", "Delete")
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

module.exports.StoreOperation = StoreOperation;