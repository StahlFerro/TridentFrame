
import { env, cwd } from "process";
import { spawn } from "child_process";
import { PythonShell } from "python-shell";
import { PYTHON_PATH, ENGINE_EXEC_PATH } from "../constants/appconfig";
import { NewlineTransformer } from "./stream_transformer";
import { isNullOrWhitespace } from "../utility/stringutils";


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
    console.error({
      error: "[NOT JSON OUTSTREAM]",
      parseException: parseException,
      outstream: outstream,
    });
  }
}

function parseStdErrAndCall(errStream, callback) {
  try {
    let err = JSON.parse(errStream);
    if (err.traceback)
      console.error(err.traceback.join())
    if (err.error) {
      console.error(err.error);
      callback(err.error, "");
    }
  }
  catch (parseException) {
    console.error({
      error: "[NOT JSON OUTSTREAM]",
      parseException: parseException,
      outstream: errStream,
    });
  }
}


// let _remaining;

// Old buffer processor (copied from python-shell v2.0.3 repository)
// https://github.com/extrabacon/python-shell/blob/f3b64d3307d8dc15eb9c071d8aa774c1e7d5b2d7/index.ts#L379 receiveInternal method
// function processBuffer(emitType, data, outCallback){
//   console.log({"buffer": data});
//   console.log({"remaining": _remaining});
//   let parts = (''+data).split(EOL);
//   if (parts.length === 1) {
//     // an incomplete record, keep buffering
//     _remaining = (_remaining || '') + parts[0];
//   }
//   let lastLine = parts.pop();
//   // fix the first line with the remaining from the previous iteration of 'receive'
//   parts[0] = (_remaining || '') + parts[0];
//   // keep the remaining for the next iteration of 'receive'
//   _remaining = lastLine;
//   parts.forEach(function (part) {
//     if(emitType == 'message') {
//       console.log(part);
//       parseStdOutAndCall(part, outCallback);
//     }
//     else if(emitType == 'stderr') {
//       console.log(part);
//       parseStdErrAndCall(part, outCallback);
//     }
//   });
// }


/**
 * Perform call to python console application.
 * @param {Array} args - Array of arguments. First element of the array must be the name of the python method on the PythonImager class. The rest are the respective method parameters.
 * @param {pyOutCallback} outCallback - The callback function to execute after receiving either stderr or stdout from python/child process. Must have arguments (error, res), which respresents stderr and stdout respectively. 
 * @param {callback} endCallback - The callback function to execute after python/child process terminates
 */
export function tridentEngine(args, outCallback, endCallback) {
  console.log(`Current dir: ${cwd()}`);
  console.log(`DEPLOY ENV ${env.DEPLOY_ENV}`);

  let command = args[0];
  let cmd_args = args.slice(1);
  let json_command = {
    "command": command, 
    "args": cmd_args,
    "globalvar_overrides": {
      "debug": true,
    }
  };
  let str_cmd = JSON.stringify(json_command);


  if (env.DEPLOY_ENV == "DEV") {
    console.log({"json_command": json_command});
    console.log("str_cmd");
    console.log(str_cmd);
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
    pyshell.send(`${str_cmd}\n`);
    
    console.log("DEBUG 4");
    pyshell.end(function (err,code,signal) {
      console.log("pycommander exit start >>>");
      console.log({status: "exited", code: code, signal: signal});
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

    /*
    * New stdout and stderr buffering using NewlineTransformer
    * Reference: https://github.com/extrabacon/python-shell/blob/5b6c3165136bfb320615dd2e8c12fcceceeb3164/index.ts#L176-L197
    Node buffers stdout&stderr in batches regardless of newline placement
    This is troublesome if you want to recieve distinct individual messages
    for example JSON parsing breaks if it recieves partial JSON
    so we use newlineTransformer to emit each batch seperated by newline
    */

    console.debug("Spawning python engine");
    const child = spawn(ENGINE_EXEC_PATH, {mode: "text"});
    // child.stdout.on("data", receive.bind(this));
    console.debug("Attached event handlers");
    let stdoutSplitter = new NewlineTransformer();
    let stderrSplitter = new NewlineTransformer();
    stdoutSplitter.setEncoding('utf8');
    stderrSplitter.setEncoding('utf8');
    child.stdout.pipe(stdoutSplitter).on('data', (chunk) => {
      parseStdOutAndCall(chunk, outCallback);
    });
    child.stderr.pipe(stderrSplitter).on('data', (chunk) => {
      parseStdErrAndCall(chunk, outCallback);
    });

    // child.stdout.on("data", (data) => { processBuffer("message", data, outCallback) });
    // child.stderr.on("data", (err) => { processBuffer("stderr", err, outCallback) });
    child.on('close', function (code) {
      console.log(`Program ended with code: ${code}`);
      if (code == 0 && endCallback) {
        endCallback();
      }
    });
    console.log("beforewrite");
    child.stdin.write(`${str_cmd}\n`, (error) => {
      if (error)
        console.log({"stdin.write error": error});
    });
    child.stdin.end();
    console.log("afterwrite");
    child.on('exit', function (code) {
      console.log({status: "exited", code: code});
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
};
