<template>
  <div id="modify_panel">
    <div class="modify-panel-root">

      <div class="mod-orig-info-container" style="display: none;">
      </div>

      <div class="modify-panel-displays">
        <div class="modify-old-container silver-bordered-no-right"
          v-bind:class="{'has-checkerboard-bg': orig_checkerbg_active }">
          <img v-bind:src="escapeLocalPath(orig_attribute.path)" />
        </div>
        <div class="modify-image-info silver-bordered">
          <table class="mod-info-table is-hpaddingless" style="width: 100%;">
            <thead>
              <tr>
                <th>Original</th>
                <th>Attribute</th>
                <th>Modified</th>
              </tr>
            </thead>
            <tbody>
              <!-- <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute.name">{{ orig_attribute.name }}</span>
                </td>
                <td class="mod-info-label is-cyan">Name</td>
                <td class="mod-info-data">
                </td>
              </tr> -->
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origDimensions }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">Dimensions</td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ previewDimensions }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.file_size_hr }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  File size
                  <template v-if="preview_attribute">
                    <br/>
                    {{ previewSizePercentage }}
                  </template>
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ preview_attribute.file_size_hr }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.format }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">Format</td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ preview_attribute.format }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.frame_count }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">Total frames</td>
                <td class="mod-info-data">
                  <span v-if="preview_info">{{ preview_attribute.frame_count }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.fps }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">Frame rate</td>
                <td class="mod-info-data">
                  <span v-if="preview_info">{{ preview_attribute.fps }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.delay_info }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">Avg. Delay</td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ preview_attribute.delay_info }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.loop_duration }}</span>
                </td>
                <td class="mod-info-label is-cyan">Loop duration</td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ preview_attribute.loop_duration }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <template v-if="orig_attribute">
                    {{ orig_attribute.loop_count }}
                    <!-- <span v-if="orig_attribute.loop_count == 0">Infinite</span>
                    <span v-else>{{ orig_attribute.loop_count }}</span> -->
                  </template>
                  <!-- <template v-else>-</template> -->
                </td>
                <td class="mod-info-label is-cyan">Loop count</td>
                <td class="mod-info-data">
                  <template v-if="preview_attribute">
                    {{ preview_attribute.loop_count }}
                    <!-- <span v-if="preview_attribute.loop_count == 0">Infinite</span>
                    <span v-else>{{ preview_attribute.loop_count }}</span> -->
                  </template>
                </td>
              </tr>
            </tbody>
          </table>

        </div>
        <div class="modify-new-container silver-bordered-no-left" 
          v-bind:title="preview_info?
            `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
            `File size: ${preview_info.general_info.fsize_hr.value}\n` +
            `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
            `Format: ${preview_info.general_info.format.value}` : ''
          "
          v-bind:class="{'has-checkerboard-bg': new_checkerbg_active }">
          <img v-bind:src="escapeLocalPath(preview_path_cb)" />
        </div>
      </div>
      <div class="modify-panel-middlebar">
        <div class="mpb-load-buttons">
          <a v-on:click="loadImage" class="button is-neon-emerald" v-bind:class="{'is-loading': MOD_IS_LOADING, 'non-interactive': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load Image</span>
          </a>
          <a v-on:click="clearImage" class="button is-neon-crimson" v-bind:class="{'non-interactive': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-times"></i>
            </span>
            <span>Clear</span>
          </a>
          <a v-on:click="toggleOrigCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': orig_checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </div>
        <div class="mpb-center-buttons"></div>
        <div class="mpb-preview-buttons">
          <a v-on:click="previewModImg" class="button is-neon-cyan" v-bind:class="{'is-loading': MOD_IS_PREVIEWING, 'non-interactive': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-eye"></i>
            </span>
            <span>Preview</span>
          </a>
          <a v-on:click="clearPreviewImage" class="button is-neon-crimson" v-bind:class="{'non-interactive': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-times"></i>
            </span>
            <span>Clear</span>
          </a>
          <a v-on:click="toggleNewCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': new_checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </div>
      </div>
      <div class="modify-panel-controls">
        <div class="mpc-left-panel">
          <aside class="menu has-text-centered" style="margin: 0;">
            <ul class="menu-list">
              <li id="MOD_box_general" class="subtab-menu-item"
                v-bind:class="{'is-selected': mod_menuselection == 0}">
                <a id="MOD_menu_general" v-on:click="mod_menuselection = 0">
                  <span class="icon is-large">
                    <i class="fas fa-image fa-2x fa-inverse"></i>
                  </span>
                  <p class="is-white-d">General</p>
                </a>
              </li>
              <li id="MOD_box_gif" class="subtab-menu-item is-cyan"
                v-bind:class="{'is-selected': mod_menuselection == 1}">
                <a id="MOD_menu_gif" v-on:click="mod_menuselection = 1"
                  v-bind:class="{'is-disabled': criteria.format == 'PNG'}">
                  <span class="icon is-large">
                    <i class="far fa-images fa-2x fa-inverse"></i>
                  </span>
                  <p class="is-white-d is-large">GIF</p>
                </a>
              </li>
              <li id="MOD_box_apng" class="subtab-menu-item"
                v-bind:class="{'is-selected': mod_menuselection == 2}">
                <a id="MOD_menu_apng" v-on:click="mod_menuselection = 2"
                  v-bind:class="{'is-disabled': criteria.format == 'GIF'}">
                  <span class="icon is-large">
                    <i class="far fa-images fa-2x fa-inverse"></i>
                  </span>
                  <p class="is-white-d is-large">APNG</p>
                </a>
              </li>
            </ul>
          </aside>
        </div>
        <div class="mpc-right-panel">
          <div v-show="mod_menuselection == 0">
            <table class="" width="100%">
              <tr>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">Width</label>
                    <div class="control">
                      <input v-bind:value="criteria.width" v-on:keydown="numConstrain($event, true, true)" v-on:input="widthHandler(criteria.width, $event)" 
                        class="input is-neon-white" type="number" min="1" step="1"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">Height</label>
                    <div class="control">
                      <input v-bind:value="criteria.height" v-on:keydown="numConstrain($event, true, true)" v-on:input="heightHandler(criteria.height, $event)"
                      class="input is-neon-white" type="number" min="1" step="1"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label
                      class="label"
                      title="Which algorithm to use when resizing the image. Default is Bicubic"
                      >Resize Method</label
                    >
                    <div class="control">
                      <div class="select is-neon-cyan">
                        <select v-model="criteria.resize_method">
                          <option
                            value="BICUBIC"
                            title="General-use resizing algorithm for most images"
                          >
                            Bicubic
                          </option>
                          <option
                            value="NEAREST"
                            title="Preserve sharp edges. Ideal for pixel art"
                          >
                            Nearest
                          </option>
                          <option
                            value="BILINEAR"
                            title="Similar to Bicubic, but not as smooth"
                          >
                            Bilinear
                          </option>
                          <option value="BOX">Box</option>
                          <option value="HAMMING">Hamming</option>
                          <option value="LANCZOS">Lanczos</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  
                </td>
                <td width="16.7%" class="force-vcenter">
                  <label class="checkbox" title="Flip the image horizontally">
                    <input v-model="criteria.flip_x" type="checkbox" />
                    Flip X
                  </label>
                  <br/>
                  <label class="checkbox" title="Flip the image vertically">
                    <input v-model="criteria.flip_y" type="checkbox" />
                    Flip Y
                  </label>
                </td>
                <td width="16.7%" class="force-vcenter">
                  <label class="checkbox" title="Reverse the animation">
                    <input v-model="criteria.is_reversed" type="checkbox" />
                    Reversed
                  </label>
                  <br/>
                  <!-- <label class="checkbox" title="Preserve transparent pixels">
                    <input v-model="preserve_alpha" type="checkbox" />
                    Preserve Alpha
                  </label> -->
                  <label class="checkbox">
                    <input v-model="lock_aspect_ratio" type="checkbox"/>
                    Lock aspect ratio
                  </label>
                </td>
              </tr>
              <tr>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">FPS</label>
                    <div class="control">
                      <input v-model="criteria.fps" v-on:input="fpsConstrain" v-on:keydown="numConstrain($event, true, false)" class="input is-neon-white" type="number" min="0"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">Delay</label>
                    <div class="control">
                      <input v-model="criteria.delay" v-on:input="delayConstrain" v-on:keydown="numConstrain($event, true, false)" class="input is-neon-white" type="number" min="0"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">Loop count</label>
                    <div class="control">
                      <input v-model="criteria.loop_count" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <!-- <div class="field">
                    <label class="label">Rotation</label>
                    <div class="control">
                      <input v-model="criteria.rotation" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" />
                    </div>
                  </div> -->
                </td>
                <!-- <td width="20%">
                  <div class="field">
                    <label class="label">Skip Frames</label>
                    <div class="control">
                      <input v-model="skip_frame" class="input is-neon-white" type="number" min="0"/>
                    </div>
                  </div>
                </td> -->
                <td width="16.7%">
                </td>
                <td width="16.7%" class="force-vcenter">
                  <!-- <label class="checkbox">
                    <input v-model="lock_aspect_ratio" type="checkbox"/>
                    Lock aspect ratio
                  </label> -->
                  <br/>
                  <template v-if="aspect_ratio && aspect_ratio.text">
                    <input v-model="aspect_ratio.text" class="input is-border-colorless is-paddingless" style="height: 1.5em;" readonly="readonly"/>
                  </template>
                  <template v-else>&nbsp;</template>
                </td>
              </tr>
              <tr>
              </tr>
              <tr>
                <td colspan="4">
                  <div class="field has-addons">
                    <div class="control">
                      <a v-on:click="btnSetSavePath" class="button is-neon-cyan">
                        <span class="icon is-small">
                          <i class="fas fa-save"></i>
                        </span>
                        <span>Save to</span>
                      </a>
                    </div>
                    <div class="control is-expanded">
                      <input v-model="savePath"
                        class="input is-neon-white"
                        type="text"
                        placeholder="Output file"
                        readonly
                      />
                    </div>
                  </div>
                </td>
                <td colspan="1">
                  <div class="field">
                    <div class="control">
                      <div class="select is-neon-cyan" v-bind:class="{'non-interactive': buttonIsFrozen}">
                        <select v-model="criteria.format">
                          <option value="GIF">GIF</option>
                          <option value="PNG">APNG</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </td>
                <td colspan="1">
                  <a v-on:click="btnModifyImage" class="button is-neon-cyan"  v-bind:class="{'is-loading': MOD_IS_MODIFYING, 'non-interactive': buttonIsFrozen}">
                    MODIFY</a>
                </td>
              </tr>
              <tr>
                <td colspan="6">
                  <input
                    v-model="modify_msgbox"
                    type="text"
                    class="input is-left-paddingless is-border-colorless"
                    readonly="readonly"
                  />
                </td>
              </tr>
            </table>
          </div>
          <div v-show="mod_menuselection == 1">
            <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
              <GIFOptimizationRow
                :is_optimized.sync="gif_opt_criteria.is_optimized"
                :optimization_level.sync="gif_opt_criteria.optimization_level"
                :is_lossy.sync="gif_opt_criteria.is_lossy"
                :lossy_value.sync="gif_opt_criteria.lossy_value"
                :is_reduced_color.sync="gif_opt_criteria.is_reduced_color"
                :color_space.sync="gif_opt_criteria.color_space"
                :is_unoptimized.sync="gif_opt_criteria.is_unoptimized"
              />
              <GIFUnoptimizationRow
              :is_optimized.sync="gif_opt_criteria.is_optimized"
              :is_lossy.sync="gif_opt_criteria.is_lossy"
              :is_reduced_color.sync="gif_opt_criteria.is_reduced_color"
              :is_unoptimized.sync="gif_opt_criteria.is_unoptimized"
              />
            </table>
          </div>
          <div v-show="mod_menuselection == 2">
            <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
              <APNGOptimizationRow
                :apng_is_optimized.sync="apng_opt_criteria.apng_is_optimized"
                :apng_optimization_level.sync="apng_opt_criteria.apng_optimization_level"
                :apng_is_lossy.sync="apng_opt_criteria.apng_is_lossy"
                :apng_lossy_value.sync="apng_opt_criteria.apng_lossy_value"
                :apng_convert_color_mode.sync="apng_opt_criteria.apng_convert_color_mode"
                :apng_new_color_mode.sync="apng_opt_criteria.apng_new_color_mode"
                :apng_is_unoptimized.sync="apng_opt_criteria.apng_is_unoptimized"
              />
              <APNGUnoptimizationRow
                :apng_is_optimized.sync="apng_opt_criteria.apng_is_optimized"
                :apng_is_lossy.sync="apng_opt_criteria.apng_is_lossy"
                :apng_is_unoptimized.sync="apng_opt_criteria.apng_is_unoptimized"
              />
            </table>
          </div>
        </div>
      </div>
    </div>
    <!-- </div> -->
  </div>
