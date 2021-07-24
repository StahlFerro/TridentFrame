const { roundPrecise } = require("./calculations.js");

function varToSpaceUpper(meta_categ) {
  return meta_categ.replace("_", " ").toUpperCase();
}

/**
 * Generate random alphanumeric string
 * @param {number} Output string length
 */
function randString(length) {
  let result = '';
  let charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let charsetlen = charset.length;
  for ( let i = 0; i < length; i++ ) {
     result += charset.charAt(Math.floor(Math.random() * charsetlen));
  }
  return result;
}

/***
 * Convert bytes to human-readable file sizes using the biggest possible size unit without having the value smaller than 1
 * @param {number} nbytes - Total amount of bytes
 * @param {number} precision - Amount of decimal places to round up
 */
function formatBytes(nbytes, precision) {
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


/**
 * Check whether a string is null or whitespace
 * @param {string} input String to check
 */
function isNullOrWhitespace(input) {
  if (typeof input === 'undefined' || input == null) return true;
  return input.replace(/\s/g, '').length < 1;
}

// function quintcellLister(sequence_infos, from_where="") {
//   var quintrows = {};
//   // let sq_infos = Array.from(sequence_infos);
//   // sq_infos.unshift("_CONTROL_CELL");
//   console.log('sequence infos');
//   console.log(sequence_infos);
//   console.log('sq_infos');
//   // console.log(sq_infos);
//   for (var row = 0; row < Math.ceil(sequence_infos.length / 5); row++) {
//     var quintcells = {}
//     for (var c = 0; c < 5; c++) {
//       const index = row * 5 + c;
//       const img_info = sequence_infos[index];
//       // console.log(img_info)
//       if (img_info === undefined) {continue;}
//       quintcells[c] = img_info;
//     }
//     quintrows[row] = quintcells;
//   }
//   console.log('after');
//   console.log(quintrows);
//   return quintrows;
// }

module.exports = {
  varToSpaceUpper: varToSpaceUpper,
  formatBytes: formatBytes,
  randString: randString,
  isNullOrWhitespace: isNullOrWhitespace,
}
