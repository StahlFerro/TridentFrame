<template>
  <div id="create_panel" class="container" style="padding:10px;">
    <table class="table is-borderless" style="padding: 5px;" width="100%">
      <tr>
        <td
          id="CRT_sequence_cell"
          class="silver-bordered is-paddingless"
          style="width: 500px; height: 320px;"
        >
          <table class="sequence-grid is-paddingless" width="100%">
            <tbody>
              <tr v-for="(quintjson, row) in CRTQuintcellLister" v-bind:key="row">
                <!-- <template v-for="(item, i) in quintjson">
                  <template v-if="item == '_CONTROL_CELL'"> -->
                    <!-- <td v-bind:key="i" class="force-center">
                      <table class="intracell-table" width="100%">
                        <tr>
                          <td width="50%" class="">
                            <a v-on:click="loadImages('insert')" class="button square-button is-medium flex-expand is-neon-emerald neon-borderless"
                               title="Add Images. Select one or more images to be added into this sequence">
                              <span class="icon is-small">
                                <i class="fas fa-image"></i>
                              </span>
                            </a>
                          </td>
                          <td class="">
                            <a v-on:click="loadImages('smart_insert')" class="button square-button is-medium flex-expand is-neon-emerald neon-borderless"
                              title="Smart Add Image. Select one images and then let TridentFrame add the rest of the sequence by looking at images with the same name">
                              <span class="icon is-small">
                                <i class="fas fa-images"></i>
                              </span>
                            </a>
                          </td>
                        </tr>
                        <tr>
                          <td width="100%" colspan="2" class="">
                            <label class="label" title="The frame number in which new frames will be inserted after. Leave blank as default (insert new ones after the last on the existing sequence)">
                              Insert after</label>
                            <input v-model="insert_index" class="input is-block-grey" type="number" v-on:keydown="numConstrain($event, true, true)" placeholder="Frame no." min="0"
                             title="The frame number in which new frames will be inserted after. Leave blank as default (insert new ones after the last on the existing sequence)"/>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </template>
                  <template v-else> -->
                    <td v-for="(item, i) in quintjson" v-bind:key="i" v-bind:title="
                          `Name: ${item.name.value}\n` + 
                          `Dimensions: ${item.width.value} x ${item.height.value}\n` +
                          `Format: ${item.format.value}\n` +
                          `Mode: ${item.color_mode.value}\n` +
                          `Comment: ${item.comments.value || 'None'}`
                        ">
                      <div class="seqdiv">
                        <!-- <span>{{ i }}</span><br/> -->
                        <img v-bind:src="item.absolute_url.value"/>
                        <span class="index-anchor">
                          {{ parseInt(row) * 5 + parseInt(i) + 1 }}
                        </span>
                        <a class="del-anchor" v-on:click="removeFrame(parseInt(row) * 5 + parseInt(i))">
                          <span class="icon" v-on:click="removeFrame(parseInt(row) * 5 + parseInt(i))">
                            <i class="fas fa-minus-circle" v-on:click="removeFrame(parseInt(row) * 5 + parseInt(i))"></i>
                          </span>
                        </a>
                      </div>
                    </td>
                  <!-- </template>
                </template> -->

              </tr>
            </tbody>
          </table>
        </td>
        <td
          id="create_aimg_cell"
          class="silver-bordered force-center is-paddingless"
          style="width: 320px; height: 320px;"
          v-bind:class="{'has-checkerboard-bg': checkerbg_active}">
          <!-- <div v-if="preview_info" class="crt-aimg-container"> -->
            <div v-if="preview_info" class="crt-aimg-container" v-bind:title="
              `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
              `File size: ${preview_info.general_info.fsize_hr.value}\n` +
              `FPS: ${preview_info.animation_info.fps.value}\n` +
              `Duration: ${preview_info.animation_info.loop_duration.value} seconds\n` +
              `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
              `Format: ${preview_info.general_info.format.value}`
            ">
              <img v-bind:src="preview_path_cb"/>
            </div>
          <!-- </div> -->
        </td>
      </tr>
      <tr>
        <td class="is-hpaddingless">
          <nav class="level">
            <div class="level-left">
              <div class="level-item has-text-centered">
                <div>
                  <a v-on:click="loadImages('insert')" class="button is-neon-emerald" v-bind:class="{'is-loading': CRT_INSERT_LOAD, 'is-static': isButtonFrozen}">
                    <span class="icon is-small">
                      <i class="fas fa-plus"></i>
                    </span>
                    <span>Add</span>
                  </a>
                  <a v-on:click="loadImages('smart_insert')" class="button is-neon-emerald" v-bind:class="{'is-loading': CRT_SMARTINSERT_LOAD, 'is-static': isButtonFrozen}">
                    <span class="icon is-small">
                      <i class="fas fa-plus-circle"></i>
                    </span>
                    <span>Smart</span>
                  </a>
                  <div class="dualine-label">
                    <span>Insert<br/>after</span>
                  </div>
                  <input v-model="insert_index" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0" style="width: 70px;"/>
                  <a v-on:click="loadImages('replace')" class="button is-neon-emerald" v-bind:class="{'is-loading': CRT_REPLACE_LOAD, 'is-static': isButtonFrozen}"
                    title="Loads multiple static images to create an animated image. This replaces the current sequence above">
                    <span class="icon is-small">
                      <i class="fas fa-plus-square"></i>
                    </span>
                    <span>Load</span>
                  </a>
                  <a v-on:click="CRTClearAIMG" class="button is-neon-crimson" v-bind:class="{'is-static': isButtonFrozen}">
                    <span class="icon is-small">
                      <i class="fas fa-trash-alt"></i>
                    </span>
                    <span>Clear</span>
                  </a>
                </div>
              </div>
              <div class="level-item has-text-centered">
                <div>
                </div>
              </div>
              <!-- <div class="level-item has-text-right">
                <div>
                  <p>{{ sequenceCounter }}</p>
                </div>
              </div> -->
            </div>
          </nav>
        </td>
        <td class="has-text-left is-paddingless" style="vertical-align: middle;">
          <nav class="level">
            <div class="level-item has-text-centered">
              <div>
                <a v-on:click="previewAIMG" class="button is-neon-cyan" v-bind:class="{'is-loading': CRT_IS_PREVIEWING, 'is-static': isButtonFrozen}">
                  <span class="icon is-medium">
                    <i id="autoprev_icon" class="far fa-eye"></i>
                  </span>
                  <span>Preview</span>
                </a>
                <a v-on:click="CRTToggleCheckerBG" class="button is-neon-white" v-bind:class="{'is-active': checkerbg_active}">
                  <span class="icon is-medium">
                    <i class="fas fa-chess-board"></i>
                  </span>
                </a>
              </div>
            </div>
          </nav>
        </td>
      </tr>
      <tr>
        <td id="CRT_control_cell" class="silver-bordered is-paddingless" colspan="2">
          <div class="crt-aimg-control-container">
          <table class="table is-paddingless is-marginless" width="100%" height="100%">
            <tr>
              <td width="5%" class="crt-menu-subtab is-paddingless">
                <div class="crt-left-menu">
                  <aside class="menu has-text-centered" style="margin: 0;">
                    <ul class="menu-list">
                      <li class="subtab-menu-item"
                        v-bind:class="{'is-selected': crt_menuselection == 0}">
                        <a v-on:click="crt_menuselection = 0">
                          <span class="icon is-large">
                            <i class="fas fa-image fa-2x fa-inverse"></i>
                          </span>
                          <p class="is-white-d">General</p>
                        </a>
                      </li>
                      <li class="subtab-menu-item is-cyan"
                        v-bind:class="{'is-selected': crt_menuselection == 1}">
                        <a v-on:click="crt_menuselection = 1"
                          v-bind:class="{'is-disabled': format == 'PNG'}">
                          <span class="icon is-large">
                            <i class="far fa-images fa-2x fa-inverse"></i>
                          </span>
                          <p class="is-white-d is-large">GIF</p>
                        </a>
                      </li>
                      <li class="subtab-menu-item"
                        v-bind:class="{'is-selected': crt_menuselection == 2}">
                        <a v-on:click="crt_menuselection = 2"
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
              <td width="95%" class="is-paddingless">                
                <div v-show="crt_menuselection == 0">
                  <table class="table crt-control-table" width="100%">
                    <tr>
                      <td width="16.7%">
                        <div class="field">
                          <label class="label" title="The name of the GIF/APNG">Name</label>
                          <div class="control">
                            <input v-model="name" class="input is-neon-white" type="text" />
                          </div>
                        </div>
                      </td>
                      <td width="16.7%">
                        <div class="field">
                          <label class="label" title="The width of the GIF/APNG">Width</label>
                          <div class="control">
                            <input v-bind:value="width" v-on:keydown="numConstrain($event, true, true)" v-on:input="widthHandler(width, $event)" 
                            class="input is-neon-white" type="number" min="1"/>
                          </div>
                        </div>
                      </td>
                      <td width="16.7%">
                        <div class="field">
                          <label class="label" title="The height of the GIF/APNG">Height</label>
                          <div class="control">
                            <input v-bind:value="height" v-on:keydown="numConstrain($event, true, true)" v-on:input="heightHandler(height, $event)"
                            class="input is-neon-white" type="number" min="1"/>
                          </div>
                        </div>
                      </td>
                      <td width="16.7%">
                        <div class="field">
                          <label class="label" title="Which algorithm to use when resizing the image. Default is Bicubic">Resize Method</label>
                          <div class="control">
                            <div class="select is-neon-cyan">
                              <select v-model="resize_method">
                                <option value="BICUBIC" title="General-use resizing algorithm for most images">Bicubic</option>
                                <option value="NEAREST" title="Preserve sharp edges. Ideal for pixel art">Nearest</option>
                                <option value="BILINEAR" title="Similar to Bicubic, but not as smooth">Bilinear</option>
                                <option value="BOX">Box</option>
                                <option value="HAMMING">Hamming</option>
                                <option value="LANCZOS">Lanczos</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td width="16.7%" style="vertical-align: bottom;">
                        <label class="checkbox">
                          <input v-model="lock_aspect_ratio" type="checkbox"/>
                          Lock aspect ratio
                        </label>
                        <br/>
                        <template v-if="aspect_ratio && aspect_ratio.text">
                          <input v-model="aspect_ratio.text" class="input is-border-colorless is-paddingless" style="height: 1.5em;" readonly="readonly"/>
                        </template>
                        <template v-else>&nbsp;</template>
                      </td>
                      <td width="16.7%">
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div class="field">
                          <label class="label" title="The time needed to move to the next frame">Delay (seconds)</label>
                          <div class="control">
                            <input v-model="delay" v-on:keydown="numConstrain($event, true, false)" v-on:input="delayConstrain" class="input is-neon-white" type="number" min="0" />
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="field">
                          <label class="label" title="How many frames will be consecutively displayed per second.">Frame rate</label>
                          <div class="control">
                            <input v-model="fps" v-on:keydown="numConstrain($event, true, false)" v-on:input="fpsConstrain" class="input is-neon-white" type="number" min="0" max="50" step="0.01"/>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="field">
                          <label class="label" title="How many times the GIF/APNG will loop. Zero/blank for infinite loop">Loop count</label>
                          <div class="control">
                            <input v-model="loop_count" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0" max="999" step="1"/>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="field">
                          <label class="label" title="Choose which frame to start the animation from. Default is 1 (is also 1 if left blank or typed 0)">Start at frame</label>
                          <div class="control">
                            <input v-model="start_frame" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0" step="1"/>
                          </div>
                        </div>
                      </td>
                      <td style="vertical-align: bottom;">
                        <label class="checkbox" title="Flip the image horizontally">
                          <input v-model="flip_x" type="checkbox" />
                          Flip X
                        </label>
                        <br />
                        <label class="checkbox" title="Flip the image vertically">
                          <input v-model="flip_y" type="checkbox" />
                          Flip Y
                        </label>
                      </td>
                      <td style="vertical-align: bottom;">
                        <label class="checkbox" title="Preserve transparent pixels">
                          <input v-model="is_transparent" type="checkbox" />
                          Preserve Alpha
                        </label>
                        <br />
                        <label class="checkbox" title="Reverse the animation">
                          <input v-model="is_reversed" type="checkbox" />
                          Reversed
                        </label>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="4" style="padding-top: 15px;">
                        <div class="field has-addons">
                          <div class="control">
                            <a class="button is-neon-cyan" v-on:click="CRTChooseOutdir">
                              <span class="icon is-small">
                                <i class="fas fa-folder-open"></i>
                              </span>
                              <span>Save to</span>
                            </a>
                          </div>
                          <div class="control is-expanded">
                            <input
                              v-model="outdir"
                              class="input is-neon-white"
                              type="text"
                              placeholder="Output folder"
                              readonly
                            />
                          </div>
                        </div>
                      </td>
                      <td colspan="1" style="padding-top: 15px;">
                        <div class="field">
                          <!-- <label class="label">Format</label> -->
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
                      <td colspan="1" style="padding-top: 15px;">
                        <div class="field has-text-centered">
                          <div class="control">
                            <a v-on:click="CRTCreateAIMG" class="button is-neon-cyan" 
                              v-bind:class="{'is-loading': CRT_IS_CREATING == true, 'is-static': isButtonFrozen}">Create</a>
                          </div>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td colspan="6">
                        <input v-model="create_msgbox" type="text" class="input is-left-paddingless is-border-colorless" readonly="readonly"/>
                      </td>
                    </tr>
                  </table>

                </div>
                <div v-show="crt_menuselection == 1">
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
                    <!-- <GIFUnoptimizationRow
                      :is_optimized.sync="is_optimized"
                      :is_lossy.sync="is_lossy"
                      :is_reduced_color.sync="is_reduced_color"
                      :is_unoptimized.sync="is_unoptimized"
                    /> -->
                  </table>
                </div>
                <div v-show="crt_menuselection == 2">
                  <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
                    <APNGOptimizationRow
                      :apng_is_optimized.sync="apng_is_optimized"
                      :apng_optimization_level.sync="apng_optimization_level"
                      :apng_is_lossy.sync="apng_is_lossy"
                      :apng_lossy_value.sync="apng_lossy_value"
                      :apng_is_unoptimized.sync="apng_is_unoptimized"
                    />
                    <!-- <APNGUnoptimizationRow
                      :apng_is_optimized.sync="apng_is_optimized"
                      :apng_is_lossy.sync="apng_is_lossy"
                      :apng_is_unoptimized.sync="apng_is_unoptimized"
                    /> -->
                  </table>
                </div>
              </td>
            </tr>
          </table>
          </div>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
