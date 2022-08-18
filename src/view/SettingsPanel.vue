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
          v-show="settings_tab_selection == 0"
          class="settings-subpanel-general"
        >
          <div id="settings_startup" class="settings-group">
            <h4 class="title is-4 settings-header">
              On startup
            </h4>
            <hr />
            <div class="field">
              <input id="fullscreenCheckbox" v-model="APP_SETTINGS.startup.fullscreen" class="is-checkradio is-white" type="checkbox" />
              <label for="fullscreenCheckbox">Start in fullscreen</label>
            </div>
            <div class="field">
              <input id="openDebuggerCheckbox" v-model="APP_SETTINGS.startup.open_devtools" class="is-checkradio is-white" type="checkbox" />
              <label for="openDebuggerCheckbox">Open developer tools</label>
            </div>
          </div>
          
          <div id="settings_image_preview" class="settings-group">
            <h4 class="title is-4 settings-header">
              Image previewing
            </h4>
            <hr />
            <div class="field is-horizontal-midlined">
              <!-- <div class="field-body"> -->
              <label
                title="How the name of the preview image will be saved as"
              >Save name</label>
              <div class="control">
                <div class="select is-neon-cyan">
                  <select id="nameSaveBehaviourSelection" v-model="APP_SETTINGS.preview_image.name_save_behaviour">
                    <option v-for="(sb, index) in previewImageSaveNameBehaviour" :key="index" :value="sb.name" :title="sb.description">
                      {{ sb.label }}
                    </option>
                    <!-- <option value="GIF">GIF</option>
                    <option value="PNG">APNG</option> -->
                  </select>
                </div>
              </div>
              <!-- </div> -->
            </div>
          </div>
        </div>

        <div
          v-show="settings_tab_selection == 1"
          class="settings-subpanel-window"
        >
          <table class="table is-borderless" style="padding: 5px" width="100%">
            <tr>
              <td>
                <a
                  class="button is-large is-neon-cyan"
                  @click="refreshWindow"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="redo-alt" />
                  </span>
                  <span>Reload Window</span>
                </a>
              </td>
              <td>
                <a
                  class="button is-large is-neon-white"
                  @click="openInspector"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="bug" />
                    <!-- <i class="fas fa-bug"></i> -->
                  </span>
                  <span>Open Developer Tools</span>
                </a>
              </td>
            </tr>
            <tr>
              <td>
                <a
                  class="button is-large is-neon-sunset"
                  @click="btnRelaunchApp"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="power-off" />
                  </span>
                  <span>Relaunch App</span>
                </a>
              </td>
              <!-- <td>
                <a
                  class="button is-large is-neon-crimson"
                  @click="testCInterface"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="flask" />
                  </span>
                  <span>Call CF</span>
                </a>
              </td> -->
            </tr>
          </table>
        </div>

        <div
          v-show="settings_tab_selection == 2"
          class="settings-subpanel-about"
        >
          <div class="about-content">
            <div class="about-logo">
              <img :src="logo" class="about-logo no-select-drag" />
            </div>
            <div class="about-info">
              <h1 class="about-software-name">
                TridentFrame
              </h1>
              <p class="about-software-version">
                v0.1.0-beta.12
              </p>
              <p class="about-software-copyright">
                Author: StahlFerro
                <!-- <span class="icon">
                  <font-awesome-icon :icon="['far', 'copyright']" />
                </span> -->
              </p>
              <p class="about-software-license">
                TridentFrame is free software licensed under the GNU General Public License
                <!-- <span class="icon">
                  <font-awesome-icon :icon="['far', 'copyright']" />
                </span> -->
              </p>
              <!-- <p class="about-software-author">Developed by StahlFerro</p> -->
            </div>
            <div class="about-buttons">
              <div class="field is-grouped is-grouped-centered">
                <p class="control">
                  <a
                    class="button is-neon-cyan is-medium"
                    @click="warpGithub"
                  >
                    <span class="icon">
                      <font-awesome-icon :icon="['fab', 'github']" />
                      <!-- <i class="fab fa-github"></i> -->
                    </span>
                    <span>Github</span>
                  </a>
                </p>
                <p class="control">
                  <a class="button is-neon-cyan is-medium" @click="warpLicense">
                    <span class="icon">
                      <font-awesome-icon icon="globe" />
                    </span>
                    <span>License</span>
                  </a>
                </p>
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
import { PreviewImageSaveNameBehaviour } from "../models/previewImage.js";
import logo from '../assets/imgs/TridentFrame_logo_512x512.png';

export default {
  data: function () {
    return {
      logo: logo,
      settings_tab_selection: 0,
      previewImageSaveNameBehaviour: PreviewImageSaveNameBehaviour.getAll(),
      APP_SETTINGS: {},
      APP_SETTINGS_PREVIOUS: {},
    };
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
  beforeMount: function () {
    console.debug("SettingsPanel mounted");
    console.log(PreviewImageSaveNameBehaviour.getAll())
    Object.keys(PreviewImageSaveNameBehaviour).forEach(saveBehaviour => console.log("saveBehaviour:", saveBehaviour));
    // ipcRenderer.invoke('reload-window-once');
    const SETTINGS = ipcRenderer.sendSync("get-settings");
    console.debug(SETTINGS);
    this.APP_SETTINGS = { ...SETTINGS };
    this.APP_SETTINGS_PREVIOUS = { ...SETTINGS };
    this.applySettingsWatcher();
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
      console.log(this.APP_SETTINGS);
      console.log("Settings in store");
      console.log(ipcRenderer.sendSync("get-settings"));
    },
    btnSaveSettings() {
      ipcRenderer.sendSync("set-settings", this.APP_SETTINGS);
    },
    btnRelaunchApp() {
      ipcRenderer.invoke("relaunch-application");
    },
    warpGithub() {
      shell.openExternal("https://github.com/StahlFerro/TridentFrame");
    },
    warpLicense() {
      shell.openExternal("https://www.gnu.org/licenses/gpl-3.0.en.html");
    },
    warpDonate() {
      shell.openExternal("https://en.liberapay.com/StahlFerro");
    },
    applySettingsWatcher() {
      this.$watch("APP_SETTINGS", function() {
        console.debug(this.APP_SETTINGS);
        // Need to convert Vue proxy objects to plain object so that ipc can transmit the object
        let new_settings = JSON.parse(JSON.stringify(this.APP_SETTINGS));
        console.debug(new_settings);
        ipcRenderer.sendSync("set-settings", new_settings);
      }, { deep: true});
    },
    testCInterface() {
      tridentEngine(["ping_c_interface"], (error, res) => {
        if (error) {
          console.error(error);
        }
        else {
          console.debug(res);
        }
      });
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
