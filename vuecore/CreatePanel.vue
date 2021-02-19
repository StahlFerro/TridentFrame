<template>
  <div id="create_panel">
    <div class="create-panel-root">
      <div class="create-panel-display">
        <div class="create-panel-sequence silver-bordered">
          <div class="rtable rtable-5cols">
            <div class="rtable-cell" v-for="(item, index) in sequence_info" v-bind:key="index"
              v-bind:title="sequence_info?                    
                `Name: ${item.name.value}\n` +
                `Dimensions: ${item.width.value} x ${item.height.value}\n` +
                `Format: ${item.format.value}\n` +
                `Mode: ${item.color_mode.value}\n` +
                `Comment: ${item.comments.value || 'None'}` : ''
              ">
              <img v-bind:src="item.absolute_url.value" />
              <span class="index-anchor is-white-d">
                {{ parseInt(index) + 1 }}
              </span>
              <a class="del-anchor" v-on:click="removeFrame(parseInt(index))">
                <span class="icon" v-on:click="removeFrame(parseInt(index))">
                  <i class="fas fa-minus-circle" v-on:click="removeFrame(parseInt(index))"
                  ></i>
                </span>
              </a>
            </div>
          </div>

          <!-- <table class="sequence-grid is-paddingless" width="100%">
            <tbody>
              <tr v-for="(quintjson, row) in CRTQuintcellLister" v-bind:key="row">
                <td v-for="(item, i) in quintjson" v-bind:key="i"
                  v-bind:title="
                    `Name: ${item.name.value}\n` +
                    `Dimensions: ${item.width.value} x ${item.height.value}\n` +
                    `Format: ${item.format.value}\n` +
                    `Mode: ${item.color_mode.value}\n` +
                    `Comment: ${item.comments.value || 'None'}`
                  "
                >
                  <div class="seqdiv">
                    <img v-bind:src="item.absolute_url.value" />
                  </div>
                </td>
              </tr>
            </tbody>
          </table> -->

        </div>
        <div class="create-panel-preview silver-bordered-no-left"
          v-bind:title="preview_info? 
            `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
            `File size: ${preview_info.general_info.fsize_hr.value}\n` +
            `FPS: ${preview_info.animation_info.fps.value}\n` +
            `Duration: ${preview_info.animation_info.loop_duration.value} seconds\n` +
            `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
            `Format: ${preview_info.general_info.format.value}` : ''
          ">
          <!-- <div v-if="preview_info" class="crt-aimg-container"> -->
          <img v-if="preview_info" v-bind:src="preview_path_cb" />
          <!-- </div> -->
        </div>
      </div>

      <div class="create-panel-middlebar">
        <div id="crtLoadPopper" class="context-menu" ref="popper" v-show="popperIsVisible" tabindex="-1" style="display: block;">
          <ul class="context-menu-options">
            <li class="context-menu-option" @click="loadImages('insert')">
              <div class="ctxmenu-content">
                <div class="ctxmenu-icon">
                  <span class="icon is-small"><i class="fas fa-plus"></i></span>
                </div>
                <div class="ctxmenu-text"><span>Image</span></div>
              </div>
            </li>
            <li class="context-menu-option" @click="loadImages('replace')">
              <div class="ctxmenu-content">
                <div class="ctxmenu-icon">
                  <span class="icon is-small"><i class="fas fa-plus-square"></i></span>
                </div>
                <div class="ctxmenu-text">Multiple images</div>
              </div>
            </li>
            <li class="context-menu-option" @click="loadImages('smart_insert')">
              <div class="ctxmenu-content">
                <div class="ctxmenu-icon">
                  <span class="icon is-small"><i class="fas fa-plus-circle"></i></span>
                </div>
                <div class="ctxmenu-text">Autodetect sequence</div>
              </div>
            </li>
          </ul>
        </div>
        <div class="cpb-sequence-buttons">
          <div class="cpb-sequence-btn">
            <a id="addPopperBtn" v-on:click="toggleLoadPopper" v-click-outside="closeLoadPopper" class="button is-neon-emerald"
              v-bind:class="{'is-loading': CRT_IS_LOADING, 'non-interactive': isButtonFrozen }" title="Open image loading dialog">
              <span class="icon is-small">
                <i class="fas fa-plus"></i>
              </span>
              <span>Add...</span>
            </a>
          </div>
          <div class="cpb-sequence-btn">
            <span class="is-white-d compact-line">Insert<br />after</span>
          </div>
          <div class="cpb-sequence-btn">
            <input v-model="insert_index" v-on:keydown="numConstrain($event, true, true)" class="input is-neon-white" type="number" min="0" style="width: 70px"
              title="The frame number at which new sequence of images will be inserted after. Setting 0 will add the new sequence before the first frame, and leaving this field empty is the default operation (append the new sequence after the last frame)"/>
          </div>
          <div class="cpb-sequence-btn">
            <a v-on:click="CRTClearAIMG" class="button is-neon-crimson" v-bind:class="{ 'non-interactive': isButtonFrozen }" title="Clears the entire sequence">
              <span class="icon is-small">
                <i class="fas fa-times"></i>
              </span>
              <span>Clear</span>
            </a>
          </div>
          <div class="cpb-sequence-btn">
             <span class="is-white-d" v-if="sequence_info.length &gt; 0">Total: {{ computeTotalSequenceSize }} </span>
          </div>
          <!-- <a
            v-on:click="loadImages('replace')"
            class="button is-neon-emerald"
            v-bind:class="{ 'is-loading': CRT_REPLACE_LOAD, 'non-interactive': isButtonFrozen }"
            title="Loads multiple static images to create an animated image. This replaces the current sequence above"
          >
            <span class="icon is-small">
              <i class="fas fa-plus-square"></i>
            </span>
            <span>Load</span>
          </a> -->
        </div>
        <div class="cpb-preview-buttons">
          <a v-on:click="previewAIMG" class="button is-neon-cyan"
            v-bind:class="{
              'is-loading': CRT_IS_PREVIEWING,
              'non-interactive': isButtonFrozen,
            }">
            <span class="icon is-medium">
              <i id="autoprev_icon" class="far fa-eye"></i>
            </span>
            <span>Preview</span>
          </a>
          <a v-on:click="CRTToggleCheckerBG" class="button is-neon-white"
            v-bind:class="{'is-active': checkerbg_active}">
            <span class="icon is-medium">
              <i class="fas fa-chess-board"></i>
            </span>
          </a>
        </div>
      </div>

      <div class="create-panel-controls">
        <div class="cpc-left-panel">
          <aside class="menu has-text-centered" style="margin: 0">
            <ul class="menu-list">
              <li class="subtab-menu-item" v-bind:class="{ 'is-selected': crt_menuselection == 0 }">
                <a v-on:click="crt_menuselection = 0">
                  <span class="icon is-large">
                    <i class="fas fa-image fa-2x fa-inverse"></i>
                  </span>
                  <p class="is-white-d">General</p>
                </a>
              </li>
              <li class="subtab-menu-item is-cyan"
                v-bind:class="{ 'is-selected': crt_menuselection == 1 }">
                <a v-on:click="crt_menuselection = 1"
                  v-bind:class="{ 'is-disabled': criteria.format == 'PNG' }">
                  <span class="icon is-large">
                    <i class="far fa-images fa-2x fa-inverse"></i>
                  </span>
                  <p class="is-white-d is-large">GIF</p>
                </a>
              </li>
              <li class="subtab-menu-item"
                v-bind:class="{ 'is-selected': crt_menuselection == 2 }">
                <a v-on:click="crt_menuselection = 2"
                  v-bind:class="{ 'is-disabled': criteria.format == 'GIF' }">
                  <span class="icon is-large">
                    <i class="far fa-images fa-2x fa-inverse"></i>
                  </span>
                  <p class="is-white-d is-large">APNG</p>
                </a>
              </li>
            </ul>
          </aside>
        </div>
        <div class="cpc-right-panel">
          <div v-show="crt_menuselection == 0">
            <table class="" width="100%">
              <tr>
                <td width="16.7%">
                  <div class="field">
                    <label class="label" title="The name of the GIF/APNG">Name</label>
                    <div class="control">
                      <input v-model="criteria.name" class="input is-neon-white" type="text" />
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label" title="The width of the GIF/APNG">Width</label>
                    <div class="control">
                      <input v-bind:value="criteria.width" v-on:keydown="numConstrain($event, true, true)"
                        v-on:input="widthHandler(criteria.width, $event)" class="input is-neon-white"
                        type="number" min="1"/>
                    </div>
                  </div>
                </td>
                <td width="16.7%">
                  <div class="field">
                    <label class="label" title="The height of the GIF/APNG">Height</label>
                    <div class="control">
                      <input
                        v-bind:value="criteria.height"
                        v-on:keydown="numConstrain($event, true, true)"
                        v-on:input="heightHandler(criteria.height, $event)"
                        class="input is-neon-white"
                        type="number"
                        min="1"
                      />
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
                <td width="16.7%" style="vertical-align: bottom">
                  <label class="checkbox">
                    <input v-model="lock_aspect_ratio" type="checkbox" />
                    Lock aspect ratio
                  </label>
                  <br />
                  <template v-if="aspect_ratio && aspect_ratio.text">
                    <input
                      v-model="aspect_ratio.text"
                      class="input is-border-colorless is-paddingless"
                      style="height: 1.5em"
                      readonly="readonly"
                    />
                  </template>
                  <template v-else>&nbsp;</template>
                </td>
                <td width="16.7%"></td>
              </tr>
              <tr>
                <td>
                  <div class="field">
                    <label class="label" title="The time needed to move to the next frame"
                      >Delay (seconds)</label
                    >
                    <div class="control">
                      <input
                        v-model="criteria.delay"
                        v-on:keydown="numConstrain($event, true, false)"
                        v-on:input="delayConstrain"
                        class="input is-neon-white"
                        type="number"
                        min="0"
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label class="label"
                      title="How many frames will be consecutively displayed per second.">Frame rate</label>
                    <div class="control">
                      <input
                        v-model="criteria.fps"
                        v-on:keydown="numConstrain($event, true, false)"
                        v-on:input="fpsConstrain"
                        class="input is-neon-white"
                        type="number"
                        min="0"
                        max="50"
                        step="0.01"
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label
                      class="label"
                      title="How many times the GIF/APNG will loop. Zero/blank for infinite loop"
                      >Loop count</label
                    >
                    <div class="control">
                      <input
                        v-model="criteria.loop_count"
                        v-on:keydown="numConstrain($event, true, true)"
                        class="input is-neon-white"
                        type="number"
                        min="0"
                        max="999"
                        step="1"
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <div class="field">
                    <label
                      class="label"
                      title="Choose which frame to start the animation from. Default is 1 (is also 1 if left blank or typed 0)"
                      >Start at frame</label
                    >
                    <div class="control">
                      <input
                        v-model="criteria.start_frame"
                        v-on:keydown="numConstrain($event, true, true)"
                        class="input is-neon-white"
                        type="number"
                        min="0"
                        step="1"
                      />
                    </div>
                  </div>
                </td>
                <td style="vertical-align: bottom">
                  <label class="checkbox" title="Flip the image horizontally">
                    <input v-model="criteria.flip_x" type="checkbox" />
                    Flip X
                  </label>
                  <br />
                  <label class="checkbox" title="Flip the image vertically">
                    <input v-model="criteria.flip_y" type="checkbox" />
                    Flip Y
                  </label>
                </td>
                <td style="vertical-align: bottom">
                  <label class="checkbox" title="Preserve transparent pixels">
                    <input v-model="criteria.is_transparent" type="checkbox" />
                    Preserve Alpha
                  </label>
                  <br />
                  <label class="checkbox" title="Reverse the animation">
                    <input v-model="criteria.is_reversed" type="checkbox" />
                    Reversed
                  </label>
                </td>
              </tr>
              <tr>
                <td colspan="4" style="padding-top: 15px">
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
                <td colspan="1" style="padding-top: 15px">
                  <div class="field">
                    <!-- <label class="label">Format</label> -->
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
                <td colspan="1" style="padding-top: 15px">
                  <div class="field has-text-centered">
                    <div class="control">
                      <a
                        v-on:click="CRTCreateAIMG"
                        class="button is-neon-cyan"
                        v-bind:class="{
                          'is-loading': CRT_IS_CREATING == true,
                          'non-interactive': isButtonFrozen,
                        }">Create</a>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="6">
                  <input
                    v-model="create_msgbox"
                    type="text"
                    class="input is-left-paddingless is-border-colorless"
                    readonly="readonly"
                  />
                </td>
              </tr>
            </table>
          </div>
          <div v-show="crt_menuselection == 1">
            <table
              class="table mod-new-control-table is-hpaddingless medium-size-label"
              width="100%"
            >
              <GIFOptimizationRow
                :is_optimized.sync="gif_opt.is_optimized"
                :optimization_level.sync="gif_opt.optimization_level"
                :is_lossy.sync="gif_opt.is_lossy"
                :lossy_value.sync="gif_opt.lossy_value"
                :is_reduced_color.sync="gif_opt.is_reduced_color"
                :color_space.sync="gif_opt.color_space"
                :is_unoptimized.sync="gif_opt.is_unoptimized"
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
            <table
              class="table mod-new-control-table is-hpaddingless medium-size-label"
              width="100%"
            >
              <APNGOptimizationRow
                :apng_is_optimized.sync="apng_opt.apng_is_optimized"
                :apng_optimization_level.sync="apng_opt.apng_optimization_level"
                :apng_is_lossy.sync="apng_opt.apng_is_lossy"
                :apng_lossy_value.sync="apng_opt.apng_lossy_value"
                :apng_is_unoptimized.sync="apng_opt.apng_is_unoptimized"
              />
              <!-- <APNGUnoptimizationRow
                      :apng_is_optimized.sync="apng_is_optimized"
                      :apng_is_lossy.sync="apng_is_lossy"
                      :apng_is_unoptimized.sync="apng_is_unoptimized"
                    /> -->
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const remote = require("electron").remote;
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const { writeImagePathsCache, writeCriterionCache } = require("./Client.vue");
const { tridentEngine } = require("./Client.vue");
const lodashClonedeep = require('lodash.clonedeep');
import {
  quintcellLister,
  validateFilename,
  GIF_DELAY_DECIMAL_PRECISION,
  APNG_DELAY_DECIMAL_PRECISION,
  randString,
  gcd,
  numConstrain,
  fileExists,
  readFilesize,
} from "./Utility.vue";
import GIFOptimizationRow from "./vueshards/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./vueshards/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./vueshards/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./vueshards/APNGUnoptimizationRow.vue";
import { createPopper } from '@popperjs/core';
import ClickOutside from 'vue-click-outside';