const remote = require("electron").remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const session = remote.getCurrentWebContents().session;
const { client } = require("./Client.vue");
import { quintcellLister, validateFilename, GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION,
  randString, gcd, numConstrain, fileExists } from "./Utility.vue";
import GIFOptimizationRow from "./vueshards/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./vueshards/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./vueshards/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./vueshards/APNGUnoptimizationRow.vue";

var data = {
  crt_menuselection: 0,
  image_paths: [],
  sequence_info: [],
  insert_index: "",
  name: "",
  fps: "",
  orig_width: "",
  old_width: "",
  orig_height: "",
  old_height: "",
  width: "",
  height: "",
  resize_method: "BICUBIC",
  delay: "",
  loop_count: "",
  start_frame: "",
  is_transparent: false,
  is_reversed: false,
  flip_x: false,
  flip_y: false,
  rotation: 0,
  format: "GIF",
  outdir: "",
  preview_path: "",
  preview_path_cb: "",
  preview_info: "",
  aspect_ratio: "",
  lock_aspect_ratio: false,

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

  create_msgbox: "",
  // sequence_counter: "",
  checkerbg_active: false,
  CRT_INSERT_LOAD: false,
  CRT_SMARTINSERT_LOAD: false,
  CRT_REPLACE_LOAD: false,
  CRT_IS_LOADING: false,
  CRT_IS_PREVIEWING: false,
  CRT_IS_CREATING: false,
}

