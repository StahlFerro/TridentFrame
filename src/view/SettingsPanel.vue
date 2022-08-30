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
            <div class="field is-enhanced selection">
              <!-- <div class="field-body"> -->
              <label
                title="How the name of the preview image will be saved as"
              >Save name</label>
              <div class="controls-container">
                <div class="control main">
                  <div class="select is-neon-cyan">
                    <select id="nameSaveBehaviourSelection" v-model="APP_SETTINGS.preview_image.name_save_behaviour">
                      <option v-for="(sb, index) in previewImageSaveNameBehaviours" :key="index" :value="sb.name" :title="sb.description">
                        {{ sb.label }}
                      </option>
                      <!-- <option value="GIF">GIF</option>
                      <option value="PNG">APNG</option> -->
                    </select>
                  </div>
                </div>
              </div>
              <!-- </div> -->
            </div>
          </div>
          
          <div id="settings_empty_001" class="settings-group" />


          
          <div id="settings_directories" class="settings-group is-2">
            <h4 class="title is-4 settings-header">
              Default output folders
            </h4>
            <hr />
            <div class="field is-enhanced textbox">
              <label title="The time needed to move to the next frame">Create AIMG</label>
              <div class="controls-container">
                <div class="control">
                  <a class="button square-button is-neon-cyan" @click="btnSetOutDir('create_panel')">
                    <span class="icon is-small">
                      <font-awesome-icon icon="folder-open" />
                    </span>
                    <span>Choose</span>
                  </a>
                </div>
                <div class="control main">
                  <input
                    v-model="intermediate.directories.default_out_dir.create_panel"
                    class="input is-neon-white"
                    type="text"
                    @blur="blurCommitDefaultOutDir($event, 'create_panel')"
                  />
                </div>
              </div>
              <div class="stat-icon">
                <span v-if="errors.defaultOutDirCreate" class="icon is-crimson" title="The directory does not exist, and will not be used as a default">
                  <font-awesome-icon icon="circle-exclamation" size="lg" />
                </span>
              </div>
            </div>
            <div class="field is-enhanced textbox">
              <label title="The time needed to move to the next frame">Split AIMG</label>
              <div class="controls-container">
                <div class="control">
                  <a class="button square-button is-neon-cyan" @click="btnSetOutDir('split_panel')">
                    <span class="icon is-small">
                      <font-awesome-icon icon="folder-open" />
                    </span>
                    <span>Choose</span>
                  </a>
                </div>
                <div class="control main">
                  <input
                    v-model="intermediate.directories.default_out_dir.split_panel"
                    class="input is-neon-white"
                    type="text"
                    @blur="blurCommitDefaultOutDir($event, 'split_panel')"
                  />
                </div>
              </div>
              <div class="stat-icon">
                <span v-if="errors.defaultOutDirSplit" class="icon is-crimson" title="The directory does not exist, and will not be used as a default">
                  <font-awesome-icon icon="circle-exclamation" size="lg" />
                </span>
              </div>
            </div>
            <div class="field is-enhanced textbox">
              <label title="The time needed to move to the next frame">Modify AIMG</label>
              <div class="controls-container">
                <div class="control">
                  <a class="button square-button is-neon-cyan" @click="btnSetOutDir('modify_panel')">
                    <span class="icon is-small">
                      <font-awesome-icon icon="folder-open" />
                    </span>
                    <span>Choose</span>
                  </a>
                </div>
                <div class="control main">
                  <input
                    v-model="intermediate.directories.default_out_dir.modify_panel"
                    class="input is-neon-white"
                    type="text"
                    @blur="blurCommitDefaultOutDir($event, 'modify_panel')"
                  />
                </div>
              </div>
              <div class="stat-icon">
                <span v-if="errors.defaultOutDirModify" class="icon is-crimson" title="The directory does not exist, and will not be used as a default">
                  <font-awesome-icon icon="circle-exclamation" size="lg" />
                </span>
              </div>
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
import { access } from "fs";
import { tridentEngine } from "../modules/streams/trident_engine.js";
import { PreviewImageSaveNameBehaviour } from "../models/previewImage.js";
import logo from '../assets/imgs/TridentFrame_logo_512x512.png';

const DIR_DIALOG_PROPS = ["openDirectory", "createDirectory"];

