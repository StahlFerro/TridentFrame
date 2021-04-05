<template>
  <div id="modify_panel">
    <div class="modify-panel-root">

      <div class="mod-orig-info-container" style="display: none;">
        <table class="table mod-orig-info-table is-hpaddingless">
          <tbody>
            <tr>
              <td class="mod-info-label is-cyan">Name</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.name">{{ orig_attribute.name }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Dimensions</td>
              <td class="mod-info-data">
                <span v-if="origDimensions">{{ origDimensions }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">File size</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.file_size_hr">{{ orig_attribute.file_size_hr }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Format</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.file_size_hr">{{ orig_attribute.format }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Total frames</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.frame_count">{{ orig_attribute.frame_count }} ({{ orig_attribute.frame_count_ds }})</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Frame rate</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.fps">{{ orig_attribute.fps }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Frame delay</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.fps">{{ orig_attribute.delay_info }}</span>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Loop duration</td>
              <td class="mod-info-data">
                <span v-if="orig_attribute.loop_duration">{{ orig_attribute.loop_duration }} seconds</span>
                <span v-else>-</span>
                </td>
            </tr>
            <tr>
              <td class="mod-info-label is-cyan">Loop count</td>
              <td class="mod-info-data">
                <template v-if="orig_attribute.path">
                  <span v-if="orig_attribute.loop_count == 0">Infinite</span>
                  <span v-else>{{ orig_attribute.loop_count }}</span>
                </template>
                <template v-else>-</template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="modify-panel-displays">
        <div class="modify-old-container silver-bordered">
          <img v-bind:src="orig_attribute.path" />
        </div>
        <div class="modify-new-container silver-bordered-no-left" 
          v-bind:title="preview_info?
            `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
            `File size: ${preview_info.general_info.fsize_hr.value}\n` +
            `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
            `Format: ${preview_info.general_info.format.value}` : ''
          ">
          <img v-bind:src="preview_path_cb" />
        </div>
      </div>
      <div class="modify-panel-middlebar">
        <div class="mpb-load-buttons">
          <a v-on:click="loadImage" class="button is-neon-emerald" v-bind:class="{'is-loading': MOD_IS_LOADING, 'non-interactive': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load GIF/APNG</span>
          </a>
          <a v-on:click="clearImage" class="button is-neon-crimson">
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
        <div class="mpb-preview-buttons">
          <a v-on:click="previewModImg" class="button is-neon-cyan" v-bind:class="{'is-loading': MOD_IS_PREVIEWING, 'non-interactive': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-eye"></i>
            </span>
            <span>Preview</span>
          </a>
          <a v-on:click="clearPrevImage" class="button is-neon-crimson" v-bind:class="{'non-interactive': buttonIsFrozen}">
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
                <td width="33.33333%" colspan="2">
                  <div class="field">
                    <label class="label">Name</label>
                    <div class="control">
                      <input v-model="criteria.name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">Width</label>
                    <div class="control">
                      <input v-bind:value="criteria.width" v-on:keydown="numConstrain($event, true, true)" v-on:input="widthHandler(width, $event)" 
                        class="input is-neon-white" type="number" min="1" step="1"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label">Height</label>
                    <div class="control">
                      <input v-bind:value="criteria.height" v-on:keydown="numConstrain($event, true, true)" v-on:input="heightHandler(height, $event)"
                      class="input is-neon-white" type="number" min="1" step="1"/>
                    </div>
                  </div>
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
                  <div class="field">
                    <label class="label">Rotation</label>
                    <div class="control">
                      <input v-model="criteria.rotation" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" />
                    </div>
                  </div>
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
                  <div class="field">
                    <label class="label">Format</label>
                    <div class="control">
                      <div class="select is-neon-cyan">
                        <select v-model="criteria.format">
                          <option value="GIF">GIF</option>
                          <option value="PNG">APNG</option>
                        </select>
                      </div>
                    </div>
                  </div>
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
                <td colspan="5">
                  <div class="field has-addons">
                    <div class="control">
                      <a v-on:click="chooseOutDir" class="button is-neon-cyan">
                        <span class="icon is-small">
                          <i class="fas fa-folder-open"></i>
                        </span>
                        <span>Save to</span>
                      </a>
                    </div>
                    <div class="control is-expanded">
                      <input v-model="outdir"
                        class="input is-neon-white"
                        type="text"
                        placeholder="Output folder"
                        readonly
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <a v-on:click="modifyImage" class="button is-neon-cyan"  v-bind:class="{'is-loading': MOD_IS_MODIFYING, 'non-interactive': buttonIsFrozen}">
                    MODIFY</a>
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
const { tridentEngine } = require("./PythonCommander.vue");
const { GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION, randString, wholeNumConstrain, posWholeNumConstrain, floatConstrain, numConstrain, 
        gcd, validateFilename, fileExists } = require("./Utility.vue");
import GIFOptimizationRow from "./components/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./components/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./components/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./components/APNGUnoptimizationRow.vue";


var data = {
  orig_attribute: {
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
  },
  criteria: {
    name: "",
    width: "",
    height: "",
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
  },
  preview_path: "",
  preview_path_cb: "",
  preview_info: "",
  outdir: "",
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

function clearOrigFields() {
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

function clearNewFields() {
  data.name = "";
  data.old_width = "";
  data.width = "";
  data.old_height = "";
  data.height = "";
  data.rotation = "";
  data.fps = "";
  data.delay = "";
  data.loop_count = "";
  data.skip_frame = "";
  data.modify_msgbox = "";
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
          console.error(error);
          let error_data = JSON.parse(error);
          data.modify_msgbox = error_data.error;
        }
        catch (e) {
          data.modify_msgbox = error;
        }
        // mboxError(split_msgbox, error);
        data.MOD_IS_LOADING = false;
      } else if (res) {
        res = JSON.parse(res);
        if (res && res.msg) {
          data.modify_msgbox = res.msg;
        } else if (res && res.data) {
          loadOrigInfo(res.data);
          loadNewInfo(res.data);
          data.modify_msgbox = "";
        }
        data.MOD_IS_LOADING = false;
      }
    });
    console.log("registered!");
  });
}

