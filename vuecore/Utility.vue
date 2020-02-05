<script>
const path = require('path');
const fs = require('fs');
const remote = require("electron").remote;
const app = remote.app;

function quintcellLister(sequence_infos, from_where="") {
  var quintrows = {};
  // let sq_infos = Array.from(sequence_infos);
  // sq_infos.unshift("_CONTROL_CELL");
  console.log('sequence infos');
  console.log(sequence_infos);
  console.log('sq_infos');
  // console.log(sq_infos);
  for (var row = 0; row < Math.ceil(sequence_infos.length / 5); row++) {
    var quintcells = {}
    for (var c = 0; c < 5; c++) {
      const index = row * 5 + c;
      const img_info = sequence_infos[index];
      // console.log(img_info)
      if (img_info === undefined) {continue;}
      quintcells[c] = img_info;
    }
    quintrows[row] = quintcells;
  }
  console.log('after');
  console.log(quintrows);
  return quintrows;
}

function validateFilename(filename) {
  // Valid if the filename does not contain these characters: <>:"/\|?*
  var is_valid = !filename.match(/[<>:"\/\\|\?\*]/g);
  if (is_valid) {
    return {"valid": true, "msg": ""};
  }
  else {
    return {"valid": false, "msg": `File names must not contain these following characters: < > : " / \\ | ? *`};
  }
}

function ticks() {
  let epoch = new Date().getTime() * 10000;
  console.log(epoch);
  return epoch
}

function randString() {
   let result = '';
   let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   let charactersLength = characters.length;
   for ( let i = 0; i < 50; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

function gcd(a, b) { // Gets the greatest common divisor between two numbers
  if (b == 0)
    return a;
  else
    return gcd(b, (a % b));
}

function wholeNumConstrain(event) {
  console.log('wholeNumConstrain', event.key);
  if (event.key != "." && event.key != 'e') {
    console.log("IS DIGIT!");
    return true;
  }
  else {
    console.log("IS NOT DIGIT!");
    event.preventDefault();
  }
}

function floatConstrain(event) {
  console.log('float constrain', event);
  let current_value = event.target.value;
  let key = event.key;
  if (current_value.includes(".") && key == ".") {
    event.preventDefault();
  }
  else {
    return true;
  }
  // let float_regex = new RegExp('(^[0-9]*\\.?[0-9]*$)');
  // if (float_regex.test(event.target.value)) {
  //   console.log("IS FLOAT!");
  //   return true;
  // }
  // else {
  //   console.log("NOT FLOAT!");
  //   event.preventDefault();
  // }
}

function numConstrain(event, must_unsigned=false, must_whole=false) {
  console.log(event);
  console.log("num constrain args", must_unsigned, must_whole);
  let current_value = event.target.value;
  console.log("current value", current_value);
  let key = event.key;
  let is_unsigned = false;
  let is_whole = false;
  let is_violating = false;
  if ((current_value.includes(".") && key == ".") || key == 'e') {
    event.preventDefault();
  }
  else {
    if (must_unsigned) {
      is_violating = event.key == '-'? true : is_violating;
      console.log("is violating must_unsigned", event.key == '-');
    }
    if (must_whole) {
      is_violating = event.key == '.'? true : is_violating;
      console.log("is violating must_whole", event.key == '.');
    }
    if (is_violating) { event.preventDefault(); }
    else { return true; }
  }
}

function posWholeNumConstrain(event) {
  console.log(event.key);
  if (event.key != "." && event.key != '-') {
    console.log("IS DIGIT!");
    return true;
  }
  else {
    console.log("IS NOT DIGIT!");
    event.preventDefault();
  }
}

function fileExists(out_dir, name) {
  let full_path = path.join(out_dir, name);
  console.log("full path", full_path);
  return fs.existsSync(full_path);
}


const GIF_DELAY_DECIMAL_PRECISION = 2;
const APNG_DELAY_DECIMAL_PRECISION = 3;

module.exports = {
  quintcellLister: quintcellLister,
  GIF_DELAY_DECIMAL_PRECISION: GIF_DELAY_DECIMAL_PRECISION,
  APNG_DELAY_DECIMAL_PRECISION: APNG_DELAY_DECIMAL_PRECISION,
  validateFilename: validateFilename,
  randString: randString,
  gcd: gcd,
  wholeNumConstrain: wholeNumConstrain,
  posWholeNumConstrain: posWholeNumConstrain,
  numConstrain: numConstrain,
  floatConstrain: floatConstrain,
  fileExists: fileExists,
}

</script>
