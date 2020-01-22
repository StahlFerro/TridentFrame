<template>
  <div id="modify_panel" class="container" style="display: none; padding:10px;">
    <!-- <div class="content"> -->
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <!-- <td width="3%"></td> -->
        <td width="35%"
          colspan="3"
          class="silver-bordered force-center is-paddingless"
          v-bind:class="{'has-checkerboard-bg': orig_checkerbg_active}"
          style="height: 250px;">
          <div class="mod-aimg-container">
            <img v-bind:src="orig_path" />
          </div>
          <!-- <input id="MOD_orig_path" name="MOD_orig_path_field" type="hidden" value /> -->
        </td>
        <!-- <td width="3%"></td> -->

        <td width="6%"></td>
        <td width="9%"></td>
        <td width="35%"
          class="silver-bordered force-center is-paddingless"
          v-bind:class="{'has-checkerboard-bg': new_checkerbg_active}"
          style="height: 250px;">
            <div v-if="preview_info" class="mod-aimg-container" v-bind:title="
              `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
              `File size: ${preview_info.general_info.fsize_hr.value}\n` +
              `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
              `Format: ${preview_info.general_info.format.value}`
            ">
              <img v-bind:src="preview_path_cb" />
            </div>
        </td>
        <td colspan="2" width="15%">
          <span v-if="preview_size">
            Preview size:<br/>{{ preview_size_hr }}<br/>
            ({{ previewSizePercentage }}% of original)
            </span>
        </td>
      </tr>
      <tr>
        <td colspan="3" class="has-text-centered is-hpaddingless">
          <a v-on:click="loadImage" class="button is-neon-cyan" v-bind:class="{'is-loading': MOD_IS_LOADING, 'is-static': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-plus"></i>
            </span>
            <span>Load GIF/APNG</span>
          </a>
          <a v-on:click="clearImage" class="button is-neon-white">
            <span class="icon is-small">
              <i class="fas fa-trash-alt"></i>
            </span>
            <span>Clear</span>
          </a>
          <a v-on:click="toggleOrigCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': orig_checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </td>
        <td colspan="2">
        </td>
        <td class="has-text-centered is-hpaddingless">
          <a v-on:click="previewModImg" class="button is-neon-cyan" v-bind:class="{'is-loading': MOD_IS_PREVIEWING, 'is-static': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-eye"></i>
            </span>
            <span>Preview</span>
          </a>
          <a v-on:click="clearPrevImage" class="button is-neon-white" v-bind:class="{'is-static': buttonIsFrozen}">
            <span class="icon is-small">
              <i class="fas fa-trash-alt"></i>
            </span>
            <span>Clear</span>
          </a>
          <a v-on:click="toggleNewCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': new_checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </td>
        <td colspan="2">
        </td>
      </tr>
      <tr>
        <td style="width: 288px; height: 275px;" colspan="3" class="is-paddingless silver-bordered">
          <div class="mod-orig-info-container">
            <table class="table mod-orig-info-table is-hpaddingless">
              <tbody>
                <tr>
                  <td class="mod-info-label is-cyan">Name</td>
                  <td class="mod-info-data">
                    <span v-if="orig_name">{{ orig_name }}</span>
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
                    <span v-if="orig_file_size_hr">{{ orig_file_size_hr }}</span>
                    <span v-else>-</span>
                  </td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Format</td>
                  <td class="mod-info-data">
                    <span v-if="orig_file_size_hr">{{ orig_format }}</span>
                    <span v-else>-</span>
                  </td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Total frames</td>
                  <td class="mod-info-data">
                    <span v-if="orig_frame_count">{{ orig_frame_count }} ({{ orig_frame_count_ds }})</span>
                    <span v-else>-</span>
                  </td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Frame rate</td>
                  <td class="mod-info-data">
                    <span v-if="orig_fps">{{ orig_fps }}</span>
                    <span v-else>-</span>
                  </td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Frame delay</td>
                  <td class="mod-info-data">
                    <span v-if="orig_fps">{{ orig_delay_info }}</span>
                    <span v-else>-</span>
                  </td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Loop duration</td>
                  <td class="mod-info-data">
                    <span v-if="orig_loop_duration">{{ orig_loop_duration }} seconds</span>
                    <span v-else>-</span>
                    </td>
                </tr>
                <tr>
                  <td class="mod-info-label is-cyan">Loop count</td>
                  <td class="mod-info-data">
                    <template v-if="orig_path">
                      <span v-if="orig_loop_count == 0">Infinite</span>
                      <span v-else>{{ orig_loop_count }}</span>
                    </template>
                    <template v-else>-</template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </td>
        <td style="width: 532px; height: 275px;" colspan="5"
          class="has-text-centered is-paddingless silver-bordered-left-thicc">
          <div class="mod-aimg-control-container">
            <table class="table is-paddingless is-marginless" width="100%">
              <tr>
                <td width="10%" class="mod-menu-subtab is-paddingless">
                  <div class="mod-left-menu">
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
                            v-bind:class="{'is-disabled': format == 'PNG'}">
                            <span class="icon is-large">
                              <i class="far fa-images fa-2x fa-inverse"></i>
                            </span>
                            <p class="is-white-d is-large">GIF</p>
                          </a>
                        </li>
                        <li id="MOD_box_apng" class="subtab-menu-item"
                          v-bind:class="{'is-selected': mod_menuselection == 2}">
                          <a id="MOD_menu_apng" v-on:click="mod_menuselection = 2"
                            v-bind:class="{'is-disabled': format == 'GIF'}">
                            <span class="icon is-large">
                              <i class="far fa-images fa-2x fa-inverse"></i>
                            </span>
                            <p class="is-white-d is-large">APNG</p>
                          </a>
                        </li>
                      </ul>
                    </aside>
                  </div>
                </td>
                <td width="90%" class="is-paddingless">
                  <div v-show="mod_menuselection == 0">
                    <table class="table mod-new-control-table is-hpaddingless" width="100%">
                      <tr>
                        <td width="40%" colspan="2">
                          <div class="field">
                            <label class="label">Name</label>
                            <div class="control">
                              <input v-model="name" class="input is-neon-white" type="text" />
                            </div>
                          </div>
                        </td>
                        <td width="20%">
                          <div class="field">
                            <label class="label">Width</label>
                            <div class="control">
                              <input v-bind:value="width" v-on:keydown="numConstrain($event, true, true)" v-on:input="widthHandler(width, $event)" 
                                class="input is-neon-white" type="number" min="1" step="1"/>
                            </div>
                          </div>
                        </td>
                        <td width="20%">
                          <div class="field">
                            <label class="label">Height</label>
                            <div class="control">
                              <input v-bind:value="height" v-on:keydown="numConstrain($event, true, true)" v-on:input="heightHandler(height, $event)"
                              class="input is-neon-white" type="number" min="1" step="1"/>
                            </div>
                          </div>
                        </td>
                        <td width="20%">
                          <div class="field">
                            <label class="label">Rotation</label>
                            <div class="control">
                              <input v-model="rotation" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" />
                            </div>
                          </div>
                        </td>
                      </tr>
                      <tr>
                        <td width="20%">
                          <div class="field">
                            <label class="label">FPS</label>
                            <div class="control">
                              <input v-model="fps" v-on:input="fpsConstrain" v-on:keydown="numConstrain($event, true, false)" class="input is-neon-white" type="number" min="0"/>
                            </div>
                          </div>
                        </td>
                        <td width="20%">
                          <div class="field">
                            <label class="label">Delay</label>
                            <div class="control">
                              <input v-model="delay" v-on:input="delayConstrain" v-on:keydown="numConstrain($event, true, false)" class="input is-neon-white" type="number" min="0"/>
                            </div>
                          </div>
                        </td>
                        <td width="20%">
                          <div class="field">
                            <label class="label">Loop count</label>
                            <div class="control">
                              <input v-model="loop_count" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0"/>
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
                        <td width="20%">
                          <div class="field">
                            <label class="label">Format</label>
                            <div class="control">
                              <div class="select is-neon-cyan">
                                <select v-model="format">
                                  <option value="GIF">GIF</option>
                                  <option value="PNG">APNG</option>
                                </select>
                              </div>
                            </div>
                          </div>
                        </td>
                      </tr>
                      <tr>
                        <td width="20%" class="force-vcenter">
                          <label class="checkbox" title="Flip the image horizontally">
                            <input v-model="flip_x" type="checkbox" />
                            Flip X
                          </label>
                          <label class="checkbox" title="Flip the image vertically">
                            <input v-model="flip_y" type="checkbox" />
                            Flip Y
                          </label>
                        </td>
                        <td width="40%" class="force-vcenter" colspan="2">
                          <label class="checkbox" title="Reverse the animation">
                            <input v-model="is_reversed" type="checkbox" />
                            Reversed
                          </label>
                          <!-- <label class="checkbox" title="Preserve transparent pixels">
                            <input v-model="preserve_alpha" type="checkbox" />
                            Preserve Alpha
                          </label> -->
                          <label class="checkbox">
                            <input v-model="lock_aspect_ratio" type="checkbox"/>
                            Lock aspect ratio
                          </label>
                        </td>
                        <td width="40%" class="force-vcenter" colspan="2">
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
                        <td colspan="4">
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
                          <a v-on:click="modifyImage" class="button is-neon-cyan"  v-bind:class="{'is-loading': MOD_IS_MODIFYING, 'is-static': buttonIsFrozen}">
                            MODIFY</a>
                        </td>
                      </tr>
                    </table>
                  </div>
                  <div v-show="mod_menuselection == 1">
                    <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
                      <GIFOptimizationRow
                        :is_optimized.sync="is_optimized"
                        :optimization_level.sync="optimization_level"
                        :is_lossy.sync="is_lossy"
                        :lossy_value.sync="lossy_value"
                        :is_reduced_color.sync="is_reduced_color"
                        :color_space.sync="color_space"
                        :is_unoptimized.sync="is_unoptimized"
                      />
                      <GIFUnoptimizationRow
                      :is_optimized.sync="is_optimized"
                      :is_lossy.sync="is_lossy"
                      :is_reduced_color.sync="is_reduced_color"
                      :is_unoptimized.sync="is_unoptimized"
                      />
                    </table>
                  </div>
                  <div v-show="mod_menuselection == 2">
                    <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
                      <APNGOptimizationRow
                        :apng_is_optimized.sync="apng_is_optimized"
                        :apng_optimization_level.sync="apng_optimization_level"
                        :apng_is_lossy.sync="apng_is_lossy"
                        :apng_lossy_value.sync="apng_lossy_value"
                        :apng_is_unoptimized.sync="apng_is_unoptimized"
                      />
                      <APNGUnoptimizationRow
                        :apng_is_optimized.sync="apng_is_optimized"
                        :apng_is_lossy.sync="apng_is_lossy"
                        :apng_is_unoptimized.sync="apng_is_unoptimized"
                      />
                    </table>
                  </div>
                </td>
              </tr>
            </table>
          </div>
        </td>
      </tr>
      <tr>
        <td colspan="8" class="is-paddingless" style="vertical-align: middle;">
          <input v-model="modify_msgbox" type="text" class="input is-paddingless is-border-colorless" readonly="readonly"/>
        </td>
      </tr>
    </table>
    <!-- </div> -->
  </div>