let extension_filters = [{ name: "Images", extensions: ["png", "gif"] }];
let img_dialog_props = ["openfile"];
let imgs_dialog_props = ["openfile", "multiSelections", "createDirectory"];
let dir_dialog_props = ["openDirectory", "createDirectory"];



function toggleLoadButtonAnim(ops, state=false) {
  if (ops == 'insert') {
    data.CRT_INSERT_LOAD = state;
  }
  else if (ops == 'smart_insert') {
    data.CRT_SMARTINSERT_LOAD = state;
  }
  else if (ops == 'replace') {
    data.CRT_REPLACE_LOAD = state;
  }
}



function loadImages(ops) {
  // ops are between 'replace', 'insert' or 'smart_insert'
  console.log("crt load image with ops:", ops);
  let props = ops == 'smart_insert'? img_dialog_props : imgs_dialog_props;
  console.log('obtained props', props);
  var options = {
    filters: extension_filters,
    properties: props,
  }

  dialog.showOpenDialog(mainWindow, options, (img_paths) => {
    console.log(img_paths);
    if (img_paths === undefined || img_paths.length == 0) { return; }
    data.CRT_IS_LOADING = true;
    toggleLoadButtonAnim(ops, true);

    client.invoke("inspect_many", img_paths, (error, res) => {
      if (error) {
        console.error(error);
        data.create_msgbox = error;
        data.CRT_IS_LOADING = false;
      } else {
        console.log(res);
        if (res && res.msg) {
          console.log('msg executed');
          data.create_msgbox = res.msg;
        }
        else if (res && res.data) {
          let info = res.data;
          console.log('sequence info');
          console.log(info.sequence_info);
          // data.image_paths = info.sequence;
          // data.sequence_info = info.sequence_info;
          renderSequence(info, {operation: ops})
          data.name = info.name;
          // data.sequence_counter = `${info.total} image${info.total > 1 ? "s" : ""} (${info.size})`;
          data.orig_width = info.width;
          data.width = info.width;
          data.orig_height = info.height;
          data.height = info.height;
          data.fps = 50;
          data.delay = 0.02;
          data.create_msgbox = "";
          updateAspectRatio(data.width, data.height);
          data.CRT_IS_LOADING = false;
          toggleLoadButtonAnim(ops, false);
        }
      }
    });
  });
}