</template>

<script>

const remote = require('electron').remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { tridentEngine } = require("./PythonCommander.js");
const { GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION, randString, wholeNumConstrain, posWholeNumConstrain, floatConstrain, numConstrain, 
        gcd, validateFilename, fileExists, roundPrecise, escapeLocalPath, TEMP_PATH, PREVIEWS_PATH, stem } = require("./Utility.vue");
const path = require("path");
const lodashClonedeep = require('lodash.clonedeep');
import GIFOptimizationRow from "./components/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./components/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./components/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./components/APNGUnoptimizationRow.vue";

let common_metadata = {
  name: "",
  width: "",
  height: "",
  frame_count: "",
  frame_count_ds: "",
  fps: "",
  delay: "",
  delay_info: "",
  loop_duration: "",
  loop_count: "",
  file_size: "",
  file_size_hr: "",
  format: "",
  path: "",
  hash_sha1: "",
  last_modified_dt: "",
};

var data = {
  orig_attribute: lodashClonedeep(common_metadata),
  preview_attribute: lodashClonedeep(common_metadata),
  // orig_attribute: {
  //   name: "",
  //   width: "",
  //   height: "",
  //   frame_count: "",
  //   frame_count_ds: "",
  //   fps: "",
  //   delay: "",
  //   delay_info: "",
  //   loop_duration: "",
  //   loop_count: "",
  //   file_size: "",
  //   file_size_hr: "",
  //   format: "",
  //   path: "",
  //   hash_sha1: "",
  //   last_modified_dt: "",
  // },
  criteria: {
    width: "",
    height: "",
    resize_method: "BICUBIC",
    rotation: "",
    fps: "",
    delay: "",
    loop_count: "",
    format: "GIF",
    skip_frame: "",
    flip_x: false,
    flip_y: false,
    is_reversed: false,
    preserve_alpha: false,
    start_frame: 0,
  },
  gif_opt_criteria: {
    is_optimized: false,
    optimization_level: "1",
    is_lossy: false,
    lossy_value: "",
    is_reduced_color: false,
    color_space: "",
    is_unoptimized: false,
  },
  apng_opt_criteria: {
    apng_is_optimized: false,
    apng_optimization_level: "1",
    apng_is_lossy: false,
    apng_lossy_value: "",
    apng_is_unoptimized: false,
    apng_convert_color_mode: false,
    apng_new_color_mode: "RGBA",
  },
  preview_path: "",
  preview_path_cb: "",
  preview_info: "",
  save_fstem: "",
  save_dir: "",
  preview_size: "",
  preview_size_hr: "",
  aspect_ratio: "",
  lock_aspect_ratio: false,
  mod_menuselection: 0,
  orig_checkerbg_active: false,
  new_checkerbg_active: false,
  MOD_IS_LOADING: false,
  MOD_IS_MODIFYING: false,
  MOD_IS_PREVIEWING: false,
  modify_msgbox: "",
};

