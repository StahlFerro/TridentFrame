<script>
const { PythonShell } = require('python-shell');
const deploy_env = process.env.DEPLOY_ENV;
let pyOptions = {
  mode: 'text',
  pythonPath: 'python.exe',
  pythonOptions: ['-u'], // get print results in real-time
  // scriptPath: 'main.py',
};
function getPyShell(args) {
  console.log(deploy_env);
  pyOptions.args = args;
  console.log(args);
  return new PythonShell("main.py", pyOptions);
}
module.exports = {
  getPyShell: getPyShell,
}
</script>