function loadOrigInfo(res) {
  let geninfo = res.general_info;
  let ainfo = res.animation_info;
  data.orig_attribute.name = geninfo.name.value;
  data.orig_attribute.width = geninfo.width.value;
  data.orig_attribute.height = geninfo.height.value;
  data.orig_attribute.fps = `${ainfo.fps.value} fps`;
  data.orig_attribute.frame_count= ainfo.frame_count.value;
  data.orig_attribute.format = geninfo.format.value;
  let delay_info = `${ainfo.average_delay.value} seconds`;
  if (ainfo.delay_is_even) {
    delay_info += ` (even)`;
  }
  data.orig_attribute.delay = ainfo.average_delay.value;
  data.orig_attribute.delay_info = delay_info;
  data.orig_attribute.loop_duration = ainfo.loop_duration.value;
  data.orig_attribute.loop_count = ainfo.loop_count.value;
  data.orig_attribute.path = geninfo.absolute_url.value;
  data.orig_attribute.file_size = geninfo.fsize.value;
  data.orig_attribute.file_size_hr = geninfo.fsize_hr.value;
  data.orig_attribute.last_modified_dt = geninfo.modification_datetime.value;
  data.orig_attribute.hash_sha1 = geninfo.hash_sha1.value;
}

function loadNewInfo(res) {
  var geninfo = res.general_info;
  var ainfo = res.animation_info;
  data.criteria.name = geninfo.base_filename.value;
  data.criteria.format = geninfo.format.value;
  data.criteria.width = geninfo.width.value;
  data.criteria.height = geninfo.height.value;
  data.criteria.delay = ainfo.average_delay.value;
  data.criteria.fps = ainfo.fps.value;
  data.criteria.loop_count = ainfo.loop_count.value;
  updateAspectRatio(data.width, data.height);
}

function clearImage() {
  console.log(data);
  clearOrigFields();
  clearNewFields();
  clearPrevImage();
}

function clearPrevImage() {
  data.preview_path = "";
  data.preview_path_cb = "";
  data.preview_size = "";
  data.preview_size_hr = "";
}

function chooseOutDir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options, (chosen_dir) => {
    console.log(chosen_dir);
    if (chosen_dir && chosen_dir.length > 0) { 
      data.outdir = chosen_dir[0];
    }
  });
}

function widthHandler(width, event) {
  data.old_width = parseInt(width);
  console.log(event);
  let newWidth = event.target.value;
  data.width = newWidth;
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) { // Change height if lock_aspect_ratio is true and height is not 0
    let raHeight = Math.round(newWidth / data.aspect_ratio.w_ratio * data.aspect_ratio.h_ratio);
    data.height = raHeight > 0? raHeight : "";
  }
  else {
    updateAspectRatio(data.width, data.height);
  }
}

function heightHandler(height, event) {
  data.old_height = parseInt(height);
  let newHeight = event.target.value;
  data.height = newHeight;
  if (data.lock_aspect_ratio && data.aspect_ratio.w_ratio > 0) {
    let raWidth = Math.round(newHeight / data.aspect_ratio.h_ratio * data.aspect_ratio.w_ratio);
    console.log(raWidth);
    data.width = raWidth > 0? raWidth : "";
  }
  else {
    updateAspectRatio(data.width, data.height);
  }
}

