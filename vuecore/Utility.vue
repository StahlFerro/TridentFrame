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
  console.log("quintrow", from_where)
  console.log(quintrows);
  return quintrows;
}

const GIF_DELAY_DECIMAL_PRECISION = 2;

module.exports.quintcellLister = quintcellLister;
module.exports.GIF_DELAY_DECIMAL_PRECISION = GIF_DELAY_DECIMAL_PRECISION;
</script>