function clearOrigMetadata() {
  data.orig_attribute.name = "";
  data.orig_attribute.width = "";
  data.orig_attribute.height = "";
  data.orig_attribute.frame_count = "";
  data.orig_attribute.frame_count_ds = "";
  data.orig_attribute.fps = "";
  data.orig_attribute.delay = "";
  data.orig_attribute.delay_info = "";
  data.orig_attribute.loop_duration = "";
  data.orig_attribute.loop_count = "";
  data.orig_attribute.file_size = "";
  data.orig_attribute.file_size_hr = "";
  data.orig_attribute.format = "";
  data.orig_attribute.path = "";
  data.orig_attribute.hash_sha1 = "";
  data.orig_attribute.last_modified_dt = "";
  data.modify_msgbox = "";
}

function clearPreiewMetadata() {
  data.preview_attribute.name = "";
  data.preview_attribute.width = "";
  data.preview_attribute.height = "";
  data.preview_attribute.frame_count = "";
  data.preview_attribute.frame_count_ds = "";
  data.preview_attribute.fps = "";
  data.preview_attribute.delay = "";
  data.preview_attribute.delay_info = "";
  data.preview_attribute.loop_duration = "";
  data.preview_attribute.loop_count = "";
  data.preview_attribute.file_size = "";
  data.preview_attribute.file_size_hr = "";
  data.preview_attribute.format = "";
  data.preview_attribute.path = "";
  data.preview_attribute.hash_sha1 = "";
  data.preview_attribute.last_modified_dt = "";
  data.modify_msgbox = "";
}

