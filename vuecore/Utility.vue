<script>
function quintcellLister(sequence_paths, from_where="") {
  var quintrows = {};
  for (var row = 0; row < Math.ceil(sequence_paths.length / 5); row++) {
    var quintcells = []
    for (var c = 0; c < 5; c++) {
      const index = row * 5 + c;
      const img_path = sequence_paths[index];
      if (img_path === undefined) {continue;}
      quintcells.push(img_path);
    }
    quintrows[row] = quintcells;
  }
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
  return new Date().getTime() * 10000;
}

const GIF_DELAY_DECIMAL_PRECISION = 2;

module.exports.quintcellLister = quintcellLister;
module.exports.GIF_DELAY_DECIMAL_PRECISION = GIF_DELAY_DECIMAL_PRECISION;
module.exports.validateFilename = validateFilename;
module.exports.ticks = ticks;
</script>
