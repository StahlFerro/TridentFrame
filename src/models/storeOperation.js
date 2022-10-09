const { Enumeration } = require("./enum");

class StoreOperation extends Enumeration {
  static Add = new StoreOperation(
    "add_entry", "Add")
  static Update = new StoreOperation(
    "update_entry", "Update")
  static Delete = new StoreOperation(
    "delete_entry", "Delete")
  constructor(name, label, description=""){
    super(name, label, description);
  }
}

module.exports.StoreOperation = StoreOperation;