function clearCriteriaFields() {
  data.criteria.old_width = "";
  data.criteria.width = "";
  data.criteria.old_height = "";
  data.criteria.height = "";
  data.criteria.rotation = "";
  data.criteria.fps = "";
  data.criteria.delay = "";
  data.criteria.loop_count = "";
  data.criteria.skip_frame = "";
  data.criteria.modify_msgbox = "";
  let ARData = {
    "w_ratio": "",
    "h_ratio": "",
    "text": "",
  };
  data.aspect_ratio = ARData;
}

function toggleOrigCheckerBG() {
  data.orig_checkerbg_active = !data.orig_checkerbg_active;
  console.log("orig checkerbg is", data.orig_checkerbg_active);
}

function toggleNewCheckerBG() {
  data.new_checkerbg_active = !data.new_checkerbg_active;
  console.log("new checkerbg is", data.new_checkerbg_active);
}

let extension_filters = [
    { name: 'Images', extensions: ['png', 'gif'] },
];
let file_dialog_props = ['openfile'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];

function loadImage() {
  console.log("mod load image called");
  var options = {
    filters: extension_filters,
    properties: file_dialog_props
  };
  dialog.showOpenDialog(mainWindow, options).then((result) => {
    let chosen_path = result.filePaths;
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined || chosen_path.length == 0) {
      return;
    }
    data.MOD_IS_LOADING = true;
    tridentEngine(["inspect_one", chosen_path[0], "animated"], (error, res) => {
      if (error) {        
        try {
          data.modify_msgbox = error;
        }
        catch (e) {
          data.modify_msgbox = error;
        }
        // mboxError(split_msgbox, error);
        data.MOD_IS_LOADING = false;
      } else if (res) {
        if (res && res.msg) {
          data.modify_msgbox = res.msg;
        } else if (res && res.data) {
          loadOrigMetadata(res.data);
          populateForm(res.data);
          data.save_fname = res.data.general_info.name.value;
          data.modify_msgbox = "";
        }
        data.MOD_IS_LOADING = false;
        data.lock_aspect_ratio = true;
      }
    });
    console.log("registered!");
  });
}