</template>

<script>

const remote = require('electron').remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.vue');
const { GIF_DELAY_DECIMAL_PRECISION, randString, wholeNumConstrain, posWholeNumConstrain, floatConstrain, numConstrain, gcd, validateFilename,
        fileExists } = require("./Utility.vue");
import GIFOptimizationRow from "./vueshards/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./vueshards/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./vueshards/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./vueshards/APNGUnoptimizationRow.vue";


var data = {
  orig_name: "",
  orig_width: "",
  orig_height: "",
  orig_frame_count: "",
  orig_frame_count_ds: "",
  orig_fps: "",
  orig_delay: "",
  orig_delay_info: "",
  orig_loop_duration: "",
  orig_loop_count: "",
  orig_file_size: "",
  orig_file_size_hr: "",
  orig_format: "",
  orig_path: "",
  name: "",
  old_width: "",
  width: "",
  old_height: "",
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
  is_optimized: false,
  optimization_level: "1",
  is_lossy: false,
  lossy_value: "",
  is_reduced_color: false,
  color_space: "",
  is_unoptimized: false,
  apng_is_optimized: false,
  apng_optimization_level: "1",
  apng_is_lossy: false,
  apng_lossy_value: "",
  apng_is_unoptimized: false,
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
  data.orig_name = "";
  data.orig_width = "";
  data.orig_height = "";
  data.orig_frame_count = "";
  data.orig_frame_count_ds = "";
  data.orig_fps = "";
  data.orig_delay = "";
  data.orig_delay_info = "";
  data.orig_loop_duration = "";
  data.orig_loop_count = "";
  data.orig_file_size = "";
  data.orig_file_size_hr = "";
  data.orig_format = "";
  data.orig_path = "";
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
  dialog.showOpenDialog(mainWindow, options, (chosen_path) => {
    console.log(`chosen path: ${chosen_path}`);
    if (chosen_path === undefined || chosen_path.length == 0) {
      return;
    }
    data.MOD_IS_LOADING = true;
    client.invoke("inspect_one", chosen_path[0], "animated", (error, res) => {
      if (error) {
        console.error(error);
        data.modify_msgbox = error;
        // mboxError(modify_msgbox, error);
      } else {
        loadOrigInfo(res);
        loadNewInfo(res);
        data.modify_msgbox = "";
      }
      data.MOD_IS_LOADING = false;
    });
    console.log("registered!");
  });
}

