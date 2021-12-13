<template>
  <div id="settings_panel" style="display: none">
    <div class="settings-panel-root">
      <div class="settings-tab">
        <div class="tabs">
          <ul>
            <li :class="{ 'is-active': settings_tab_selection == 0 }">
              <a @click="settings_tab_selection = 0">General</a>
            </li>
            <li :class="{ 'is-active': settings_tab_selection == 1 }">
              <a @click="settings_tab_selection = 1">Window</a>
            </li>
            <li :class="{ 'is-active': settings_tab_selection == 2 }">
              <a @click="settings_tab_selection = 2">About</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="settings-subpanels">
        <div
          class="settings-subpanel-general"
          v-show="settings_tab_selection == 0"
        >
          <table class="table is-borderless" style="padding: 5px" width="100%">
            <!-- <tr>
              <td>
                <a
                  v-on:click="btnGetSettings"
                  class="button is-large is-neon-cyan"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="bug" />
                  </span>
                  <span>Get Settings</span>
                </a>
              </td>
              <td>
                <a
                  v-on:click="btnSaveSettings"
                  class="button is-large is-neon-cyan"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="bug" />
                  </span>
                  <span>Set Settings</span>
                </a>
              </td>
            </tr> -->

            <tr>
              <td>
                <label class="checkbox">
                  <input v-model="USER_SETTINGS.fullscreen" type="checkbox" />
                  Start in fullscreen
                </label>
              </td>
            </tr>
          </table>
        </div>

        <div
          class="settings-subpanel-window"
          v-show="settings_tab_selection == 1"
        >
          <table class="table is-borderless" style="padding: 5px" width="100%">
            <tr>
              <td>
                <a
                  v-on:click="refreshWindow"
                  class="button is-large is-neon-cyan"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="redo-alt" />
                  </span>
                  <span>Reload Window</span>
                </a>
              </td>
              <td>
                <a
                  v-on:click="openInspector"
                  class="button is-large is-neon-white"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="bug" />
                    <!-- <i class="fas fa-bug"></i> -->
                  </span>
                  <span>Open Inspector</span>
                </a>
              </td>
            </tr>
            <tr>
              <td>
                <a
                  v-on:click="btnRelaunchApp"
                  class="button is-large is-neon-sunset"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="power-off" />
                  </span>
                  <span>Relaunch App</span>
                </a>
              </td>
            </tr>
          </table>
        </div>

        <div
          class="settings-subpanel-about"
          v-show="settings_tab_selection == 2"
        >
          <div class="about-content">
            <div class="about-info">
              <img v-bind:src="logo" class="about-logo no-select-drag" />
              <h1 class="about-software-name">TridentFrame</h1>
              <p class="about-software-version">v0.1.0-beta.9</p>
              <p class="about-software-copyright">
                Copyright
                <span class="icon">
                  <font-awesome-icon :icon="['far', 'copyright']" />
                </span>
                2021 StahlFerro
              </p>
              <!-- <p class="about-software-author">Developed by StahlFerro</p> -->
            </div>
            <div class="about-buttons">
              <div class="field is-grouped is-grouped-centered">
                <p class="control">
                  <a
                    v-on:click="warpGithub"
                    class="button is-neon-cyan is-medium"
                  >
                    <span class="icon">
                      <font-awesome-icon :icon="['fab', 'github']" />
                      <!-- <i class="fab fa-github"></i> -->
                    </span>
                    <span>Github</span>
                  </a>
                </p>
                <!-- <p class="control">
                  <a v-on:click="warpDonate" class="button is-neon-cyan is-medium">
                    <span class="icon">
                      <i class="fas fa-heart"></i>
                    </span>
                    <span>Donate</span>
                  </a>
                </p> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ipcRenderer, shell } from "electron";
import { tridentEngine } from "../modules/streams/trident_engine.js";
import logo from '../assets/imgs/TridentFrame_logo_512x512.png';

export default {
  data: function () {
    return {
      logo: logo,
      settings_tab_selection: 0,
      USER_SETTINGS: {},
      USER_SETTINGS_PREVIOUS: {},
    };
  },
  methods: {
    refreshWindow() {
      ipcRenderer.invoke("reload-window");
    },
    openInspector() {
      ipcRenderer.invoke("open-inspector");
    },
    btnGetSettings() {
      console.log("Settings in panel");
      console.log(this.USER_SETTINGS);
      console.log("Settings in store");
      console.log(ipcRenderer.sendSync("get-settings"));
    },
    btnSaveSettings() {
      ipcRenderer.sendSync("set-user-settings", this.USER_SETTINGS);
    },
    btnRelaunchApp() {
      ipcRenderer.invoke("relaunch-application");
    },
    warpGithub() {
      shell.openExternal("https://github.com/StahlFerro/TridentFrame");
    },
    warpDonate() {
      shell.openExternal("https://en.liberapay.com/StahlFerro");
    },
    applySettingsWatcher() {
      this.$watch("USER_SETTINGS", function() {
        ipcRenderer.sendSync("set-user-settings", this.USER_SETTINGS);
      }, { deep: true});
    },
    ipcWindow: function () {
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
      console.log("before invoke");
      ipcRenderer.invoke("open-dialog", options).then((result) => {
        tridentEngine(["inspect_one", result.filePaths[0]], (error, res) => {
          console.log(res);
        });
      });
      console.log("after invoke here");
    },
  },
  // watch: {
  //   USER_SETTINGS: {
  //     handler: function (val) {
  //       // console.log("old:");
  //       // console.log(this.USER_SETTINGS_PREVIOUS);
  //       // console.log("new:");
  //       // console.log(val);
  //       // ipcRenderer.sendSync("set-settings", this.USER_SETTINGS);
  //     },
  //     deep: true,
  //   },
  // },
  mounted: function () {
    // ipcRenderer.invoke('reload-window-once');
    const SETTINGS = ipcRenderer.sendSync("get-settings");
    this.USER_SETTINGS = { ...SETTINGS.user };
    this.USER_SETTINGS_PREVIOUS = { ...SETTINGS.user };
    this.applySettingsWatcher();
  },
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
