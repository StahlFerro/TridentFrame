
const { PythonShell } = require("python-shell");
const { ipcRenderer }  = require("electron");
const { env, cwd } = require("process");
const { spawn } = require("child_process");
const { PYTHON_PATH, ENGINE_EXEC_PATH } = require("./config.js");
const engine_env = env.DEPLOY_ENV;


const { EOL } = require('os');
const { isNullOrWhitespace } = require("./utility.js");


/**
 * Perform call to python console application.
 * @param {Array} args - Array of arguments. First element of the array must be the name of the python method on the PythonImager class. The rest are the respective method parameters.
 * @param {pyOutCallback} outCallback - The callback function to execute after receiving either stderr or stdout from python/child process. Must have arguments (error, res), which respresents stderr and stdout respectively. 
 * @param {callback} endCallback - The callback function to execute after python/child process terminates
 */
function tridentEngine(args, outCallback, endCallback) {
  console.log(`Current dir: ${cwd()}`);
  console.log(`DEPLOY ENV ${engine_env}`);

  let command = args[0];
  let cmd_args = args.slice(1);
  let json_command = JSON.stringify({
    "command": command, 
    "args": cmd_args,
    "globalvar_overrides": {
      "debug": true,
  }});


  if (engine_env == "DEV") {
    console.log("json_command");
    console.log(json_command);
    let pyshell = new PythonShell(ENGINE_EXEC_PATH, {
      mode: "text",
      pythonPath: PYTHON_PATH,
      // pythonOptions: ["-u"],
    });
    console.log("DEBUG 1");
    pyshell.on("message", (res) => {
      console.log("pycommander stdout start >>>>>");
      if (!(isNullOrWhitespace(res))) {
        console.log(res);
        parseStdOutAndCall(res, outCallback);
      }
      console.log("pycommander stdout end <<<<<");
    });
    console.log("DEBUG 2");
    pyshell.on("stderr", (err) => {
      console.log("pycommander stderr start >>>>>");
      if (!(isNullOrWhitespace(err))) {
        console.log(err);
        parseStdErrAndCall(err, outCallback);
      }
      console.log("pycommander stderr end <<<<<");
    });
    console.log("DEBUG 3");
    pyshell.send(`${json_command}\n`);
    
    console.log("DEBUG 4");
    pyshell.end(function (err,code,signal) {
      console.log("pycommander exit start >>>");
      console.log('[PYSHELL END EXIT CODE] ' + code); 
      console.log('[PYSHELL END EXIT SIGNAL] ' + signal);
      console.log('[PYSHELL END FINISHED]');
      if (err) {
        console.error(err);
      }
      console.log("out call back was:");
      console.log(outCallback)
      console.log("end call back is:");
      console.log(endCallback);
      if (code == 0 && endCallback) {
        endCallback();
      }
      console.log("pycommander exit end <<<");
    });
    console.log("DEBUG 5");
  } 
  
  else {
    console.debug("Spawning python engine");
    const child = spawn(ENGINE_EXEC_PATH, {mode: "text"});
    // child.stdout.on("data", receive.bind(this));
    console.debug("Attached event handlers");
    child.stdout.on("data", (data) => { receiveInternal("message", data, outCallback) });
    child.stderr.on("data", (err) => { receiveInternal("stderr", err, outCallback) });
    child.on('close', function (code) {
      console.log(`Program ended with code: ${code}`);
      if (code == 0 && endCallback) {
        endCallback();
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
  let _remaining;  
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
      parseStdOutAndCall(part, outCallback);
    }
    else if(emitType == 'stderr') {
      console.log(part);
      parseStdErrAndCall(part, outCallback);
    }
  });
}

function parseStdOutAndCall(outstream, callback) {
  try {
    let json = JSON.parse(outstream);
    if (json.debug) {
      console.log(json.debug);
    }
    else {
      callback("", json);
    }
  }
  catch (parseException) {
    console.error("[NOT JSON OUTSTREAM]");
    console.error(parseException);
    console.log(outstream)
  }
}

function parseStdErrAndCall(errStream, callback) {
  try {
    let err = JSON.parse(errStream);
    if (err.traceback)
      console.error(err.traceback.join())
    else if (err.error) {
      console.error(err.error);
      callback(err.error, "");
    }
  }
  catch (parseException) {
    console.error("[NOT JSON OUTSTREAM]");
    console.error(parseException);
    console.log(errStream)
  }
}

module.exports = {
  tridentEngine: tridentEngine
}