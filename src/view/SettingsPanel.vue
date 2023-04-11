<template>
  <div id="settings_panel" style="display: none">
    <div class="settings-panel-root">
      <div class="settings-tab">
        <div class="tabs">
          <ul>
            <li :class="{ 'is-active': settingsTabSelection == 0 }">
              <a @click="settingsTabSelection = 0">General</a>
            </li>
            <li :class="{ 'is-active': settingsTabSelection == 1 }">
              <a @click="settingsTabSelection = 1">Presets</a>
            </li>
            <!-- <li :class="{ 'is-active': settingsTabSelection == 2 }">
              <a @click="settingsTabSelection = 2">Languages</a>
            </li> -->
            <li :class="{ 'is-active': settingsTabSelection == 2 }">
              <a @click="settingsTabSelection = 2">Backup</a>
            </li>
            <li :class="{ 'is-active': settingsTabSelection == 3 }">
              <a @click="settingsTabSelection = 3">Window</a>
            </li>
            <li :class="{ 'is-active': settingsTabSelection == 4 }">
              <a @click="settingsTabSelection = 4">About</a>
            </li>
          </ul>
        </div>
      </div>
      <div class="settings-subpanels">
        <div v-show="settingsTabSelection == 0" class="settings-subpanel-general">
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
            
            <ButtonInputField label="Create AIMG" 
                              error-message="The directory does not exist, and will not be used as a default"
                              :use-icons="true" :has-error="errors.defaultOutDirCreate"
            >
              <template #buttonControl>
                <ButtonField label="Choose" color="blue" :is-square="true" :icons="['fas', 'folder-open']"
                             @click="btnSetOutDir('create_panel')"
                />
              </template>
              <template #inputControl>
                <InputField v-model="intermediate.directories.default_out_dir.create_panel"
                            type="text" @blur="blurCommitDefaultOutDir($event, 'create_panel')"
                />
              </template>
            </ButtonInputField>

            <ButtonInputField label="Split AIMG" 
                              error-message="The directory does not exist, and will not be used as a default"
                              :use-icons="true" :has-error="errors.defaultOutDirSplit"
            >
              <template #buttonControl>
                <ButtonField label="Choose" color="blue" :is-square="true" :icons="['fas', 'folder-open']"
                             @click="btnSetOutDir('split_panel')"
                />
              </template>
              <template #inputControl>
                <InputField v-model="intermediate.directories.default_out_dir.split_panel"
                            type="text" @blur="blurCommitDefaultOutDir($event, 'split_panel')"
                />
              </template>
            </ButtonInputField>

            <ButtonInputField label="Modify AIMG" 
                              error-message="The directory does not exist, and will not be used as a default"
                              :use-icons="true" :has-error="errors.defaultOutDirModify"
            >
              <template #buttonControl>
                <ButtonField label="Choose" color="blue" :is-square="true" :icons="['fas', 'folder-open']"
                             @click="btnSetOutDir('modify_panel')"
                />
              </template>
              <template #inputControl>
                <InputField v-model="intermediate.directories.default_out_dir.modify_panel"
                            type="text" @blur="blurCommitDefaultOutDir($event, 'modify_panel')"
                />
              </template>
            </ButtonInputField>
          </div>
          <div id="settings_empty_001" class="settings-group" />

          <div id="settings_locale" class="settings-group">
            <h4 class="title is-4 settings-header">
              Language
            </h4>
            <hr />
            <DropdownField v-model="$i18n.locale" :options-list="LOCALES_LIST" />
          </div>
        </div>

        <div v-show="settingsTabSelection == 1" class="settings-subpanel-presets">
          <div class="settings-preset-selector">
            <KeyValueTable :rows="localPresetsList" value-header="Preset">
              <template #rowControlsHeaderRight>
                <th>
                  Type
                </th>
                <!-- <th>
                  Created at
                </th> -->
                <th>
                  Last modifed at
                </th>
                <th class="kvp-control-fit">
                  Controls
                </th>
              </template>
              <template #dataRow="presetRow">
                <td class="clickable is-paddingless is-marginless">
                  <div :id="`PresetRowId-${presetRow.id}`" :class="{'is-selected': presetSelectionId == presetRow.id}" @click="viewPreset(presetRow.id)">
                    {{ presetRow.name }}
                  </div>
                </td>
                <td class="is-paddingless is-marginless kvp-control-fit">
                  {{ presetRow.typeName }}
                </td>
                <!-- <td>
                  {{ formatUnixTimestamp(presetRow.createdDateTime) }}
                </td> -->
                <td class="kvp-control-fit">
                  {{ formatUnixTimestamp(presetRow.lastModifiedDateTime) }}
                </td>
              </template>
              <template #rowControlsRight="presetRow">
                <td class="center">
                  <ButtonField color="red" size="small" :icons="['fas', 'trash-can']" @click="deletePresetAsync(presetRow.id)" />
                </td>
              </template>
            </KeyValueTable>
          </div>
          <div class="settings-preset-key-values">
            <KeyValueTable :rows="selectedPresetAttributes" key-header="Attribute" value-header="Value">
              <template #dataRow="attr">
                <td>
                  <p>
                    {{ attr.label }}
                  </p>
                </td>
                <td>
                  <p>
                    {{ attr.value }}
                  </p>
                </td>
              </template>
            </KeyValueTable>
          </div>
          <div class="settings-preset-controls">
            
          </div>
        </div>

        <div v-show="settingsTabSelection == 2" class="settings-subpanel-backup">
          <div class="settings-backup-view">
            <KeyValueTable :rows="appStats" data-type="object" key-header="Statistics" value-header="Value">
              <template #dataRow="presetRow">
                <td class="is-paddingless is-marginless kvp-control-fit">
                  {{ presetRow.name }}
                </td>
                <td>
                  {{ presetRow.value }}
                </td>
              </template>
            </KeyValueTable>
          </div>
          <div class="settings-backup-control">
            <ButtonField @click="createBackup" label="Create Backup" />
            <!-- <ButtonField @click="restoreBackup" label="Restore Backup" /> -->
          </div>
          <div class="settings-backup-footer">
            <StatusBar :status-bar-id="statusBarId" />
          </div>
        </div>

        <div v-show="settingsTabSelection == 3" class="settings-subpanel-window">
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

        <div v-show="settingsTabSelection == 4" class="settings-subpanel-about">
          <div class="about-content">
            <div class="about-logo">
              <img :src="logo" class="about-logo no-select-drag" />
            </div>
            <div class="about-info">
              <h1 class="about-software-name">
                TridentFrame
              </h1>
              <p class="about-software-version">
                v0.1.0-beta.13
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
                  <ButtonField label="Github" color="white" size="medium" :hint="externalLinks.github"
                               :icons="['fab', 'github']"
                               @click="warpGithub"
                  />
                </p>
                <p class="control">
                  <ButtonField label="Website" color="cyan" size="medium" :hint="externalLinks.authorWebsite"
                               :icons="['fas', 'globe']"
                               @click="warpAuthorWebsite"
                  />
                </p>
                <p class="control">
                  <ButtonField label="License" color="orange" size="medium" :hint="externalLinks.license"
                               :icons="['fas', 'scale-balanced']"
                               @click="warpLicense"
                  />
                </p>
                <p class="control">
                  <ButtonField label="Buy me a coffee" color="green" size="medium" :hint="externalLinks.kofi"
                               :icons="['fas', 'mug-hot']"
                               @click="warpDonate"
                  />
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
import { access, writeFile } from "fs";
import { tridentEngine } from "../modules/streams/trident_engine.js";
import { PreviewImageSaveNameBehaviour } from "../models/previewImage.js";
import logo from '../assets/imgs/TridentFrame_logo_512x512.png';
import StatusBar from "./components/StatusBar.vue";