function loadOrigInfo(res) {
  let geninfo = res.general_info;
  let ainfo = res.animation_info;
  data.orig_name = geninfo.name.value;
  data.orig_width = geninfo.width.value;
  data.orig_height = geninfo.height.value;
  data.orig_fps = `${ainfo.fps.value} fps`;
  data.orig_frame_count= ainfo.frame_count.value;
  data.orig_frame_count_ds= ainfo.frame_count_ds.value;
  data.orig_format = geninfo.format.value;
  let delay_info = `${ainfo.avg_delay.value} seconds`;
  if (ainfo.delay_is_uneven) {
    delay_info += ` (uneven)`;
  }
  data.orig_delay = ainfo.avg_delay.value;
  data.orig_delay_info = delay_info;
  data.orig_loop_duration = ainfo.loop_duration.value;
  data.orig_loop_count = ainfo.loop_count.value;
  data.orig_path = geninfo.absolute_url.value;
  data.orig_file_size = geninfo.fsize.value;
  data.orig_file_size_hr = geninfo.fsize_hr.value;
}

function loadNewInfo(res) {
  var geninfo = res.general_info;
  var ainfo = res.animation_info;
  data.name = geninfo.base_fname.value;
  data.format = geninfo.format.value;
  data.width = geninfo.width.value;
  data.height = geninfo.height.value;
  data.delay = ainfo.avg_delay.value;
  data.fps = ainfo.fps.value;
  data.loop_count = ainfo.loop_count.value;
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
  // console.log("delay event", event);
  var value = event.target.value;
  console.log(value);
  if (value && value.includes(".")) {
    var numdec = value.split(".");
    console.log("numdec", numdec);
    if (numdec[1].length > GIF_DELAY_DECIMAL_PRECISION) {
      var twodecs = numdec[1].substring(0, GIF_DELAY_DECIMAL_PRECISION);
      // console.log("twodecs limit triggered", twodecs);
      data.delay = `${numdec[0]}.${twodecs}`;
    }
  }
  data.fps = Math.round(1000 / data.delay) / 1000;
}

function fpsConstrain (event) {
  console.log("fps event", event);
  var value = event.target.value;
  if (value) {
    data.delay = Math.round(100 / data.fps) / 100;
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