var data = {
  criteria: {
    name: "",
    fps: "",
    delay: "",
    format: "GIF",
    is_reversed: false,
    is_transparent: false,
    flip_x: false,
    flip_y: false,
    width: "",
    height: "",
    resize_method: "BICUBIC",
    loop_count: "",
    start_frame: "",
    rotation: 0,
  },
  gif_opt: {
    is_optimized: false,
    optimization_level: "1",
    is_lossy: false,
    lossy_value: "",
    is_reduced_color: false,
    color_space: "",
    is_unoptimized: false,
  },
  apng_opt: {
    apng_is_optimized: false,
    apng_optimization_level: "1",
    apng_is_lossy: false,
    apng_lossy_value: "",
    apng_is_unoptimized: false,
  },
  crt_menuselection: 0,
  image_paths: [],
  sequence_info: [],
  insert_index: "",
  total_size: "",
  orig_width: "",
  old_width: "",
  orig_height: "",
  old_height: "",
  outdir: "",
  preview_path: "",
  preview_path_cb: "",
  preview_info: "",
  aspect_ratio: "",
  lock_aspect_ratio: false,

  create_msgbox: "",
  // sequence_counter: "",
  checkerbg_active: false,
  CRT_INSERT_LOAD: false,
  CRT_SMARTINSERT_LOAD: false,
  CRT_REPLACE_LOAD: false,
  CRT_IS_LOADING: false,
  CRT_IS_PREVIEWING: false,
  CRT_IS_CREATING: false,

  popperIsVisible: false,
};

