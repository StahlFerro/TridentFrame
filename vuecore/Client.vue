<script>
const { execFile } = require("child_process");
const { stderr }=require("process");
const { PythonShell } = require("python-shell");
const deploy_env = process.env.DEPLOY_ENV;
const engine_exec_path = ".resources/app/engine/windows/main.exe";

function tridentEngine(args, callback) {
  console.log(`Current dir: ${process.cwd()}`);
  if (deploy_env == "DEV") {
    let pyOptions = {
      mode: "text",
      pythonPath: "python.exe",
      pythonOptions: ["-u"], // get print results in real-time
      // scriptPath: 'main.py',
    };
    pyOptions.args = args;
    console.log(args);
    let pyshell = new PythonShell("main.py", pyOptions);
    pyshell.on("message", (res) => {
      callback("", res);
    });
    pyshell.on("stderr", (err) => {
      callback(err, "");
    });
  } else if (deploy_env == "PROD") {
    const exec = require("child_process").execFile;
    exec(engine_exec_path, args, (error, stdout, stderr) => {
      console.log(">>error");
      console.log(error);
      console.log(">>stdout");
      console.log(stdout);
      console.log(">>stderr");
      console.log(stderr);
      if (error) {
        console.error(error);
      }
      else {
        callback(stderr, stdout);
      }
    });
  }
}
module.exports = {
  tridentEngine: tridentEngine,
};
</script>