function loadOrigMetadata(res) {
  let geninfo = res.general_info;
  let ainfo = res.animation_info;
  data.orig_attribute.name = geninfo.name.value;
  data.save_fstem = stem(data.save_fstem || geninfo.name.value);
  data.orig_attribute.width = geninfo.width.value;
  data.orig_attribute.height = geninfo.height.value;
  data.orig_attribute.fps = `${ainfo.fps.value} FPS`;
  data.orig_attribute.frame_count= ainfo.frame_count.value;
  data.orig_attribute.format = geninfo.format.value;
  let delay_info = `${roundPrecise(ainfo.average_delay.value, 3)} ms`;
  if (ainfo.delays_are_even.value) {
    delay_info += ` (even)`;
  }
  else {
    delay_info += ` (uneven)`;
  }
  data.orig_attribute.delay = ainfo.average_delay.value;
  data.orig_attribute.delay_info = delay_info;
  data.orig_attribute.loop_duration = `${ainfo.loop_duration.value} seconds`;
  if (ainfo.loop_count.value == 0) {
    data.orig_attribute.loop_count = "Infinite"
  }
  else {
    data.orig_attribute.loop_count = ainfo.loop_count.value;
  }
  data.orig_attribute.path = geninfo.absolute_url.value;
  data.orig_attribute.file_size = geninfo.fsize.value;
  data.orig_attribute.file_size_hr = geninfo.fsize_hr.value;
  data.orig_attribute.last_modified_dt = geninfo.modification_datetime.value;
  data.orig_attribute.hash_sha1 = geninfo.hash_sha1.value;
}

