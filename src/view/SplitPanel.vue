<template>
  <div id="split_panel">
    <div class="split-panel-root">
      <div class="split-panel-display">
        <div
          class="split-panel-image silver-bordered"
          :class="{ 'has-checkerboard-bg': checkerbg_active }"
        >
          <img :src="escapeLocalPath(previewPathCB)" />
        </div>
        <div class="split-panel-info silver-bordered-no-left">
          <table class="table spl-info-table" width="100%">
            <thead>
              <tr>
                <th colspan="2">
                  <p class="is-white-d">
                    {{ info_header }}
                  </p>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="spl-info-label is-cyan">Name</td>
                <td class="spl-info-data">
                  <span v-if="name">{{ name }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Dimensions</td>
                <td class="spl-info-data">
                  <span v-if="dimensions">{{ dimensions }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">File Size</td>
                <td class="spl-info-data">
                  <span v-if="file_size">{{ file_size_hr }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Has Transparency</td>
                <td class="spl-info-data">
                  <span v-if="has_transparency">{{
                    has_transparency ? "Yes" : "No"
                  }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Total frames</td>
                <td class="spl-info-data">
                  <span v-if="frame_count">{{ frame_count }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <!-- <tr>
                <td class="spl-info-label is-cyan">Total frames (DS)</td>
                <td class="spl-info-data">
                  <span v-if="frame_count_ds">{{ frame_count_ds }}</span>
                  <span v-else>-</span>
                </td>
              </tr> -->
              <tr>
                <td class="spl-info-label is-cyan">Average delay (ms)</td>
                <td class="spl-info-data">
                  <span v-if="average_delay">{{
                    roundPrecise(average_delay, 3)
                  }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Delays are even</td>
                <td class="spl-info-data">
                  <span v-if="delays">{{
                    delays_are_even ? "Yes" : "No"
                  }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Delays</td>
                <td class="spl-info-data">
                  <span v-if="delays">{{ delays }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Frame rate (FPS)</td>
                <td class="spl-info-data">
                  <span v-if="fps">{{ fps }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Loop duration</td>
                <td class="spl-info-data">
                  <span v-if="loop_duration">{{ loop_duration }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
              </tr>
              <tr>
                <td class="spl-info-label is-cyan">Loop count</td>
                <td class="spl-info-data">
                  <template v-if="previewPath">
                    <span v-if="loop_count == 0">Infinite</span>
                    <span v-else>{{ loop_count }}</span>
                  </template>
                  <!-- <template v-else>-</template> -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="split-panel-middlebar">
        <div class="spl-control-btn">
          <a
            class="button is-neon-emerald"
            :class="{
              'is-loading': SPL_IS_LOADING,
              'non-interactive': isButtonFrozen,
            }"
            @click="loadImage"
          >
            <span class="icon is-small">
              <font-awesome-icon icon="plus" />
              <!-- <i class="fas fa-plus"></i> -->
            </span>
            <span>Load GIF/APNG</span>
          </a>
        </div>
        <div class="spl-control-btn">
          <a
            class="button is-neon-crimson"
            :class="{ 'non-interactive': isButtonFrozen }"
            @click="clearImage"
          >
            <span class="icon is-small">
              <font-awesome-icon icon="times" />
              <!-- <i class="fas fa-times"></i> -->
            </span>
            <span>Clear</span>
          </a>
        </div>
        <div class="spl-control-btn">
          <a
            class="button is-neon-white"
            :class="{ 'is-active': checkerbg_active }"
            @click="toggleCheckerBG"
          >
            <span class="icon is-medium">
              <font-awesome-icon icon="chess-board" />
              <!-- <i class="fas fa-chess-board"></i> -->
            </span>
          </a>
        </div>
      </div>
      <div class="split-panel-controls">
        <div class="spc-top">
          <div class="general-form row-5">
            <div class="field-cell">
              <InputField v-model="criteria.new_name" label="Rename sequence" type="text" hint="The new name of the sequence" />
            </div>
            <div class="field-cell">
              <InputField v-model="criteria.pad_count" label="Pad count" type="number" hint="Amount of zero-padding applied to the sequence number. Example: Pad count 4 -> 0000, 0001, 0002"
                          :constraint-option="{ handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true }}"
                          @input="widthHandler"
              />
            </div>
            <div class="field-cell">
              <CheckboxField v-model="criteria.is_unoptimized" label="Unoptimize" hint="Reconstructs the original image of each frame. Use on optimized GIFs" />
              <br />
              <CheckboxField v-model="criteria.convert_to_rgba" label="Convert to RGBA" hint="Convert each frame into a PNG with RGBA color mode" />
              <br />
              <CheckboxField v-model="criteria.extract_delay_info" label="Extract frame delays" hint="Generate a file containing the delay information of each frame" />
            </div>
            <div class="separator">
              <div class="separator-space" />
            </div>
            <div class="field-cell span-4">
              <ButtonInputField v-model="saveDir" button-label="Save to" :use-icons="false" 
                                 @control-button-click="btnSetSavePath" 
              />
            </div>
            <div class="field-cell center-h">
              <a class="button is-neon-cyan" :class="{
                   'is-loading': SPL_IS_SPLITTING,
                   'non-interactive': isButtonFrozen,
                 }"
                 @click="btnSplitImage"
              >
                Split to folder
              </a>
            </div>
          </div>

          <!-- <table width="100%">
            <tr>
              <td width="20%">
                <div class="field">
                  <label class="label">Rename sequence</label>
                  <div class="control">
                    <input
                      v-model="criteria.new_name"
                      class="input is-neon-white"
                    />
                  </div>
                </div>
              </td>
              <td width="20%">
                <div class="field">
                  <label class="label">Pad count</label>
                  <div class="control">
                    <input
                      v-model="criteria.pad_count"
                      class="input is-neon-white"
                      type="number"
                      min="0"
                      max="6"
                      @keydown="numConstrain($event, true, true)"
                    />
                  </div>
                </div>
              </td>
              <td width="20%" style="vertical-align: middle">
                <label
                  class="checkbox"
                  title="Reconstructs the original image of each frame. Use on optimized GIFs"
                >
                  <input v-model="criteria.is_unoptimized" type="checkbox" />
                  Unoptimize
                </label>
                <br />
                <label
                  class="checkbox"
                  title="Convert each frame into a PNG with RGBA color mode"
                >
                  <input v-model="criteria.convert_to_rgba" type="checkbox" />
                  Convert to RGBA
                </label>
                <br />
                <label
                  class="checkbox"
                  title="Generate a file containing the delay information of each frame"
                >
                  <input
                    v-model="criteria.extract_delay_info"
                    type="checkbox"
                  />
                  Extract frame delays
                </label>
              </td>
              <td width="20%" style="vertical-align: middle">
                <br />
              </td>
              <td width="20%" style="vertical-align: middle">
                <br />
              </td>
            </tr>
            <tr>
              <td colspan="4">
                <div class="field has-addons">
                  <div class="control">
                    <a class="button is-neon-cyan" @click="btnSetSavePath">
                      <span class="icon is-small">
                        <font-awesome-icon icon="save" />
                      </span>
                      <span>Save to</span>
                    </a>
                  </div>
                  <div class="control is-expanded">
                    <input
                      v-model="saveDir"
                      class="input is-neon-white"
                      type="text"
                      placeholder="Output folder"
                    />
                  </div>
                </div>
              </td>
              <td class="has-text-centered">
                <a
                  class="button is-neon-cyan"
                  :class="{
                    'is-loading': SPL_IS_SPLITTING,
                    'non-interactive': isButtonFrozen,
                  }"
                  @click="btnSplitImage"
                >
                  Split to folder</a
                >
              </td>
            </tr>
          </table>
           -->

        </div>
        <div class="spc-bottom">
          <StatusBar :status-bar-id="statusBarId" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ipcRenderer } from "electron";
import { roundPrecise } from "../modules/utility/calculations";
import {
  validateFilename,
  escapeLocalPath,
  getSystemForbiddenFilenameCharacters,
} from "../modules/utility/pathutils";
import { numConstrain } from "../modules/events/constraints";
import { tridentEngine } from "../modules/streams/trident_engine";

let extension_filters = [{ name: "Images", extensions: ["png", "gif"] }];
let file_dialog_props = ["openfile"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

// import Vue from 'vue';

import StatusBar from "./components/StatusBar.vue";
import InputField from "./components/Form/InputField.vue";
import CheckboxField from './components/Form/CheckboxField.vue';
import DropdownField from './components/Form/DropdownField.vue';
import ButtonInputField from './components/Form/ButtonInputField.vue';

import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";

var defaults = {
  info_header: "Information",
  name: "",
  new_name: "",
  dimensions: "",
  file_size: "",
  file_size_hr: "",
  frame_count: "",
  frame_count_ds: "",
  fps: "",
  average_delay: "",
  delays: "",
  delays_are_even: "",
  loop_duration: "",
  loop_count: "",
  has_transparency: "",
  previewPath: "",
  previewPathCB: "",
};

export default {
  components: {
    StatusBar,
    InputField,
    CheckboxField,
    DropdownField,
    ButtonInputField,
  },
  data: function () {
    return {
      info_header: "Information",
      name: "",
      criteria: {
        new_name: "",
        pad_count: "",
        color_space: "",
        is_duration_sensitive: false,
        is_unoptimized: false,
        convert_to_rgba: false,
        extract_delay_info: false,
      },
      dimensions: "",
      file_size: "",
      file_size_hr: "",
      frame_count: "",
      frame_count_ds: "",
      fps: "",
      average_delay: "",
      delays_are_even: "",
      delays: "",
      loop_duration: "",
      loop_count: "",
      has_transparency: "",
      previewPath: "",
      previewPathCB: "",
      checkerbg_active: false,
      is_reduced_color: false,
      saveDir: "",
      SPL_IS_LOADING: false,
      SPL_IS_SPLITTING: false,
      // statusBarBus: new Vue(),
      statusBarId: "splitPanelStatusBar",
    };
  },
  computed: {
    isButtonFrozen() {
      if (this.SPL_IS_LOADING || this.SPL_IS_SPLITTING) return true;
      else return false;
    },
  },
  beforeMount: function () {
    const SETTINGS = ipcRenderer.sendSync("IPC-GET-SETTINGS");
    try {
      const defaultOutDir = SETTINGS.directories.default_out_dir.split_panel;
      if (defaultOutDir) {
        this.saveDir = defaultOutDir;
      }
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    _inspectImage(imagePath) {
      this._logProcessing(`Loading image ${imagePath}`);
      tridentEngine(["inspect_one", imagePath, "animated"], (err, res) => {
        if (err) {
          if (err.error) {
            this._logError(err.error);
            this.SPL_IS_LOADING = false;
          } else if (err.warning) {
            this._logWarning(err.warning);
          }
          // mboxError(split_msgbox, error);
        } else if (res) {
          if (res && res.msg) {
            this._logProcessing(res.msg);
          } else if (res && res.data) {
            let info = res.data;
            var geninfo = info.general_info;
            var ainfo = info.animation_info;
            this.name = geninfo.name.value;
            this.dimensions = `${geninfo.width.value} x ${geninfo.height.value}`;
            this.info_header = `${geninfo.format.value} Information`;
            this.file_size = geninfo.fsize.value;
            this.file_size_hr = geninfo.fsize_hr.value;
            this.has_transparency = geninfo.has_transparency.value;
            this.frame_count = `${ainfo.frame_count.value} frames`;
            // data.frame_count_ds = `${ainfo.frame_count_ds.value} frames`
            this.fps = `${ainfo.fps.value} fps`;
            // let delay_info = `${ainfo.avg_delay.value} seconds`;
            // if (ainfo.delay_is_even.value) {
            //   delay_info += ` (even)`;
            // }
            // data.delay = delay_info;
            this.average_delay = ainfo.average_delay.value;
            this.delays_are_even = ainfo.delays_are_even.value;
            this.delays = ainfo.delays.value;
            this.loop_duration = `${ainfo.loop_duration.value} seconds`;
            this.loop_count = ainfo.loop_count.value;
            this.previewPath = geninfo.absolute_url.value;
            this.criteria.pad_count = 3;
            if (this.is_reduced_color) {
              this.criteria.color_space - 256;
            }
            this._logSuccess("Loaded image");
            this.SPL_IS_LOADING = false;
            this.previewPathCacheBreaker();
            // loadAIMG(res);
            // SPL_pad_count.value = 3;
            // if (SPL_is_reduced_color.checked) { SPL_color_space.value = 256; }
          }
        }
      });
    },
    loadImage() {
      console.log("spl load iamge");
      let options = {
        filters: extension_filters,
        properties: file_dialog_props,
      };
      ipcRenderer.invoke("open-dialog", options).then((result) => {
        let chosen_paths = result.filePaths;
        console.log(`chosen path: ${chosen_paths}`);
        if (chosen_paths === undefined || chosen_paths.length == 0) {
          console.debug("chosen path undefined/null. returning...");
          return;
        }
        this.SPL_IS_LOADING = true;
        console.log(chosen_paths);
        this._inspectImage(chosen_paths[0]);
      });
    },
    clearImage() {
      Object.assign(this, defaults);
      this._logClear();
    },
    toggleCheckerBG() {
      this.checkerbg_active = !this.checkerbg_active;
      console.log("now checkerbg is", this.checkerbg_active);
    },
    btnSetSavePath() {
      this.setSaveDirFromDialogAsync();
    },
    async setSaveDirFromDialogAsync() {
      let options = { properties: dir_dialog_props };
      let dirPath;
      const result = await ipcRenderer.invoke("open-dialog", options);
      if (result.canceled) {
        return { canceled: true, result: dirPath };
      }
      let out_dirs = result.filePaths;
      console.log(out_dirs);
      if (out_dirs && out_dirs.length > 0) {
        this.saveDir = out_dirs[0];
        dirPath = this.saveDir;
      }
      this._logClear();
      return { canceled: false, result: dirPath };
    },
    async validateFilenameAsync() {
      let nameToCheck = this.new_name ? this.new_name : this.name;
      if (validateFilename(nameToCheck)) return true;
      else return false;
    },
    btnSplitImage() {
      if (this.previewPath == "") {
        this._logError("Please load an image first!");
        return;
      }
      // else if (this.saveDir == "") {
      //   this._logError("Please specifiy an output folder first!");
      //   return;
      // }
      this.validateFilenameAsync()
        .then(async (isValid) => {
          if (isValid) {
            if (!this.saveDir) {
              const result = await this.setSaveDirFromDialogAsync();
              if (result.canceled)
                return Promise.reject("Directory selection cancelled");
              else return true;
            } else return true;
          } else {
            let errMsg = "File name contains characters that are not allowed";
            this._logError(error);
            return Promise.reject(errMsg);
          }
        })
        .then((proceed_create) => {
          console.log(`proceed create ${proceed_create}`);
          if (proceed_create) this.splitImage();
          else return;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    splitImage() {
      let new_name = this.criteria.new_name;
      if (new_name && !validateFilename(new_name)) {
        this._logError("File name contains characters that are not allowed");
        return;
      }
      this.SPL_IS_SPLITTING = true;
      // freezeButtons();
      // console.log(`in path: ${in_path} out path: ${out_path}`);
      var color_space = this.criteria.color_space;
      if (!this.is_reduced_color || color_space == "") {
        color_space = 0;
      }
      console.log(this);
      tridentEngine(
        ["split_image", this.previewPath, this.saveDir, this.criteria],
        (err, res) => {
          if (err) {
            if (err.error) {
              this._logError(err.error);
              this.SPL_IS_SPLITTING = false;
            } else if (err.warning) {
              this._logWarning(err.warning);
            }
          } else if (res) {
            if (res.msg) {
              this._logProcessing(res.msg);
            }
          }
        },
        () => {
          this._logSuccess("All frames successfully split!");
          this.SPL_IS_SPLITTING = false;
        }
      );
    },
    previewPathCacheBreaker() {
      let cb_url = this.previewPath;
      // let cb_url = `${data.previewPath}?cachebreaker=${randString()}`;
      console.log("Cache breaker url", cb_url);
      this.previewPathCB = cb_url;
    },
    _logClear() {
      logStatus(this.statusBarId, EnumStatusLogLevel.CLEAR, null);
    },
    _logMessage(message) {
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
    numConstrain: numConstrain,
    escapeLocalPath: escapeLocalPath,
    roundPrecise: roundPrecise,
  },
};
</script>