function renderSequence(pyinfo, options) {
  let operation = options.operation;
  if (operation == 'replace') {
    console.log("AA");
    data.image_paths = pyinfo.sequence;
    data.sequence_info = pyinfo.sequence_info;
  }
  else if (['insert', 'smart_insert'].includes(operation)) {
    console.log("BB");
    if (data.insert_index) {
      data.image_paths.splice(data.insert_index, 0, ...pyinfo.sequence);
      data.sequence_info.splice(data.insert_index, 0, ...pyinfo.sequence_info);
    }
    else {
      data.image_paths.push(...pyinfo.sequence);
      data.sequence_info.push(...pyinfo.sequence_info);
    }
  }
}


function removeFrame(index){
 data.image_paths.splice(index, 1);
 data.sequence_info.splice(index, 1);
}

function CRTChooseOutdir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options, (out_dirs) => {
    console.log(out_dirs)
    if (out_dirs && out_dirs.length > 0) {
      console.log("folder selected");
      data.outdir = out_dirs[0];
      data.create_msgbox = "";
    }
  });
  // mboxClear(create_msgbox);
}

function CRTClearAIMG() {
  data.image_paths = [];
  data.sequence_info = [];
  data.preview_path = "";
  data.preview_path_cb = "";
  data.preview_info = "";
  data.name = "";
  data.delay = "";
  data.fps = "";
  data.loop_count = "";
  data.orig_width = "";
  data.old_width = "";
  data.width = "";
  data.orig_height = "";
  data.old_height = "";
  data.height = "";
  // data.CRT_sequence_counter = "";
  data.create_msgbox = "";
  // data.sequence_counter = "";
  let ARData = {
    "w_ratio": "",
    "h_ratio": "",
    "text": "",
  };
  data.aspect_ratio = ARData;
  // mboxClear(create_msgbox);
  // deleteTempAIMG();
  // session.clearCache(testcallback);
}