let extension_filters = [{ name: "Images", extensions: ["png", "gif"] }];
let img_dialog_props = ["openfile"];
let imgs_dialog_props = ["openfile", "multiSelections", "createDirectory"];
let dir_dialog_props = ["openDirectory", "createDirectory"];

function toggleLoadButtonAnim(ops, state = false) {
  if (ops == "insert") {
    data.CRT_INSERT_LOAD = state;
  } else if (ops == "smart_insert") {
    data.CRT_SMARTINSERT_LOAD = state;
  } else if (ops == "replace") {
    data.CRT_REPLACE_LOAD = state;
  }
}

function toggleLoadPopper() {
  if (!data.popperIsVisible) {
  let popper = document.querySelector("#crtLoadPopper");
  let button = document.querySelector("#addPopperBtn");
  this.popper = createPopper(button, popper, {
    placement: 'top-start',
    modifiers: {
    },
  });
  console.log("toggleLoadPopper");
  data.popperIsVisible = true;
  }
  else {
    data.popperIsVisible = false;
  }
}

function closeLoadPopper(event) {
  console.log(`closeLoadPopper ${data.popperIsVisible}, ${this.popper}`);
  console.log(event);
  if (data.popperIsVisible) {
    data.popperIsVisible = false;
  }
}

function loadImages(ops) {
  console.log("crt load image with ops:", ops);
  let props = ops == "replace" ? imgs_dialog_props : img_dialog_props;
  let cmd_args = [];
  switch (ops) {
    case "insert":
      // Add one image uses inspect-many instead of inspect-one because of the different data structure returned.
      // inspect-one is suited for singular file inspection, while inspect-many can support 1 to n amount of images.
      cmd_args.push("inspect_many"); break;
    case "smart_insert":
      cmd_args.push("inspect_smart"); break;
    case "replace":
      cmd_args.push("inspect_many"); break;
  }
  console.log("obtained props", props);
  var options = {
    filters: extension_filters,
    properties: props,
  };

  dialog.showOpenDialog(mainWindow, options).then((result) => {
    let img_paths = result.filePaths;
    console.log(img_paths);
    if (img_paths === undefined || img_paths.length == 0) {
      return;
    }

    data.CRT_IS_LOADING = true;
    toggleLoadButtonAnim(ops, true);

    cmd_args.push(img_paths)

    tridentEngine(cmd_args, (error, res) => {
      if (error) {
        console.error(error);
        try {
          console.error(error_data);
          data.create_msgbox = error_data.error;
        }
        catch (e) {
          data.create_msgbox = error;
        }
        data.CRT_IS_LOADING = false;
        toggleLoadButtonAnim(ops, false);
      } else if (res) {
        console.log(`[res]\n${res}`);
        res = JSON.parse(res);
        if (res && res.msg) {
          data.create_msgbox = res.msg;
        } else if (res && res.data) {
          let info = res.data;
          console.log("sequence info");
          console.log(info.sequence_info);
          console.log(info);
          renderSequence(info, { operation: ops });
          data.total_size = `Total size: ${info.total_size}`;
          data.criteria.name = info.name;
          data.criteria.width = info.width;
          data.criteria.height = info.height;
          data.criteria.fps = 50;
          data.criteria.delay = 0.02;
          data.orig_width = info.width;
          data.orig_height = info.height;
          data.create_msgbox = "";
          updateAspectRatio(data.criteria.width, data.criteria.height);
          data.CRT_IS_LOADING = false;
          toggleLoadButtonAnim(ops, false);
        }
      }
    });
  });
}