import InputField from "./components/Form/InputField.vue";
import ButtonField from "./components/Form/ButtonField.vue";
import ButtonInputField from "./components/Form/ButtonInputField.vue";
import DropdownField from "./components/Form/DropdownField.vue";
import KeyValueTable from "./components/Displays/KeyValueTable.vue";
import { Preset, PresetType } from "../models/presets";
import { ApplicationBackup } from "../models/applicationBackup";
import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";

import dayjs from "dayjs";
import { join } from "path";

const DIR_DIALOG_PROPS = ["openDirectory", "createDirectory"];
const LOCALES_LIST = [
  {
    name: "en",
    label: "English",
    description: "",
  }
];

export default {
  components: {
    InputField,
    ButtonField,
    ButtonInputField,
    DropdownField,
    KeyValueTable,
    StatusBar,
  },
  props: {
    presets: {
      type: Object,
      default() {
        return {}
      },
      required: false,
    }
  },
  data: function () {
    return {
      logo: logo,
      settingsTabSelection: 0,
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
      },
      LOCALES_LIST: LOCALES_LIST,
      localPresetsList: [],
      appStats: {},
      presetSelectionId: "",
      selectedPresetAttributes: [],
      statusBarId: "settingsBackupSubpanelStatusBar",
      externalLinks: {
        github: "https://github.com/StahlFerro/TridentFrame",
        authorWebsite: "https://stahlferro.pages.dev",
        license: "https://www.gnu.org/licenses/gpl-3.0.en.html",
        kofi: "https://ko-fi.com/StahlFerro",
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
    computeModifiedPresets() {
      console.log('computeModifiedPresets triggered');
      const modifiedDateTimes = Object.entries(this.presets).map(([k, v]) => v.lastModifiedDateTime);
      return modifiedDateTimes
    },
    computeApplicationStatistics() {
      console.log(`computeApplicationStatistics ${Object.keys(this.APP_SETTINGS).length}`);
      if (!this.APP_SETTINGS || Object.keys(this.APP_SETTINGS).length == 0){
        console.log(`computeApplicationStatistics is null`);
        return null;
      }
      const presetCount = this.localPresetsList.length;
      const lastBkTimeText = this.APP_SETTINGS.statistics.last_backup? this.formatUnixTimestamp(this.APP_SETTINGS.statistics.last_backup) : 'Never';
      // console.log('dateText');
      // console.log(dateText);
      const stats = {
        "presetsCount": {
          name: "Presets Count",
          value: presetCount,
        },
        "lastBackupTime": {
          name: "Last backup time",
          value: lastBkTimeText,
        },
      };
      console.log(this.APP_SETTINGS);
      return stats;
    }
  },
  watch: {
    'computeApplicationStatistics': {
      handler: function(val) {
        console.log(`watch computeApplicationStatistics`);
        console.log({val});
        this.appStats = val;
      }
    },
    'intermediate.directories.default_out_dir.create_panel': {
      handler: function (val) {
        console.log(val);
      },
    },
    'computeModifiedPresets': {
      // When this property is updated, refresh the preset selector values
      handler: function(newVal, oldVal) {
        console.debug(`Preset updated\nOld/New count: ${oldVal}/${newVal}`);
        const presetCount = this.populatePresetsListTable();
        if (presetCount == 0) {
          this.presetSelectionId = "";
        }
        // If there is a preset already selected to preview the attributes, attempt to reload the attributes table in case an update is made to that particular preset.
        if (this.presetSelectionId) {
          const preset = this.viewPreset(this.presetSelectionId);
          // If preset is deleted, deselect the selection and clear the attributes table
          if (!preset) {
            this.presetSelectionId = "";
            this.selectedPresetAttributes = [];
          }
        }
      },
    }
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
    // this.applyStatisticsCompute();
    console.log(this.$i18n.locale);
    console.log(this.$i18n.availableLocales);
    const loadedPresets = this.populatePresetsListTable();
    if (loadedPresets > 0) {
      this.viewPreset(this.localPresetsList[0].id);
    }
  },
  methods: {
    formatUnixTimestamp(unixTimestamp, mode="generic") {
      try {
        const date = dayjs(unixTimestamp);
        if (!date.isValid())
          throw Error(date);
        // console.log(`date try`);
        // console.log(date);
        if (mode == "generic")
          return date.format('YYYY-MM-DD HH:mm:ss');
        else if (mode == "filename")
          return date.format('YYYY-MM-DD-HH.mm.ss');
      }
      catch (error) {
        console.error(error);
        return "";
      }
    },
    createBackup() {
      (async () => {
        const presets = ipcRenderer.sendSync("IPC-GET-PRESETS");
        console.log('backing up preset yields...');
        console.log(presets);
        const settings = ipcRenderer.sendSync("IPC-GET-SETTINGS");
        let dialogOptions = { properties: ["openDirectory", "createDirectory"] };
        const result = await ipcRenderer.invoke('open-dialog', dialogOptions);
        if (result.canceled)
          return Promise.reject("Directory selection cancelled");
        else{
          let outDirs = result.filePaths;
          if (outDirs && outDirs.length > 0) { 
            return {
              outDirs: outDirs, 
              backup: new ApplicationBackup("0.1.0-beta.13", settings, presets)
            };
          }
          else {
            return Promise.reject("No directories are selected")
          }
        }
      })()
      .then(async (res) => {
        console.log('createBackup res');
        const dir = res.outDirs[0];
        const backup =  res.backup;
        const bkTime = backup.createdDateTime;
        this.APP_SETTINGS.statistics.last_backup = bkTime;
        console.log('create Backup res');
        console.log(res);
        const bkFileName = `tridentframe_userdata_backup_${this.formatUnixTimestamp(bkTime, "filename")}.json`
        const filePath = join(dir, bkFileName);
        const serializedBackup = JSON.stringify(backup, null, 4)
        return new Promise(function(resolve, reject) {
          writeFile(filePath, serializedBackup, 'utf-8', function(err) {
            if (err) reject(err);
            else resolve(filePath);
          });
        });
      })
      .then((res) => {
        this._logSuccess(`Backup written to ${res}`);
      })
      .catch((error) => {
        console.error(error);
      });
    },
    restoreBackup() {
      
    },
    populatePresetsListTable() {
      // console.log('populatePresetsSelector');
      // console.log(this.presets);
      const presets = JSON.parse(JSON.stringify(this.presets));
      console.log(presets);
      this.localPresetsList = [];
      for (const [id, preset] of Object.entries(this.presets)) {
        this.localPresetsList.push({
          id: id,
          name: preset.name,
          typeName: PresetType.fromName(preset.presetType.name).label,
          createdDateTime: preset.createdDateTime,
          lastModifiedDateTime: preset.lastModifiedDateTime,
        })
      }
      return this.localPresetsList.length;
    },
    populatePresetAttributeTable(preset) {
      this.selectedPresetAttributes = [];
      for (const [k, v] of Object.entries(preset.presetObject)) {
        this.selectedPresetAttributes.push({
          key: k,
          label: this.$i18n.t(`criterion.${k}`),
          value: v
        });
      }
    },
    getPresetTypeLabel(presetTypeName) {
      return PresetType.fromName(presetTypeName).label;
    },
    viewPreset(presetId) {
      this.presetSelectionId = presetId;
      console.log(presetId);
      const presetJson = this.presets[presetId];
      if (presetJson) {
        const preset = Preset.fromJSON(presetJson);
        console.log(this.presets);
        console.log(preset.presetObject);
        this.populatePresetAttributeTable(preset);
        return preset;
      }
      else {
        return null;
      }
    },
    async deletePresetAsync(id) {      
      if (id) {
        console.log(id);
        const presetJson = this.presets[id];
        let options = {
          title: "TridentFrame Preset Deletion",
          buttons: ["Yes", "No"],
          message:
            `Are you sure you want to delete the preset '${presetJson.name}'?`,
        };
        const promptResult = await ipcRenderer.invoke("IPC-SHOW-MESSAGE-BOX", options);
        console.log(`msgbox promptResult:`);
        console.log(promptResult);
        if (promptResult.response == 0) {
          this.emitter.emit('delete-preset', id);
          // this._logInfo(`Deleted preset ${presetJson.name}`);
        }
      }
      else this._logWarning(`Please select a preset from the dropdown to delete!`);
    },
    mapIntermediateProperties() {
      console.log('mapIntermediateProperties');
      this.intermediate.directories.default_out_dir.create_panel = this.APP_SETTINGS.directories.default_out_dir.create_panel
      this.intermediate.directories.default_out_dir.split_panel = this.APP_SETTINGS.directories.default_out_dir.split_panel;
      this.intermediate.directories.default_out_dir.modify_panel = this.APP_SETTINGS.directories.default_out_dir.modify_panel;
    },
    refreshWindow() {
      ipcRenderer.send("IPC-RELOAD-WINDOW-SYNC");
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
      shell.openExternal(this.externalLinks.github);
    },
    warpAuthorWebsite() {
      shell.openExternal(this.externalLinks.authorWebsite);
    },
    warpLicense() {
      shell.openExternal(this.externalLinks.license);
    },
    warpDonate() {
      shell.openExternal(this.externalLinks.kofi);
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
    _logClear() {
      logStatus(this.statusBarId, EnumStatusLogLevel.CLEAR, null);
    },
    _logInfo(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.INFO, message);
    },
    _logProcessing(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.PROCESSING, message);
    },
    _logSuccess(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.SUCCESS, message);
    },
    _logWarning(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.WARNING, message);
    },
    _logError(message) {
      logStatus(this.statusBarId, EnumStatusLogLevel.ERROR, message);
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