function loadPreviewMetadata(res) {
  let geninfo = res.general_info;
  let ainfo = res.animation_info;
  data.preview_attribute.name = geninfo.name.value;
  data.preview_attribute.width = geninfo.width.value;
  data.preview_attribute.height = geninfo.height.value;
  data.preview_attribute.fps = `${ainfo.fps.value} FPS`;
  data.preview_attribute.frame_count= ainfo.frame_count.value;
  data.preview_attribute.format = geninfo.format.value;
  let delay_info = `${roundPrecise(ainfo.average_delay.value, 3)} ms`;
  if (ainfo.delays_are_even.value) {
    delay_info += ` (even)`;
  }
  else {
    delay_info += ` (not even)`;
  }
  data.preview_attribute.delay = ainfo.average_delay.value;
  data.preview_attribute.delay_info = delay_info;
  data.preview_attribute.loop_duration = `${ainfo.loop_duration.value} seconds`;
  if (ainfo.loop_count.value == 0) {
    data.preview_attribute.loop_count = "Infinite"
  }
  else {
    data.preview_attribute.loop_count = ainfo.loop_count.value;
  }
  data.preview_attribute.path = geninfo.absolute_url.value;
  data.preview_attribute.file_size = geninfo.fsize.value;
  data.preview_attribute.file_size_hr = geninfo.fsize_hr.value;
  data.preview_attribute.last_modified_dt = geninfo.modification_datetime.value;
  data.preview_attribute.hash_sha1 = geninfo.hash_sha1.value;
}

function populateForm(res) {
  var geninfo = res.general_info;
  var ainfo = res.animation_info;
  data.criteria.format = geninfo.format.value;
  data.criteria.width = geninfo.width.value;
  data.criteria.height = geninfo.height.value;
  data.criteria.delay = roundPrecise(ainfo.average_delay.value, 3) / 1000;
  data.criteria.fps = roundPrecise(ainfo.fps.value, 3);
  data.criteria.loop_count = ainfo.loop_count.value;
  updateAspectRatio(data.criteria.width, data.criteria.height);
}

function clearImage() {
  console.log(data);
  clearOrigMetadata();
  clearCriteriaFields();
  clearPreviewImage();
  data.lock_aspect_ratio = false;
}

function clearPreviewImage() {
  data.preview_path = "";
  data.preview_path_cb = "";
  data.preview_size = "";
  data.preview_size_hr = "";
  clearPreiewMetadata();
}

function singleSaveOption() {
  return {
    title: `Save As`,
    defaultPath: saveFileName(),
    filters: [{ name: data.criteria.format, extensions: [data.criteria.format.toLowerCase()] }],
    properties: ["createDirectory", "showOverwriteConfirmation", "dontAddToRecent"],
  }
}


function saveFileName() {
  return `${data.save_fstem}.${data.criteria.format.toLowerCase()}`;
}

function savePath() {
  if (data.save_dir && data.save_fstem)
    return path.join(data.save_dir, `${data.save_fstem}.${data.criteria.format.toLowerCase()}`);
  else
    return "";
}


function setSavePath(afterSaveCallback) {
  dialog.showSaveDialog(mainWindow, singleSaveOption()).then((result) => {
    if (result.canceled) return;
    let save_path = result.filePath;
    console.log(result);
    // data.save_path = save_path;
    data.save_dir = path.dirname(save_path);
    data.save_fstem = stem(path.basename(save_path));
    if (afterSaveCallback) {
      afterSaveCallback();
    }
  });
}


function btnSetSavePath() {
  setSavePath();
}

