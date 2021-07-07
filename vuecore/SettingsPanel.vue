<template>
  <div id="settings_panel" class="container" style="display: none; padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td>
          <a v-on:click="refreshWindow" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-redo-alt"></i>
            </span>
            <span>Reload Window</span>
          </a>
        </td>
        <td>
          <a v-on:click="openInspector" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-bug"></i>
            </span>
            <span>Open Inspector</span>
          </a>
        </td>
      </tr>
      <tr>
        <td>
          <a v-on:click="ipcWindow" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-window-maximize"></i>
            </span>
            <span>IPC Window Test</span>
          </a>
        </td>
      </tr>

      <!-- <tr>
        <td>
          <a v-on:click="purgeCacheTemp" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-ban"></i>
            </span>
            <span>Purge Cache</span>
          </a>
        </td>
        <td>
          <a v-on:click="testGenerator" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-bug"></i>
            </span>
            <span>Test Generator</span>
          </a>
        </td>
      </tr>
      <tr>
        <td>
          <a v-on:click="openConfirm" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-bug"></i>
            </span>
            <span>Confirm tester</span>
          </a>
        </td>
        <td>
          <a v-on:click="callPython" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fab fa-python"></i>
            </span>
            <span>TestExec</span>
          </a>
        </td>
      </tr> -->

    </table>
  </div>
</template>

<script>
const { remote, BrowserWindow, ipcRenderer } = require("electron");
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { tridentEngine } = require("./PythonCommander.js");
const { PythonShell } = require("python-shell");

function callPython() {
  let shell = new PythonShell('main.py', { 
    mode: "text",
    pythonPath: "python.exe",
    pythonOptions: ["-u"],
  });
  let jsonmsg = JSON.stringify({"command": "echostream", "args": [1, 3, 6]})
  shell.send(jsonmsg);
  shell.on('message', function (message) {
    console.log('[STDOUT message]');
    console.log(message);
  });
  shell.end();
}

function refreshWindow() {
  remote.getCurrentWindow().reload();
  session.clearCache(() => {});
}

function purgeCacheTemp() {
  client.invoke("purge_cache_temp", (error, res) => {
    if (error) {
      console.error(error);
    } else if (res) {
      console.log(res);
    }
  });
}

function openInspector() {
  remote.getCurrentWebContents().openDevTools({mode: 'detach'});
  var devtools = remote.getCurrentWindow().devToolsWebContents;
  if (devtools) { devtools.focus(); }
}

function openCWD() {
  console.log('openCWD');
  client.invoke("print_cwd", (error, res) => {
    if (error) {
      console.error(error);
    } else if (res) {
      console.log("JS DIRNAME", __dirname)
      console.log(res);
    }
  })
}

function testGenerator() {
  client.invoke("test_generator", (error, res) => {
    if (error) {
      console.error(error);
    } else if (res) {
      console.log(res);
    }
  })
}

function openConfirm() {
  let WINDOW = remote.getCurrentWindow();
  let options  = {
    buttons: ["Yes", "Cancel"],
    message: "A file with the same name exists in the output folder. Do you want to override it?"
  };
  let response = dialog.showMessageBoxSync(WINDOW, options);
  console.log(`response: ${response}`)
}


let extension_filters = [
  {
    name: "Images",
    extensions: ["png", "gif", "jpg", "webp"],
  },
];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

export default {
  methods: {
    refreshWindow: refreshWindow,
    purgeCacheTemp: purgeCacheTemp,
    openInspector: openInspector,
    openCWD: openCWD,
    testGenerator: testGenerator,
    openConfirm: openConfirm,
    callPython: callPython,
    ipcWindow: function() {
      var options = {
        filters: extension_filters,
        properties: file_dialog_props,
      };
      console.log('before invoke');
      // ipcRenderer.invoke('open-dialog', options).then((result) => {
        tridentEngine(["inspect_one", "/home/iceberg/Pictures/Florian de Looij/squares.gif"], (error, res) => {
          console.log(res);
        })
      // });
      console.log('after invoke here');

    }
  },
  /** 
   * *TODO: Find the actual cause of this bug.
  There is a weird bug in linux, in which performing the first tridentengine executable call from UI returns no response from the event handlers,
  while subsequent calls behave normally. This terrible workaround is in place so that the tridentengine executable is called at least
  once upon application startup.
  **/
  mounted: function() {
    if (process.platform == "linux") {
      setTimeout(function() {
        tridentEngine(["echo", "PING"], (error, res) => {
          console.debug(res);
        })
        tridentEngine(["info"], (error, res) => {
          console.debug(res);
        })
      }, 300);
    }
  }
};
</script>
