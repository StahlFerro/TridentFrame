<script>
const { execFile } = require("child_process");
const { stderr }=require("process");
const { PythonShell } = require("python-shell");
const fs = require('fs');
const deploy_env = process.env.DEPLOY_ENV;
const engine_exec_path = "./resources/app/engine/windows/main.exe";
const settings = JSON.parse(fs.readFileSync(deploy_env == "DEV"? "./config/settings.json" : "./resources/app/config/settings.json"));
const cache_path = deploy_env == "DEV"? `./${settings.cache_dir}` : `./resources/app/engine/windows/${settings.cache_dir}`;
const bufferfile = `${cache_path}/${settings.bufferfile}`;
const criterionfile = `${cache_path}/${settings.criterionfile}`;

function writeImagePathsCache(paths) {
  if (!fs.existsSync(cache_path)){
      fs.mkdirSync(cache_path);
      fs.writeFileSync(`${cache_path}/.include`, "");
  }
  fs.writeFileSync(bufferfile, JSON.stringify(paths));
}

function writeCriterionCache(vals) {
  if (!fs.existsSync(cache_path)){
      fs.mkdirSync(cache_path);
      fs.writeFileSync(`${cache_path}/.include`, "");
  }
  fs.writeFileSync(criterionfile, JSON.stringify(vals));
}

function tridentEngine(args, callback) {
  console.log("argon");
  console.log(`Current dir: ${process.cwd()}`);
  console.log(`DEPLOY ENV ${deploy_env}`);
  if (deploy_env == "DEV") {
    let pyshell = new PythonShell('main.py',{
      mode: "text",
      pythonPath: "python.exe",
      pythonOptions: ["-u"],
    });
    let command = args[0];
    let cmd_args = args.slice(1);
    console.log("json_command");
    let json_command = JSON.stringify({"command": command, "args": cmd_args})
    pyshell.on("message", (res) => {
      console.log("[PYTHON STDOUT RAW MSG RES]")
      console.log(res);
      callback("", res);
    });
    pyshell.on("stderr", (err) => {
      console.log("[PYTHON STDOUT RAW ERR RES]");
      console.log(err);
      callback(err, "");
    });
    console.log("json_command");
    console.log(json_command);
    pyshell.send(json_command);
    pyshell.end();
  } else {
    const exec = require("child_process").execFile;
    exec(engine_exec_path, args, (error, stdout, stderr) => {
      console.log(">>error");
      console.log(error);
      console.log(">>stdout");
      console.log(stdout);
      console.log(">>stderr");
      console.log(stderr);
      if (stderr) {
        callback(stderr, "");
      }
      else if (stdout) {
        console.log("[PYTHON STDERR]");
        console.error(err);
        callback("", stdout);
      }
    });
  }
}
module.exports = {
  tridentEngine: tridentEngine,
  writeImagePathsCache: writeImagePathsCache,
  writeCriterionCache: writeCriterionCache,
};

</script>
