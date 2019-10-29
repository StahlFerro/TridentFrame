<script>
function quintcellLister(sequence_infos, from_where="") {
  // console.log(sequence_infos);
  var quintrows = {};
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
    return {"valid": false, "msg": `File names must not contain these following characters: < > : " / \ | ? *`};
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

const GIF_DELAY_DECIMAL_PRECISION = 2;
const APNG_DELAY_DECIMAL_PRECISION = 3;

module.exports.quintcellLister = quintcellLister;
module.exports.GIF_DELAY_DECIMAL_PRECISION = GIF_DELAY_DECIMAL_PRECISION;
module.exports.APNG_DELAY_DECIMAL_PRECISION = APNG_DELAY_DECIMAL_PRECISION;
module.exports.validateFilename = validateFilename;
module.exports.randString = randString;
module.exports.gcd = gcd;
</script>