function widthHandler(width, event) {
  // data.orig_attribute.width = parseInt(width);
  console.log(event);
  let newWidth = event.target.value;
  data.criteria.width = newWidth;
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) { // Change height if lock_aspect_ratio is true and height is not 0
    let raHeight = Math.round(newWidth / data.aspect_ratio.w_ratio * data.aspect_ratio.h_ratio);
    data.criteria.height = raHeight > 0? raHeight : "";
  }
  else {
    updateAspectRatio(data.criteria.width, data.criteria.height);
  }
}

function heightHandler(height, event) {
  // data.orig_attribute.height = parseInt(height);
  let newHeight = event.target.value;
  data.criteria.height = newHeight;
  if (data.lock_aspect_ratio && data.aspect_ratio.w_ratio > 0) {
    let raWidth = Math.round(newHeight / data.aspect_ratio.h_ratio * data.aspect_ratio.w_ratio);
    console.log(raWidth);
    data.criteria.width = raWidth > 0? raWidth : "";
  }
  else {
    updateAspectRatio(data.criteria.width, data.criteria.height);
  }
}

function updateAspectRatio(width, height) {
  if (data.criteria.width && data.criteria.height) {
    console.log('uAR', width, height);
    let divisor = gcd(width, height);
    let w_ratio = width / divisor;
    let h_ratio = height / divisor;
    let ARData = {
      "w_ratio": w_ratio,
      "h_ratio": h_ratio,
      "text": `${w_ratio}:${h_ratio}`,
    };
    console.log(ARData);
    data.aspect_ratio = ARData;
  }
}

function btnModifyImage() {
  if (!data.orig_attribute.path) {
    data.modify_msgbox = "Please load the animated image to be modified!";
    return;
  }
  if (savePath())
    modifyImage();
  else
    setSavePath(modifyImage);
}


function modifyImage() {
  let proceed_modify = true;
  data.modify_msgbox = "";
  
  if (proceed_modify) {
    data.MOD_IS_MODIFYING = true;
    let criteria_pack = lodashClonedeep({
      "criteria": { ...data.criteria, "hash_sha1": data.orig_attribute.hash_sha1, "last_modified_dt": data.orig_attribute.last_modified_dt },
      "gif_opt_criteria": data.gif_opt_criteria,
      "apng_opt_criteria": data.apng_opt_criteria,
    });
    // criteria_pack.criteria.name += `_preview_${Date.now()}_${randString(7)}`;
    tridentEngine(["modify_image", data.orig_attribute.path, savePath(), criteria_pack], (error, res) => {
      if (error) {
        console.error(error);
        data.modify_msgbox = error;
        data.MOD_IS_MODIFYING = false;
      }
      else if (res) {
        console.log(res);
        if (res.msg) {
          data.modify_msgbox = res.msg;
        }
      }
    },
    () => {
      data.modify_msgbox = "Modified and saved!"
      data.MOD_IS_MODIFYING = false;
    });
  }
}

function previewModImg() {
  if (data.orig_attribute.path == "") {
    data.modify_msgbox = "Please load an animated image first!";
    return;
  }
  data.MOD_IS_PREVIEWING = true;
  let criteria_pack = lodashClonedeep({
    "criteria": { ...data.criteria, "hash_sha1": data.orig_attribute.hash_sha1, "last_modified_dt": data.orig_attribute.last_modified_dt },
    "gif_opt_criteria": data.gif_opt_criteria,
    "apng_opt_criteria": data.apng_opt_criteria,
  });
  let preview_filename = `${data.save_fstem}_preview_${Date.now()}_${randString(7)}.${data.criteria.format.toLowerCase()}`;
  let preview_savepath = path.join(process.cwd(), PREVIEWS_PATH, preview_filename);
  // criteria_pack.criteria.name += `_preview_${Date.now()}_${randString(7)}`;
  tridentEngine(["modify_image", data.orig_attribute.path, preview_savepath, criteria_pack], (error, res) => {
    if (error) {
      console.error(error);
      data.modify_msgbox = error;
      data.MOD_IS_PREVIEWING = false;
    }
    else if (res) {
      if (res.msg) {
        data.modify_msgbox = res.msg;
      }
      if (res.preview_path) {
        data.preview_path = res.preview_path;
        previewPathCacheBreaker();
      }
    }
  },
  () => tridentEngine(["inspect_one", data.preview_path, "animated"], (error, res) => {
    if (error) {
      console.error(error);
      data.modify_msgbox = error;
    } else if (res && res.data) {
      let preview_data = res.data;
      console.log(`res -> ${res}`);
      console.log("preview inspect");
      loadPreviewMetadata(preview_data);
      data.preview_info = preview_data;
      data.preview_size = preview_data.general_info.fsize.value;
      data.preview_size_hr = preview_data.general_info.fsize_hr.value;
      data.modify_msgbox = "Previewed!"
      data.MOD_IS_PREVIEWING = false;
    }})
  );
}