function renderSequence(pyinfo, options) {
  let operation = options.operation;
  // if (operation == "replace") {
    // console.log("AA");
    // data.image_paths = pyinfo.sequence;
    // data.sequence_info = pyinfo.sequence_info;
  // } else if (["insert", "smart_insert"].includes(operation)) {
    console.log("BB");
    let image_paths = []
    let sequence_info = []
    /*
    if (operation == "insert") {
      image_paths.push(pyinfo.general_info.absolute_url.value);
      sequence_info.push(pyinfo.general_info)
    }
    else if (operation == "smart_insert") {
      image_paths.push(...pyinfo.sequence);
      sequence_info.push(...pyinfo.sequence_info);
    }
    */
    if (data.insert_index) {
      data.image_paths.splice(data.insert_index, 0, ...pyinfo.sequence);
      data.sequence_info.splice(data.insert_index, 0, ...pyinfo.sequence_info);
    } else {
      data.image_paths.push(...pyinfo.sequence);
      data.sequence_info.push(...pyinfo.sequence_info);
    }
  // }
}

function removeFrame(index) {
  data.image_paths.splice(index, 1);
  data.sequence_info.splice(index, 1);
}

function CRTChooseOutdir() {
  var options = { properties: dir_dialog_props };
  dialog.showOpenDialog(mainWindow, options).then((result) => {
    let img_paths = result.filePaths;
    console.log(img_paths);
    if (img_paths && img_paths.length > 0) {
      console.log("folder selected");
      data.outdir = img_paths[0];
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
  data.total_size = "";
  data.orig_width = "";
  data.old_width = "";
  data.orig_height = "";
  data.old_height = "";
  data.criteria.name = "";
  data.criteria.delay = "";
  data.criteria.fps = "";
  data.criteria.loop_count = "";
  data.criteria.width = "";
  data.criteria.height = "";
  // data.CRT_sequence_counter = "";
  data.create_msgbox = "";
  // data.sequence_counter = "";
  let ARData = {
    w_ratio: "",
    h_ratio: "",
    text: "",
  };
  data.aspect_ratio = ARData;
  // mboxClear(create_msgbox);
  // deleteTempAIMG();
  // session.clearCache(testcallback);
}

function previewAIMG() {
  console.log("preview called");
  data.create_msgbox = "";
  if (data.sequence_info.length < 2) {
    data.create_msgbox = "Please load at least 2 images!";
    return;
  }
  let validator = validateFilename(data.criteria.name);
  if (!validator.valid) {
    console.error(validator.msg);
    data.create_msgbox = validator.msg;
    return;
  }
  data.CRT_IS_PREVIEWING = true;
  console.log(data);
  writeImagePathsCache(data.image_paths);
  writeCriterionCache(data);
  let criteria_pack = lodashClonedeep({
    "criteria": data.criteria,
    "gif_opt": data.gif_opt,
    "apng_opt": data.apng_opt,
  });
  criteria_pack.criteria.name += `_preview_${Date.now()}_${randString(7)}`;
  tridentEngine(["combine_image", data.image_paths, "./temp", criteria_pack], (error, res) => {
    if (error) {
      console.error(error);
      data.create_msgbox = error.error;
      data.CRT_IS_PREVIEWING = false;
    } else if (res) {
      res = JSON.parse(res);
      console.log(`res -> ${res}`);
      if (res.msg) {
        data.create_msgbox = res.msg;
      }
      if (res.preview_path) {
        data.preview_path = res.preview_path;
        previewPathCacheBreaker();
      }
      if (res.CONTROL == "CRT_FINISH") {
        tridentEngine(["inspect_one", data.preview_path], (err, info) => {
          if (err) {
            let err_data = JSON.parse(err);
            console.error(err_data);
            data.CRT_IS_PREVIEWING = false;
          } else if (info) {
            info = JSON.parse(info).data;
            console.log("preview inspect");
            console.log(info);
            data.preview_info = info;
            data.create_msgbox = "Previewed!";
            data.CRT_IS_PREVIEWING = false;
          }
        });
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

  if (fileExists(data.outdir, `${data.criteria.name}.${data.criteria.format.toLowerCase()}`)) {
    let WINDOW = remote.getCurrentWindow();
    let options = {
      buttons: ["Yes", "Cancel"],
      message:
        "A file with the same name already exists in the output folder. Do you want to override it?",
    };
    let response = dialog.showMessageBoxSync(WINDOW, options);
    if (response == 1) proceed_create = false;
  }

  if (proceed_create) {
    data.CRT_IS_CREATING = true;
    client.invoke(
      "combine_image",
      data.image_paths,
      data.outdir,
      data.name,
      data,
      (error, res) => {
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
              data.create_msgbox = `${data.criteria.format.toUpperCase()} created!`;
              data.CRT_IS_CREATING = false;
            }
          }
        }
      }
    );
  }
}

function computeTotalSequenceSize() {
  console.log("computeTotalSequenceSize");
  console.log(data.sequence_info.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0));
  return readFilesize(data.sequence_info.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0), 3);
}

function CRTToggleCheckerBG() {
  data.checkerbg_active = !data.checkerbg_active;
  console.log("now checkerbg is", data.checkerbg_active);
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
  data.criteria.width = newWidth;
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) {
    // Change height if lock_aspect_ratio is true and height is not 0
    let raHeight = Math.round(
      (newWidth / data.aspect_ratio.w_ratio) * data.aspect_ratio.h_ratio
    );
    data.criteria.height = raHeight > 0 ? raHeight : "";
  } else {
    updateAspectRatio(data.criteria.width, data.criteria.height);
  }
}

function heightHandler(height, event) {
  data.old_height = parseInt(height);
  let newHeight = event.target.value;
  data.criteria.height = newHeight;
  if (data.lock_aspect_ratio && data.aspect_ratio.w_ratio > 0) {
    let raWidth = Math.round(
      (newHeight / data.aspect_ratio.h_ratio) * data.aspect_ratio.w_ratio
    );
    console.log(raWidth);
    data.criteria.width = raWidth > 0 ? raWidth : "";
  } else {
    updateAspectRatio(data.criteria.width, data.criteria.height);
  }
}

function updateAspectRatio(width, height) {
  if (data.criteria.width && data.criteria.height) {
    console.log("uAR", width, height);
    let divisor = gcd(width, height);
    let w_ratio = width / divisor;
    let h_ratio = height / divisor;
    let ARData = {
      w_ratio: w_ratio,
      h_ratio: h_ratio,
      text: `${w_ratio}:${h_ratio}`,
    };
    console.log(ARData);
    data.aspect_ratio = ARData;
  }
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

function CRTQuintcellLister() {
  return quintcellLister(data.sequence_info);
}

function sequenceCounter() {
  if (data.sequence_info.length > 0) {
    return `${data.sequence_info.length} images`;
  } else return "";
}

function previewPathCacheBreaker() {
  // let cb_url = `${data.preview_path}?cachebreaker=${randString()}`;
  let cb_url = `${data.preview_path}`;
  console.log("Cache breaker url", cb_url);
  data.preview_path_cb = cb_url;
}

window.onresize = closeLoadPopper;

export default {
  data: function () {
    return data;
  },
  components: {
    GIFOptimizationRow,
    GIFUnoptimizationRow,
    APNGOptimizationRow,
    APNGUnoptimizationRow,
  },
  methods: {
    toggleLoadPopper: toggleLoadPopper,
    closeLoadPopper: closeLoadPopper,
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
    computeTotalSequenceSize: computeTotalSequenceSize,
  },
  directives:{
    ClickOutside,
  },
};
</script>
