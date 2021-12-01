import v8 from "v8";

/**
 * Deep-clone an object
 * @param {*} obj 
 */
export function structuredClone(obj) {
  return v8.deserialize(v8.serialize(obj));
};
