<template>
  <div id="settings_panel" class="container" style="display: none; padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td>
          <a v-on:click="refreshWindow" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <font-awesome-icon icon="redo-alt"/>
            </span>
            <span>Reload Window</span>
          </a>
        </td>
        <td>
          <a v-on:click="openInspector" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <font-awesome-icon icon="bug"/>
              <!-- <i class="fas fa-bug"></i> -->
            </span>
            <span>Open Inspector</span>
          </a>
        </td>
      </tr>
      <tr>
        <td>
          <a v-on:click="btnGetSettings" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <font-awesome-icon icon="bug"/>
            </span>
            <span>Get Settings</span>
          </a>
        </td>
        <td>
          <a v-on:click="btnSaveSettings" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <font-awesome-icon icon="bug"/>
            </span>
            <span>Set Settings</span>
          </a>
        </td>
      </tr>

      <tr>
        <td>
          <a v-on:click="btnRelaunchApp" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <font-awesome-icon icon="power-off"/>
            </span>
            <span>Relaunch App</span>
          </a>
        </td>
        <!-- <td>
          <a v-on:click="testGenerator" class="button is-large is-neon-cyan">
            <span class="icon is-large">
              <i class="fas fa-bug"></i>
            </span>
            <span>Test Generator</span>
          </a>
        </td> -->
      </tr>
      <!-- 
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
import { ipcRenderer } from "electron";
import { tridentEngine } from "../modules/streams/trident_engine.js";

export default {
  methods: {
    refreshWindow() {
      ipcRenderer.invoke('reload-window');
    },
    openInspector() {
      ipcRenderer.invoke('open-inspector');
    },
    btnGetSettings() {
      const SETTINGS = ipcRenderer.sendSync("get-settings");
      console.log(SETTINGS);
    },
    btnSaveSettings() {
      ipcRenderer.sendSync("set-settings", "light");
    },
    btnRelaunchApp() {
      ipcRenderer.invoke("relaunch-application");
    },
    ipcWindow: function() {
      let extension_filters = [
        {
          name: "Images",
          extensions: ["png", "gif", "jpg", "webp"],
        },
      ];
      let file_dialog_props = ["openfile"];
      let dir_dialog_props = ["openDirectory", "createDirectory"];
      var options = {
        filters: extension_filters,
        properties: file_dialog_props,
      };
      console.log('before invoke');
      ipcRenderer.invoke('open-dialog', options).then((result) => {
        tridentEngine(["inspect_one", result.filePaths[0]], (error, res) => {
          console.log(res);
        })
      });
      console.log('after invoke here');

    }
  },
  mounted: function() {
    ipcRenderer.invoke('reload-window-once');
  }
  /** 
   * *TODO: Find the actual cause of this bug.
  // There is a weird bug in linux, in which performing the first tridentengine executable call from UI returns no response from the event handlers,
  // while subsequent calls behave normally. This terrible workaround is in place so that the tridentengine executable is called at least
  // once upon application startup
  * ! Update: As of 2021-07-09 this workaround does not work. The new observed behavior is that loading images in CreatePanel works, but
  * ! image previewing/processing does not work
  **/
  // mounted: function() {
  //   if (process.platform == "linux") {
  //     setTimeout(function() {
  //       tridentEngine(["echo", "PING"], (error, res) => {
  //         console.debug(res);
  //       })
  //       tridentEngine(["info"], (error, res) => {
  //         console.debug(res);
  //       })
  //     }, 300);
  //   }
  // }
};
</script>