export default {
  data: function () {
    return {
      logo: logo,
      settings_tab_selection: 0,
      previewImageSaveNameBehaviours: PreviewImageSaveNameBehaviour.getAll(),
      APP_SETTINGS: {},
      APP_SETTINGS_PREVIOUS: {},
      errors: {
        defaultOutDirCreate: false,
        defaultOutDirSplit: false,
        defaultOutDirModify: false,
      },
      intermediate: {
        directories: {
          default_out_dir: {
            create_panel: "",
            split_panel: "",
            modify_panel: "",
          }
        }
      }
    };
  },
  computed: {
    computedAppSettings: function() {
      return Object.assign({}, this.APP_SETTINGS)
    },
    // defaultOutDirCreateValid: function() {
    //   return this.APP_SETTINGS.directories.default_out_dir.create_panel
    // },
    // defaultOutDirSplitValid: function() {
    //   return this.APP_SETTINGS.directories.default_out_dir.split_panel
    // },
    // defaultOutDirModifyValid: function() {
    //   return this.APP_SETTINGS.directories.default_out_dir.modify_panel
    // }
  },
  watch: {
    'intermediate.directories.default_out_dir.create_panel': {
      handler: function (val) {
        console.log(val);
      },
    },
  },
  beforeMount: function () {
    console.debug("SettingsPanel beforeMounting...");
    console.log(PreviewImageSaveNameBehaviour.getAll())
    Object.keys(PreviewImageSaveNameBehaviour).forEach(saveBehaviour => console.log("saveBehaviour:", saveBehaviour));
    // ipcRenderer.invoke('reload-window-once');
    const SETTINGS = ipcRenderer.sendSync("IPC-GET-SETTINGS");
    console.debug(SETTINGS);
    this.APP_SETTINGS = { ...SETTINGS };
    this.APP_SETTINGS_PREVIOUS = { ...SETTINGS };
  },
  mounted: function() {
    console.debug("SettingsPanel mounted");
    this.mapIntermediateProperties();
    this.applySettingsWatcher();
  },
  methods: {
    mapIntermediateProperties() {
      console.log('mapIntermediateProperties');
      this.intermediate.directories.default_out_dir.create_panel = this.APP_SETTINGS.directories.default_out_dir.create_panel
      this.intermediate.directories.default_out_dir.split_panel = this.APP_SETTINGS.directories.default_out_dir.split_panel;
      this.intermediate.directories.default_out_dir.modify_panel = this.APP_SETTINGS.directories.default_out_dir.modify_panel;
    },
    refreshWindow() {
      ipcRenderer.invoke("reload-window");
    },
    openInspector() {
      ipcRenderer.invoke("open-inspector");
    },
    btnSetOutDir(panel) {
      this.setOutDirAsync(panel);
    },
    async setOutDirAsync(target) {
      let options = { properties: DIR_DIALOG_PROPS };
      let dirPath;
      const result = await ipcRenderer.invoke('open-dialog', options);
      if (result.canceled) {
        return {canceled: true, result: dirPath};
      }
      let out_dirs = result.filePaths;
      console.log(out_dirs);
      if (out_dirs && out_dirs.length > 0) {
        dirPath = out_dirs[0];
      }
      if (target == 'create_panel') {
        this.intermediate.directories.default_out_dir.create_panel = dirPath;
      }
      else if (target == 'split_panel') {
        this.intermediate.directories.default_out_dir.split_panel = dirPath;
      }
      else if (target == 'modify_panel') {
        this.intermediate.directories.default_out_dir.modify_panel = dirPath;
      }
      this.commitDefaultOutDir(target);
      return {canceled: false, result: dirPath};
    },
    blurCommitDefaultOutDir(e, target) {
      console.log(`blurCommitDefaultOutDir for ${target}`);
      console.log(target);
      this.commitDefaultOutDir(target);
    },
    commitDefaultOutDir(target) {
      if (target == 'create_panel') {
        const dir = this.intermediate.directories.default_out_dir.create_panel;
        access(dir, (error) => {
          console.log(`error: ${error}`);
          if (dir && error) {
            this.errors.defaultOutDirCreate = true;
          }
          else {
            this.errors.defaultOutDirCreate = false;
            this.APP_SETTINGS.directories.default_out_dir.create_panel = this.intermediate.directories.default_out_dir.create_panel;
          }
        });
      }
      else if (target == 'split_panel') {
        const dir = this.intermediate.directories.default_out_dir.split_panel;
        access(dir, (error) => {
          if (dir && error) {
            this.errors.defaultOutDirSplit = true;
          }
          else {
            this.errors.defaultOutDirSplit = false;
            this.APP_SETTINGS.directories.default_out_dir.split_panel = this.intermediate.directories.default_out_dir.split_panel;
          }
        });
      }
      else if (target == 'modify_panel') {
        const dir = this.intermediate.directories.default_out_dir.modify_panel;
        access(dir, (error) => {
          if (dir && error) {
            this.errors.defaultOutDirModify = true;
          }
          else {
            this.errors.defaultOutDirModify = false;
            this.APP_SETTINGS.directories.default_out_dir.modify_panel = this.intermediate.directories.default_out_dir.modify_panel;
          }
        });
      }
    },
    btnGetSettings() {
      console.log("Settings in panel");
      console.log(this.APP_SETTINGS);
      console.log("Settings in store");
      console.log(ipcRenderer.sendSync("IPC-GET-SETTINGS"));
    },
    btnSaveSettings() {
      ipcRenderer.sendSync("IPC-SET-SETTINGS", this.APP_SETTINGS);
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
      this.$watch("computedAppSettings", (newVal, oldVal) => {
        console.debug(this.APP_SETTINGS);
        console.debug("newVal");
        console.debug(newVal);
        console.debug("oldVal");
        console.debug(oldVal);
        // Need to convert Vue proxy objects to plain object so that ipc can transmit the object
        let new_settings = JSON.parse(JSON.stringify(this.APP_SETTINGS));
        console.debug(new_settings);
        ipcRenderer.sendSync("IPC-SET-SETTINGS", new_settings);
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