function previewAIMG() {
  console.log("preview called");
  data.create_msgbox = "";
  let validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.create_msgbox = validator.msg;
    return;
  }
  data.CRT_IS_PREVIEWING = true;
  client.invoke("combine_image", data.image_paths, "./temp", data.name, data, (error, res) => {
    if (error) {
      console.error(error);
      data.create_msgbox = error;
      data.CRT_IS_PREVIEWING = false;
    } else {
      if (res) {
        console.log(res);
        if (res.msg) {
          data.create_msgbox = res.msg;
        }
        if (res.preview_path) {
          data.preview_path = res.preview_path;
          previewPathCacheBreaker();
        }
        if (res.CONTROL == "CRT_FINISH") {
          client.invoke("inspect_one", data.preview_path, "animated", (error, info) => {
            if (error) {
              console.error(error);
              data.CRT_IS_PREVIEWING = false;
            } else {
              console.log("preview inspect");
              console.log(info);
              data.preview_info = info;
              data.create_msgbox = "Previewed!"
              data.CRT_IS_PREVIEWING = false;
            }
          });
        }
      }
    }
  });
}

function CRTCreateAIMG() {
  let proceed_create = true;
  data.create_msgbox = "";
  var validator = validateFilename(data.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.create_msgbox = validator.msg;
    return;
  }

  if (fileExists(data.outdir, `${data.name}.${data.format.toLowerCase()}`)) {
    let WINDOW = remote.getCurrentWindow();
    let options = {
      buttons: ["Yes", "Cancel"],
      message: "A file with the same name already exists in the output folder. Do you want to override it?"
    };
    let response = dialog.showMessageBoxSync(WINDOW, options);
    if (response == 1) proceed_create = false;
  }

  if (proceed_create) {
    data.CRT_IS_CREATING = true;
    client.invoke("combine_image", data.image_paths, data.outdir, data.name, data, (error, res) => {
      if (error) {
        console.error(error);
        data.create_msgbox = error;
        data.CRT_IS_CREATING = false;
      } else {
        if (res) {
          console.log(res);
          if (res.msg) {
            data.create_msgbox = res.msg;
          }
          if (res.CONTROL == "CRT_FINISH") {
            data.create_msgbox = `${data.format.toUpperCase()} created!`;
            data.CRT_IS_CREATING = false;
          }
        }
      }
    });
  }
}

function CRTToggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log('now checkerbg is', data.checkerbg_active);
}

function isButtonFrozen() {
  if (data.CRT_IS_LOADING || data.CRT_IS_PREVIEWING || data.CRT_IS_CREATING) return true;
  else return false;
}

// function getFPS() {
//   return Math.round(1/data.delay * 1000) / 1000;
// }

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

function CRTQuintcellLister() {
  return quintcellLister(data.sequence_info);
}

function sequenceCounter() {
  if (data.sequence_info.length > 0) {
    return `${data.sequence_info.length} images`;
  }
  else return "";
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
    loadImages: loadImages,
    removeFrame: removeFrame,
    CRTClearAIMG: CRTClearAIMG,
    CRTChooseOutdir: CRTChooseOutdir,
    previewAIMG: previewAIMG,
    CRTCreateAIMG: CRTCreateAIMG,
    CRTToggleCheckerBG: CRTToggleCheckerBG,
    numConstrain: numConstrain,
    widthHandler: widthHandler,
    heightHandler: heightHandler,
    delayConstrain: delayConstrain,
    fpsConstrain: fpsConstrain,
    removeFrame: removeFrame,
  },
  computed: {
    CRTQuintcellLister: CRTQuintcellLister,
    isButtonFrozen: isButtonFrozen,
    sequenceCounter: sequenceCounter,
  },
};
</script>
