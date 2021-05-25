<script>
const { PythonShell } = require("python-shell");
const process = require("process");
const fs = require('fs');
const deploy_env = process.env.DEPLOY_ENV;
const settings = JSON.parse(fs.readFileSync(deploy_env == "DEV"? "./config/settings.json" : "./resources/app/config/settings.json"));
const cache_path = deploy_env == "DEV"? `./${settings.cache_dir}` : `./resources/app/engine/windows/${settings.cache_dir}`;
const bufferfile = `${cache_path}/${settings.bufferfile}`;
const criterionfile = `${cache_path}/${settings.criterionfile}`;
const { EOL } = require('os');
const { isNullOrWhitespace } = require("./Utility.vue");
let _remaining;

let python_path = "";
let engine_exec_path = "";
if (process.platform == "win32") {
  python_path = "python.exe";
  engine_exec_path = "./resources/app/engine/windows/main.exe";
}
else if (process.platform == "linux") { 
  python_path = "python3.7";
  engine_exec_path = "./resources/app/engine/linux/main";
}

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

/**
 * @callback pyOutCallback
 * @param {string} error - Python STDOUT
 * @param {string} res - Python STDIN
 */

/**
 * Perform call to python console application.
 * @param {Array} args - Array of arguments. First element of the array must be the name of the python method on the PythonImager class. The rest are the respective method parameters.
 * @param {pyOutCallback} outCallback - The callback function to execute after receiving either stderr or stdout from Python. Must have arguments (error, res), which respresents stderr and stdout respectively. 
 */
function tridentEngine(args, outCallback) {
  console.log(`Current dir: ${process.cwd()}`);
  console.log(`DEPLOY ENV ${deploy_env}`);

  let command = args[0];
  let cmd_args = args.slice(1);
  let json_command = JSON.stringify({
    "command": command, 
    "args": cmd_args,
    "globalvar_overrides": {
      "debug": true,
  }});
  console.log("json_command");
  console.log(json_command);


  if (deploy_env == "DEV") {
    let pyshell = new PythonShell('main.py',{
      mode: "text",
      pythonPath: python_path,
      // pythonOptions: ["-u"],
    });
    pyshell.on("message", (res) => {
      if (!(isNullOrWhitespace(res))) {
        console.log("pycommander stdout >>>");
        try {
          let data = JSON.parse(res);
          if (data.debug) {
            console.log(data.debug);
          }
          else {
            outCallback("", data);
          }
        }
        catch (parseException) {
          console.log("[NOT JSON]");
          console.log(res);
        }
      }
    });
    pyshell.on("stderr", (err) => {
      if (!(isNullOrWhitespace(err))) {
        console.log("pycommander stderr >>>");
        console.log(err);
        try {
          let errdata = JSON.parse(err);
          if (errdata.traceback)
            console.error(errdata.traceback.join())
          else if (errdata.error) {
            console.error(errdata.error);
            outCallback(errdata.error, "");
          }
        }
        catch (parseErr) {
          console.error(err);
        }
      }
    });
    pyshell.send(json_command);
    pyshell.end(function (err,code,signal) {
      console.log("pycommander end >>>");
      if (err) {
        console.error(err);
      }
      console.log('[PYSHELL END EXIT CODE] ' + code);
      console.log('[PYSHELL END EXIT SIGNAL] ' + signal);
      console.log('[PYSHELL END FINISHED]');
    });
  } 
  
  else {
    const spawn = require("child_process").spawn;
    const child = spawn(engine_exec_path, {mode: "text"});
    // child.stdout.on("data", receive.bind(this));
    child.stdout.on("data", (data) => { receiveInternal("message", data, outCallback) });
    child.stderr.on("data", (err) => { receiveInternal("stderr", err, outCallback) });
    child.on('close', function (code) {
      if (code != 0) {
        console.log("Program ended with a error code : " + code);
      }
    });
    console.log("beforewrite");
    child.stdin.write(`${json_command}\n`, (error) => {
      console.log(`[send error]\n${error}`);
    });
    child.stdin.end();
    console.log("afterwrite");
    child.on('exit', function (code) {
      console.log('child process exited with code ' + code.toString());
    });
    // exec(engine_exec_path, args, (error, stdout, stderr) => {
    //   console.log(">>error");
    //   console.log(error);
    //   console.log(">>stdout");
    //   console.log(stdout);
    //   console.log(">>stderr");
    //   console.log(stderr);
    //   if (stderr) {
    //     console.log("[PYTHON STDERR]");
    //     outCallback(stderr, "");
    //   }
    //   else if (stdout) {
    //     console.log("[PYTHON STDOUT]");
    //     outCallback("", stdout);
    //   }
    // });
  }
}

function receiveInternal(emitType, data, outCallback){
  console.log(data);
  let parts = (''+data).split(EOL);
  if (parts.length === 1) {
    // an incomplete record, keep buffering
    _remaining = (_remaining || '') + parts[0];
  }
  let lastLine = parts.pop();
  // fix the first line with the remaining from the previous iteration of 'receive'
  parts[0] = (_remaining || '') + parts[0];
  // keep the remaining for the next iteration of 'receive'
  _remaining = lastLine;

  parts.forEach(function (part) {
    if(emitType == 'message') {
      console.log(part);
      outCallback("", part);
    }
    else if(emitType == 'stderr') {
      console.log(part);
      outCallback(part, "");
    }
  });
}

module.exports = {
  tridentEngine: tridentEngine,
  writeImagePathsCache: writeImagePathsCache,
  writeCriterionCache: writeCriterionCache,
  settings: settings,
};

</script>
