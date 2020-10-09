<script>
const { PythonShell } = require('python-shell');
let pyOptions = {
  mode: 'text',
  pythonPath: 'python.exe',
  pythonOptions: ['-u'], // get print results in real-time
  // scriptPath: 'main.py',
};
function getPyShell(args) {
  pyOptions.args = args;
  return new PythonShell("main.py", pyOptions);
}
module.exports = {
  getPyShell: getPyShell,
}
</script>
