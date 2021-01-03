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
