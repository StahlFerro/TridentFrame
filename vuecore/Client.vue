<script>
const { PythonShell } = require('python-shell');
const deploy_env = process.env.DEPLOY_ENV;
const engine_dir = "resources/app/engine/wnidows/main.exe"

function getPyShell(args) {
  console.log(deploy_env);
  if (deploy_env == 'DEV') {
    let pyOptions = {
      mode: 'text',
      pythonPath: 'python.exe',
      pythonOptions: ['-u'], // get print results in real-time
      // scriptPath: 'main.py',
    };
    pyOptions.args = args;
    console.log(args);
    return new PythonShell("main.py", pyOptions);
  }
  else {
    const exec = require('child_process').exec;
  }
}
module.exports = {
  getPyShell: getPyShell,
}
</script>