function buttonIsFrozen() {
  if (data.MOD_IS_LOADING || data.MOD_IS_MODIFYING || data.MOD_IS_PREVIEWING) return true;
  else return false;
}

function delayConstrain(event) {
  console.log("delay event", event);
  let value = event.target.value;
  if (value && value.includes(".")) {
    let numdec = value.split(".");
    console.log("numdec", numdec);
    let precision = 2;
    if (data.criteria.format == "GIF") {
      precision = GIF_DELAY_DECIMAL_PRECISION;
    } else if (data.criteria.format == "PNG") {
      precision = APNG_DELAY_DECIMAL_PRECISION;
    }
    if (numdec[1].length > precision) {
      let decs = numdec[1].substring(0, precision);
      console.log("decs limit triggered", decs);
      data.criteria.delay = `${numdec[0]}.${decs}`;
    }
  }
  data.criteria.fps = Math.round(1000 / data.criteria.delay) / 1000;
}

function fpsConstrain(event) {
  console.log("fps event", event);
  let value = event.target.value;
  if (value) {
    let mult = 100;
    if (data.criteria.format == "GIF") {
      mult = 100;
    } else if (data.criteria.format == "PNG") {
      mult = 1000;
    }
    data.criteria.delay = Math.round(mult / data.criteria.fps) / mult;
  }
}


function origDimensions() {
  if (data.orig_attribute.width && data.orig_attribute.height) {
    return `${data.orig_attribute.width} x ${data.orig_attribute.height}`;
  }
  else {
    return "";
  }
}

function previewDimensions() {
  if (data.preview_attribute.width && data.preview_attribute.height) {
    return `${data.preview_attribute.width} x ${data.preview_attribute.height}`;
  }
  else {
    return "";
  }
}

function previewSizePercentage() {
  if (data.orig_attribute.path && data.preview_attribute.path) {
    let oldSize = data.orig_attribute.file_size
    let previewSize = data.preview_attribute.file_size;
    console.log(oldSize, previewSize);
    let newSizePercentage = (previewSize / oldSize * 100).toFixed(2);
    let text = `${newSizePercentage}%`;
    return text;
  }
  else return "";
}


function previewPathCacheBreaker() {
  let cb_url = `${data.preview_path}`;
  console.log("Cache breaker url", cb_url);
  data.preview_path_cb = cb_url;
}


export default {
  data: function() {
    return data;
  },
  components: {
    GIFOptimizationRow,
    GIFUnoptimizationRow,
    APNGOptimizationRow,
    APNGUnoptimizationRow,
  },
  methods: {
    loadImage: loadImage,
    clearImage: clearImage,
    clearPreviewImage: clearPreviewImage,
    btnSetSavePath: btnSetSavePath,
    // chooseOutDir: chooseOutDir,
    previewModImg: previewModImg,
    btnModifyImage: btnModifyImage,
    // modifyImage: modifyImage,
    widthHandler: widthHandler,
    heightHandler: heightHandler,
    toggleOrigCheckerBG: toggleOrigCheckerBG,
    toggleNewCheckerBG: toggleNewCheckerBG,
    delayConstrain: delayConstrain,
    fpsConstrain: fpsConstrain,
    floatConstrain: floatConstrain,
    numConstrain: numConstrain,
    roundPrecise: roundPrecise,
    escapeLocalPath: escapeLocalPath,
  },
  computed: {
    origDimensions: origDimensions,
    previewDimensions: previewDimensions,
    buttonIsFrozen: buttonIsFrozen,
    previewSizePercentage: previewSizePercentage,
    saveFileName: saveFileName,
    savePath: savePath,
  }
};
</script>