function updateAspectRatio(width, height) {
  if (data.width && data.height) {
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


function modifyImage() {
  let proceed_modify = true;

  data.modify_msgbox = "";
  var validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.modify_msgbox = validator.msg;
    return;
  }

  if (fileExists(data.outdir, `${data.name}.${data.format.toLowerCase()}`)) {
    let WINDOW = remote.getCurrentWindow();
    let options = {
      buttons: ["Yes", "Cancel"],
      message: "A file with the same name exists in the output folder. Do you want to override it?"
    };
    let response = dialog.showMessageBoxSync(WINDOW, options);
    if (response == 1) proceed_modify = false;
  }
  
  if (proceed_modify) {
    data.MOD_IS_MODIFYING = true;
    client.invoke("modify_image", data.orig_path, data.outdir, data, (error, res) => {
      if (error) {
        console.error(error);
        data.modify_msgbox = error;
        data.MOD_IS_MODIFYING = false;
      }
      else {
        if (res) {
          console.log(res);
          if (res.msg) {
            data.modify_msgbox = res.msg;
          }
          if (res.CONTROL == "MOD_FINISH") {
            data.modify_msgbox = "Modified and saved!"
            data.MOD_IS_MODIFYING = false;
          }
        }
      }
    });
  }
}

function previewModImg() {
  data.MOD_IS_PREVIEWING = true;
  client.invoke("modify_image", data.orig_path, "./temp", data, (error, res) => {
    if (error) {
      console.error(error);
      data.modify_msgbox = error;
      data.MOD_IS_PREVIEWING = false;
    }
    else {
      if (res) {
        console.log(res);
        if (res.msg) {
          data.modify_msgbox = res.msg;
        }
        if (res.preview_path) {
          data.preview_path = res.preview_path;
          previewPathCacheBreaker();
        }
        if (res.CONTROL == "MOD_FINISH") {
          console.log(data.preview_path);
          client.invoke("inspect_one", data.preview_path, "animated", (error, info) => {
            if (error) {
              console.error(error);
              data.MOD_IS_PREVIEWING = false;
            } else {
              console.log("preview inspect");
              console.log(info);
              data.preview_info = info;
              data.preview_size = info.general_info.fsize.value;
              data.preview_size_hr = info.general_info.fsize_hr.value;
              data.modify_msgbox = "Previewed!"
              data.MOD_IS_PREVIEWING = false;
            }
          });
        }
      }
    }
  });
}

function buttonIsFrozen() {
  if (data.MOD_IS_LOADING || data.MOD_IS_MODIFYING || data.MOD_IS_PREVIEWING) return true;
  else return false;
}

function delayConstrain (event) {
  console.log("delay event", event);
  let value = event.target.value;
  if (value && value.includes(".")) {
    let numdec = value.split(".");
    console.log("numdec", numdec);
    let precision = 2;
    if (data.format == 'GIF') {
      precision = GIF_DELAY_DECIMAL_PRECISION;
    }
    else if (data.format == 'PNG') {
      precision = APNG_DELAY_DECIMAL_PRECISION;
    }
    if (numdec[1].length > precision) {
      let decs = numdec[1].substring(0, precision);
      console.log("decs limit triggered", decs);
      data.delay = `${numdec[0]}.${decs}`;
    }
  }
  data.fps = Math.round(1000 / data.delay) / 1000;
}
function fpsConstrain (event) {
  console.log("fps event", event);
  let value = event.target.value;
  if (value) {
    let mult = 100
    if (data.format == 'GIF') { mult = 100; }
    else if (data.format == 'PNG') { mult = 1000; }
    data.delay = Math.round(mult / data.fps) / mult;
  }
}

function origDimensions() {
  if (data.orig_width && data.orig_height) {
    return `${data.orig_width} x ${data.orig_height}`;
  }
  else {
    return "-";
  }
}

function previewSizePercentage() {
  let oldsize = data.orig_file_size
  let prevsize = data.preview_size;
  console.log(oldsize, prevsize);
  let redux = Math.round((prevsize / oldsize) * 100);
  return redux;
}


function previewPathCacheBreaker() {
  let cb_url = `${data.preview_path}?cachebreaker=${randString()}`;
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
    clearPrevImage: clearPrevImage,
    chooseOutDir: chooseOutDir,
    previewModImg: previewModImg,
    modifyImage: modifyImage,
    widthHandler: widthHandler,
    heightHandler: heightHandler,
    toggleOrigCheckerBG: toggleOrigCheckerBG,
    toggleNewCheckerBG: toggleNewCheckerBG,
    delayConstrain: delayConstrain,
    fpsConstrain: fpsConstrain,
    floatConstrain: floatConstrain,
    numConstrain: numConstrain,
  },
  computed: {
    origDimensions: origDimensions,
    buttonIsFrozen: buttonIsFrozen,
    previewSizePercentage: previewSizePercentage,
  }
};
</script>
