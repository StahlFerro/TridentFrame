const { roundPrecise } = require("./utility");

function varToSpaceUpper(meta_categ) {
  return meta_categ.replace("_", " ").toUpperCase();
}

function escapeLocalPath(path) {
  return path.replace("%", "%25");
}

/***
 * Convert bytes to human-readable file sizes using the biggest possible size unit without having the value smaller than 1
 * @param {int} nbytes - Total amount of bytes
 * @param {int} precision - Amount of decimal places to round up
 */
function readFilesize(nbytes, precision) {
  let i = 0;
  let size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
  while (nbytes >= 1024 && i < size_suffixes.length - 1) {
    nbytes /= 1024;
    i += 1;
  }
  let size = roundPrecise(nbytes, precision);
  // size = str(round(nbytes, 3)).rstrip('0').rstrip('.')
  return `${size} ${size_suffixes[i]}`;
}

module.exports = {
  varToSpaceUpper: varToSpaceUpper,
  escapeLocalPath: escapeLocalPath,
  readFilesize: readFilesize,
}
