<template>
  <div id="create_panel">
    <div class="create-panel-root">
      <div class="create-panel-display">
        <div class="create-panel-sequence silver-bordered">
          <div class="rtable rtable-5cols">
            <div
              v-for="(item, index) in sequence_info" :key="index" class="rtable-cell"
              :title="sequence_info?                    
                `Name: ${item.name.value}\n` +
                `Dimensions: ${item.width.value} x ${item.height.value}\n` +
                `Format: ${item.format.value}\n` +
                `Mode: ${item.color_mode.value}\n` +
                `Comment: ${item.comments.value || 'None'}` : ''
              "
            >
              <img :src="escapeLocalPath(item.absolute_url.value)" />
              <span class="index-anchor is-white-d">
                {{ parseInt(index) + 1 }}
              </span>
              <button class="del-anchor" @click="removeFrame(parseInt(index))">
                <span class="icon" @click="removeFrame(parseInt(index))">
                  <font-awesome-icon icon="minus-circle" @click="removeFrame(parseInt(index))" />
                </span>
              </button>
            </div>
          </div>
        </div>
        <div
          class="create-panel-preview silver-bordered-no-left"
          :title="preview_info? 
            `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
            `File size: ${preview_info.general_info.fsize_hr.value}\n` +
            `Total frames: ${preview_info.animation_info.frame_count.value}\n` +
            `FPS: ${preview_info.animation_info.fps.value}\n` +
            `Duration: ${preview_info.animation_info.loop_duration.value} seconds\n` +
            `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
            `Format: ${preview_info.general_info.format.value}` : ''
          "
          :class="{'has-checkerboard-bg': checkerbg_active }"
        >
          <!-- <div v-if="preview_info" class="crt-aimg-container"> -->
          <img v-if="preview_info" :src="escapeLocalPath(preview_path_cb)" />
          <!-- </div> -->
        </div>
      </div>

      <div class="create-panel-middlebar">
        <div
          v-show="popperIsVisible" id="crtLoadPopper" ref="popper" class="context-menu"
          tabindex="-1" style="display: block;"
        >
          <ul class="context-menu-options">
            <li class="context-menu-option" @click="btnLoadImages('insert')">
              <div class="ctxmenu-content">
                <div class="ctxmenu-icon">
                  <span class="icon is-small">
                    <font-awesome-icon icon="plus" />
                  </span>
                </div>
                <div class="ctxmenu-text">
                  <span>Images</span>
                </div>
              </div>
            </li>
            <!-- <li class="context-menu-option" @click="btnLoadImages('replace')">
              <div class="ctxmenu-content">
                <div class="ctxmenu-icon">
                  <span class="icon is-small">
                    <i class="fas fa-plus-square"></i>
                  </span>
                </div>
                <div class="ctxmenu-text">Multiple images</div>
              </div>
            </li> -->
            <li class="context-menu-option" @click="btnLoadImages('smart_insert')">
              <div class="ctxmenu-content">
                <div class="ctxmenu-icon">
                  <span class="icon is-small">
                    <font-awesome-icon icon="plus-circle" />
                  </span>
                </div>
                <div class="ctxmenu-text">
                  Autodetect sequence
                </div>
              </div>
            </li>
          </ul>
        </div>
        <div class="cpb-sequence-buttons">
          <div class="cpb-sequence-btn">
            <a
              id="addPopperBtn" v-click-outside="closeLoadPopper" class="button is-neon-emerald" :class="{'is-loading': CRT_IS_LOADING, 'non-interactive': isButtonFrozen }"
              title="Open image loading dialog" @click="btnToggleLoadPopper"
            >
              <span class="icon is-small">
                <font-awesome-icon icon="plus" />
              </span>
              <span>Add...</span>
            </a>
          </div>
          <div class="cpb-sequence-btn">
            <span class="is-white-d compact-line">Insert<br />after</span>
          </div>
          <div class="cpb-sequence-btn">
            <input
              v-model="insert_index" class="input is-neon-white" type="number" min="0" style="width: 70px"
              title="The frame number at which new sequence of images will be inserted after. Setting 0 will add the new sequence before the first frame, and leaving this field empty is the default operation (append the new sequence after the last frame)"
              @keydown="numConstrain($event, true, true)"
            />
          </div>
          <div class="cpb-sequence-btn">
            <a class="button is-neon-crimson" :class="{ 'non-interactive': isButtonFrozen }" title="Clears the entire sequence" @click="btnClearAll">
              <span class="icon is-small">
                <font-awesome-icon icon="times" />
              </span>
              <span>Clear</span>
            </a>
          </div>
          <div class="cpb-sequence-btn">
            <span v-if="sequence_info.length &gt; 0" class="is-white-d">Total: {{ computeTotalSequenceSize }} </span>
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
          <a
            class="button is-neon-cyan" :class="{
              'is-loading': CRT_IS_PREVIEWING,
              'non-interactive': isButtonFrozen,
            }"
            @click="btnPreviewAIMG"
          >
            <span class="icon is-medium">
              <font-awesome-icon id="autoprev_icon" :icon="['far', 'eye']" />
            </span>
            <span>Preview</span>
          </a>
          <a
            class="button is-neon-white" :class="{'is-active': checkerbg_active}"
            @click="btnToggleCheckerBG"
          >
            <span class="icon is-medium">
              <font-awesome-icon icon="chess-board" />
            </span>
          </a>
        </div>
      </div>

      <div class="create-panel-controls">
        <div class="cpc-left-panel">
          <aside class="menu has-text-centered" style="margin: 0">
            <ul class="menu-list">
              <li class="subtab-menu-item" :class="{ 'is-selected': crt_menuselection == 0 }">
                <a @click="crt_menuselection = 0">
                  <span class="icon is-large">
                    <font-awesome-icon icon="image" size="2x" inverse />
                    <!-- <i class="fas fa-image fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d">General</p>
                </a>
              </li>
              <li
                class="subtab-menu-item is-cyan"
                :class="{ 'is-selected': crt_menuselection == 1 }"
              >
                <a
                  :class="{ 'is-disabled': criteria.format != 'gif' }"
                  @click="crt_menuselection = 1"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="images" size="2x" inverse />
                    <!-- <i class="far fa-images fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d is-large">GIF</p>
                </a>
              </li>
              <li
                class="subtab-menu-item"
                :class="{ 'is-selected': crt_menuselection == 2 }"
              >
                <a
                  :class="{ 'is-disabled': criteria.format != 'png' }"
                  @click="crt_menuselection = 2"
                >
                  <span class="icon is-large">                    
                    <font-awesome-icon icon="images" size="2x" inverse />
                    <!-- <i class="far fa-images fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d is-large">APNG</p>
                </a>
              </li>
            </ul>
          </aside>
        </div>
        <div class="cpc-right-panel">
          <div class="cpc-right-top-panel">
            <div v-show="crt_menuselection == 0">
              <table class="" width="100%">
                <tr>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label" title="The name of the GIF/APNG">Name</label>
                      <div class="control">
                        <input v-model="fname" class="input is-neon-white" type="text" />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label" title="The width of the GIF/APNG">Width</label>
                      <div class="control">
                        <input 
                          :value="criteria.width" 
                          class="input is-neon-white"
                          type="number" 
                          min="1"
                          @keydown="numConstrain($event, true, true)" 
                          @input="widthHandler(criteria.width, $event)"
                        />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label" title="The height of the GIF/APNG">Height</label>
                      <div class="control">
                        <input
                          :value="criteria.height"
                          class="input is-neon-white"
                          type="number"
                          min="1"
                          @keydown="numConstrain($event, true, true)"
                          @input="heightHandler(criteria.height, $event)"
                        />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label
                        class="label"
                        title="Which algorithm to use when resizing the image. Default is Bicubic"
                      >Resize Method</label>
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
                            <option value="BOX">
                              Box
                            </option>
                            <option value="HAMMING">
                              Hamming
                            </option>
                            <option value="LANCZOS">
                              Lanczos
                            </option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
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
                    <template v-else>
&nbsp;
                    </template>
                  </td>
                  <td width="16.7%" style="vertical-align: bottom" />
                </tr>
                <tr>
                  <td>
                    <div class="field">
                      <label class="label" title="The time needed to move to the next frame">Delay (seconds)</label>
                      <div class="control">
                        <input
                          v-model="criteria.delay"
                          class="input is-neon-white"
                          type="number"
                          min="0"
                          @keydown="numConstrain($event, true, false)"
                          @input="delayConstrain"
                        />
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="field">
                      <label
                        class="label"
                        title="How many frames will be consecutively displayed per second."
                      >Frame rate</label>
                      <div class="control">
                        <input
                          v-model="criteria.fps"
                          class="input is-neon-white"
                          type="number"
                          min="0"
                          max="50"
                          step="0.01"
                          @keydown="numConstrain($event, true, false)"
                          @input="fpsConstrain"
                        />
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="field">
                      <label
                        class="label"
                        title="How many times the GIF/APNG will loop. Zero/blank for infinite loop"
                      >Loop count</label>
                      <div class="control">
                        <input
                          v-model="criteria.loop_count"
                          class="input is-neon-white"
                          type="number"
                          min="0"
                          max="999"
                          step="1"
                          @keydown="numConstrain($event, true, true)"
                        />
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="field">
                      <label class="label" title="Choose which frame to start the animation from. Default is 1 (is also 1 if left blank or typed 0)">Start at frame</label>
                      <div class="control">
                        <input
                          v-model="criteria.start_frame" class="input is-neon-white" type="number" 
                          min="0" step="1" @keydown="numConstrain($event, true, true)"
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
                      <input v-model="criteria.preserve_alpha" type="checkbox" />
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
                        <a class="button is-neon-cyan" @click="btnSetSavePath">
                          <span class="icon is-small">
                            <font-awesome-icon icon="save" />
                          </span>
                          <span>Save to</span>
                        </a>
                      </div>
                      <div class="control is-expanded">
                        <input
                          v-model="save_dir"
                          class="input is-neon-white"
                          type="text"
                          placeholder="Output folder"
                        />
                      </div>
                    </div>
                  </td>
                  <td colspan="1" style="padding-top: 15px">
                    <div class="field">
                      <!-- <label class="label">Format</label> -->
                      <div class="control">
                        <div class="select is-neon-cyan" :class="{'non-interactive': isButtonFrozen}">
                          <select v-model="criteria.format">
                            <option v-for="(item, name, index) in SUPPORTED_CREATE_EXTENSIONS" :key="index" :value="name">
                              {{ item }}
                            </option>
                            <!-- <option value="GIF">GIF</option>
                            <option value="PNG">APNG</option> -->
                          </select>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td colspan="1" style="padding-top: 15px">
                    <div class="field">
                      <div class="control">
                        <a
                          class="button is-neon-cyan"
                          :class="{
                            'is-loading': CRT_IS_CREATING == true,
                            'non-interactive': isButtonFrozen,
                          }"
                          @click="btnCreateAIMG"
                        >CREATE</a>
                      </div>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td colspan="6" />
                </tr>
              </table>
            </div>
            <div v-show="crt_menuselection == 1">
              <table
                class="mod-new-control-table is-hpaddingless medium-size-label"
                width="100%"
              >
                <GIFOptimizationRow
                  v-model:is_optimized="gif_opt_criteria.is_optimized"
                  v-model:optimization_level="gif_opt_criteria.optimization_level"
                  v-model:is_lossy="gif_opt_criteria.is_lossy"
                  v-model:lossy_value="gif_opt_criteria.lossy_value"
                  v-model:is_reduced_color="gif_opt_criteria.is_reduced_color"
                  v-model:color_space="gif_opt_criteria.color_space"
                  v-model:is_unoptimized="gif_opt_criteria.is_unoptimized"
                  v-model:dither_method="gif_opt_criteria.dither_method"
                  v-model:palletization_method="gif_opt_criteria.palletization_method"
                  v-model:is_dither_alpha="gif_opt_criteria.is_dither_alpha"
                  v-model:dither_alpha_method="gif_opt_criteria.dither_alpha_method"
                  v-model:dither_alpha_threshold="gif_opt_criteria.dither_alpha_threshold"
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
                class="mod-new-control-table is-hpaddingless medium-size-label"
                width="100%"
              >
                <APNGOptimizationRow
                  v-model:apng_is_optimized="apng_opt_criteria.apng_is_optimized"
                  v-model:apng_optimization_level="apng_opt_criteria.apng_optimization_level"
                  v-model:apng_is_lossy="apng_opt_criteria.apng_is_lossy"
                  v-model:apng_lossy_value="apng_opt_criteria.apng_lossy_value"
                  v-model:apng_quantization_enabled="apng_opt_criteria.apng_quantization_enabled"
                  v-model:apng_quantization_quality="apng_opt_criteria.apng_quantization_quality"
                  v-model:apng_quantization_speed="apng_opt_criteria.apng_quantization_speed"
                  v-model:apng_convert_color_mode="apng_opt_criteria.apng_convert_color_mode"
                  v-model:apng_new_color_mode="apng_opt_criteria.apng_new_color_mode"
                  v-model:apng_is_unoptimized="apng_opt_criteria.apng_is_unoptimized"
                />
                <!-- <APNGUnoptimizationRow
                        :apng_is_optimized.sync="apng_is_optimized"
                        :apng_is_lossy.sync="apng_is_lossy"
                        :apng_is_unoptimized.sync="apng_is_unoptimized"
                      /> -->
              </table>
            </div>
          </div>
          <div class="cpc-right-bottom-panel">
            <StatusBar :status-bar-id="statusBarId" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ipcRenderer } from 'electron';
import { dirname, basename, join } from "path";
import { access, accessSync, constants, existsSync } from "fs";
const SUPPORTED_CREATE_EXTENSIONS = {
  'gif': 'GIF',
  'png': 'APNG',
}

import { tridentEngine } from "../modules/streams/trident_engine";
import { numConstrain } from "../modules/events/constraints";
import { escapeLocalPath, stem, validateFilename } from "../modules/utility/pathutils";
import { formatBytes, randString } from "../modules/utility/stringutils";
import { gcd } from "../modules/utility/calculations";
import { PREVIEWS_PATH } from "../common/paths";
import { GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION } from "../modules/constants/images";

import GIFOptimizationRow from "./components/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./components/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./components/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./components/APNGUnoptimizationRow.vue";

import { createPopper } from '@popperjs/core';
import vClickOutside from 'click-outside-vue3'

import StatusBar from "./components/StatusBar.vue";
import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";

import emitter from "../modules/events/emitter";
// import ClickOutside from 'vue-click-outside';
// import Vue from 'vue';


/*
let data = {
  criteria: {
    // name: "",
    fps: "",
    delay: "",
    format: "gif",
    is_reversed: false,
    preserve_alpha: false,
    flip_x: false,
    flip_y: false,
    width: "",
    height: "",
    resize_method: "BICUBIC",
    loop_count: "",
    start_frame: "",
    rotation: 0,
  },
  gif_opt_criteria: {
    is_optimized: false,
    optimization_level: "1",
    is_lossy: false,
    lossy_value: "",
    is_reduced_color: false,
    color_space: "",
    is_unoptimized: false,
    is_dither_alpha: false,
    dither_alpha_method: "SCREENDOOR",
    dither_alpha_threshold: 50,
  },
  apng_opt_criteria: {
    apng_is_optimized: false,
    apng_optimization_level: "1",
    apng_is_lossy: false,
    apng_lossy_value: "",
    apng_is_unoptimized: false,
    apng_preconvert_rgba: false,
    apng_convert_color_mode: false,
    apng_new_color_mode: "RGBA",
  },
  fname: "",
  supported_create_extensions: SUPPORTED_CREATE_EXTENSIONS,
  crt_menuselection: 0,
  image_paths: [],
  sequence_info: [],
  save_fstem: "",
  save_dir: "",
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
*/

let extension_filters = [{ name: "Images", extensions: Object.keys(SUPPORTED_CREATE_EXTENSIONS) }];
let img_dialog_props = ["openfile"];
let imgs_dialog_props = ["openfile", "multiSelections", "createDirectory"];
let dir_dialog_props = ["openDirectory", "createDirectory"];


/*

function toggleLoadButtonAnim(ops, state = false) {
  if (ops == "insert") {
    data.CRT_INSERT_LOAD = state;
  } else if (ops == "smart_insert") {
    data.CRT_SMARTINSERT_LOAD = state;
  } else if (ops == "replace") {
    data.CRT_REPLACE_LOAD = state;
  }
}

function btnToggleLoadPopper() {
  if (!data.popperIsVisible) {
  let popper = document.querySelector("#crtLoadPopper");
  let button = document.querySelector("#addPopperBtn");
  this.popper = createPopper(button, popper, {
    placement: 'top-start',
    modifiers: {
    },
  });
  console.log("btnToggleLoadPopper");
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

function btnLoadImages(ops) {
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

  ipcRenderer.invoke('open-dialog', options).then((result) => {
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
        try {
          data.create_msgbox = error;
        }
        catch (e) {
          data.create_msgbox = error;
        }
        data.CRT_IS_LOADING = false;
        toggleLoadButtonAnim(ops, false);
      } else if (res) {
        if (res && res.msg) {
          data.create_msgbox = res.msg;
        } else if (res && res.data) {
          let info = res.data;
          console.log("sequence info");
          console.log(info.sequence_info);
          console.log(info);
          renderSequence(info, { operation: ops });
          data.total_size = `Total size: ${info.total_size}`;
          // data.save_fstem = stem(data.save_fstem || info.name);
          data.fname = data.fname || info.name
          data.criteria.width = data.criteria.width || info.width;
          data.criteria.height = data.criteria.height || info.height;
          data.criteria.fps = data.criteria.fps || 50;
          data.criteria.delay = data.criteria.delay || 0.02;
          data.orig_width = info.width;
          data.orig_height = info.height;
          data.create_msgbox = "";
          updateAspectRatio(data.criteria.width, data.criteria.height);
          data.CRT_IS_LOADING = false;
          toggleLoadButtonAnim(ops, false);
          data.lock_aspect_ratio = true;
        }
      }
    });
  });
}

function setMinimalDimensions() {
  if (data.criteria.width == 0)
    data.criteria.width = 1;
  if (data.criteria.height == 0)
    data.criteria.height = 1;
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
  if (operation == "insert") {
    image_paths.push(pyinfo.general_info.absolute_url.value);
    sequence_info.push(pyinfo.general_info)
  }
  else if (operation == "smart_insert") {
    image_paths.push(...pyinfo.sequence);
    sequence_info.push(...pyinfo.sequence_info);
  }
  if (data.insert_index) {
    data.image_paths.splice(data.insert_index, 0, ...pyinfo.sequence);
    data.sequence_info.splice(data.insert_index, 0, ...pyinfo.sequence_info);
  } else {
    data.image_paths.push(...pyinfo.sequence);
    data.sequence_info.push(...pyinfo.sequence_info);
  }
}

function removeFrame(index) {
  data.image_paths.splice(index, 1);
  data.sequence_info.splice(index, 1);
}

function singleSaveOption() {
  return {
    title: `Save As`,
    defaultPath: saveFileName(),
    filters: [{ name: data.criteria.format, extensions: [data.criteria.format.toLowerCase()] }],
    properties: ["createDirectory", "showOverwriteConfirmation", "dontAddToRecent"],
  }
}

function setSaveDirFromDialog(afterSaveCallback) {
  let options = { properties: dir_dialog_props };
  ipcRenderer.invoke('open-dialog', options).then((result) => {
    let out_dirs = result.filePaths;
    console.log(out_dirs);
    if (out_dirs && out_dirs.length > 0) { 
      data.save_dir = out_dirs[0];
    }
    data.create_msgbox = "";
  });
}

function setSavePathFromDialog(afterSaveCallback) {
  ipcRenderer.invoke('save-dialog', singleSaveOption()).then((result) => {
    if (result.canceled) return;
    console.log(result);
    let save_path = result.filePath;
    // data.savePathInput = save_path;
    // data.save_path = save_path;
    data.save_dir = dirname(save_path);
    data.save_fstem = stem(basename(save_path));
    if (afterSaveCallback) {
      afterSaveCallback();
    }
  });
}

function btnSetSavePath() {
  // setSavePathFromDialog();
  setSaveDirFromDialog();
}


function btnClearAll() {
  clearSequence();
  clearPreviewAIMG();
  clearAuxInfo();
  clearFields();
  data.lock_aspect_ratio = false;
}

function clearSequence() {
  data.image_paths = [];
  data.sequence_info = [];
  data.save_fstem = "";
}

function clearPreviewAIMG() {
  data.preview_path = "";
  data.preview_path_cb = "";
  data.preview_info = "";
}

function clearAuxInfo() {
  data.total_size = "";
  data.orig_width = "";
  data.old_width = "";
  data.orig_height = "";
  data.old_height = "";
  data.create_msgbox = "";
  let empty_aspect_ratio = {
    w_ratio: "",
    h_ratio: "",
    text: "",
  };
  data.aspect_ratio = empty_aspect_ratio;
}

function clearFields() {
  data.criteria.name = "";
  data.criteria.delay = "";
  data.criteria.fps = "";
  data.criteria.loop_count = "";
  data.criteria.width = "";
  data.criteria.height = "";
}

function btnPreviewAIMG() {
  previewAIMG();
}

function previewAIMG() {
  console.log("preview called");
  data.create_msgbox = "";
  if (data.sequence_info.length < 2) {
    data.create_msgbox = "Please load at least 2 images!";
    return;
  }
  setMinimalDimensions();
  // let validator = validateFilename(data.criteria.name);
  // if (!validator.valid) {
  //   console.error(validator.msg);
  //   data.create_msgbox = validator.msg;
  //   return;
  // }
  data.CRT_IS_PREVIEWING = true;
  console.log(data);
  let criteria_pack = lodashClonedeep({
    "criteria": data.criteria,
    "gif_opt_criteria": data.gif_opt_criteria,
    "apng_opt_criteria": data.apng_opt_criteria,
  });
  let preview_filename = `${data.save_fstem}_preview_${Date.now()}_${randString(7)}.${data.criteria.format.toLowerCase()}`;
  let preview_savepath = join(PREVIEWS_PATH, preview_filename);
  console.log(preview_savepath);
  tridentEngine(["combine_image", data.image_paths, preview_savepath, criteria_pack], (error, res) => {
    if (error) {
      // console.error(error);
      // let error_data = JSON.parse(error);
      data.create_msgbox = error;
      data.CRT_IS_PREVIEWING = false;
    } else if (res) {
      if (res.msg) {
        data.create_msgbox = res.msg;
      }
      if (res.preview_path) {
        data.preview_path = res.preview_path;
        previewPathCacheBreaker();
      }
    }},
    () => tridentEngine(["inspect_one", data.preview_path], (error, info) => {
      if (error) {
        console.error(error);
        data.CRT_IS_PREVIEWING = false;
      } else if (info) {
        let inspectionData = info.data;
        console.log("preview inspect");
        console.log(inspectionData);
        data.preview_info = inspectionData;
        data.create_msgbox = "Previewed!";
        data.CRT_IS_PREVIEWING = false;
      }
    })
  );
}

function btnCreateAIMG() {
  if (data.sequence_info.length < 2) {
    data.create_msgbox = "Please load at least 2 images!";
    return;
  }
  if (data.save_dir) {
    if (validateFilename(data.fname))
      createAnimatedImage();
    else
      data.create_msgbox = "File name contains characters that are not allowed"
  }
  else {
    btnSetSavePath(createAnimatedImage);
  }
}

function getSavePath() {
  let file_name = `${data.fname}.${data.criteria.format}`;
  let save_path = join(data.save_dir, file_name);
  console.log(`getSavePath ${save_path}`);
  return save_path;
}

function createAnimatedImage() {
  let proceed_create = true;
  data.create_msgbox = "";
  setMinimalDimensions();
  // if (fileExists(data.save_path)) {
  //   let WINDOW = remote.getCurrentWindow();
  //   let options = {
  //     buttons: ["Yes", "Cancel"],
  //     message:
  //       "A file with the same name already exists in the output folder. Do you want to override it?",
  //   };
  //   let response = dialog.showMessageBoxSync(WINDOW, options);
  //   if (response == 1) proceed_create = false;
  // }

  if (proceed_create) {
    data.CRT_IS_CREATING = true;
    let criteria_pack = lodashClonedeep({
      "criteria": data.criteria,
      "gif_opt_criteria": data.gif_opt_criteria,
      "apng_opt_criteria": data.apng_opt_criteria,
    });
    tridentEngine(["combine_image", data.image_paths, getSavePath(), criteria_pack], (error, res) => {
      if (error) {
        try {
          data.create_msgbox = error;
          data.CRT_IS_CREATING = false;
        }
        catch (e) {
          data.create_msgbox = error;
        }
      } else if (res) {
        console.log(`res -> ${res}`);
        if (res) {
          console.log(res);
          if (res.msg) {
            data.create_msgbox = res.msg;
          }
        }
      }
    },
    () => {
      data.create_msgbox = `${data.criteria.format.toUpperCase()} created!`;
      data.CRT_IS_CREATING = false;
    });
  }
}

function computeTotalSequenceSize() {
  console.log("computeTotalSequenceSize");
  console.log(data.sequence_info.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0));
  return formatBytes(data.sequence_info.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0), 3);
}

function saveFileName() {
  return `${data.save_fstem}.${data.criteria.format.toLowerCase()}`;
}

function btnToggleCheckerBG() {
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
  let newWidth = event.target.value;
  data.criteria.width = parseInt(newWidth);
  if (data.lock_aspect_ratio && data.aspect_ratio.h_ratio > 0) {
    // Change height if lock_aspect_ratio is true and height is not 0
    let raHeight = Math.round(
      (newWidth / data.aspect_ratio.w_ratio) * data.aspect_ratio.h_ratio
    );
    data.criteria.height = raHeight > 0 ? parseInt(raHeight) : "";
  } else {
    updateAspectRatio(data.criteria.width, data.criteria.height);
  }
}

function heightHandler(height, event) {
  data.old_height = parseInt(height);
  let newHeight = event.target.value;
  data.criteria.height = parseInt(newHeight);
  if (data.lock_aspect_ratio && data.aspect_ratio.w_ratio > 0) {
    let raWidth = Math.round(
      (newHeight / data.aspect_ratio.h_ratio) * data.aspect_ratio.w_ratio
    );
    console.log(raWidth);
    data.criteria.width = raWidth > 0 ? parseInt(raWidth) : "";
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

function previewPathCacheBreaker() {
  // let cb_url = `${data.preview_path}?cachebreaker=${randString()}`;
  let cb_url = `${data.preview_path}`;
  console.log("Cache breaker url", cb_url);
  data.preview_path_cb = cb_url;
}
*/

export default {
  components: {
    GIFOptimizationRow,
    GIFUnoptimizationRow,
    APNGOptimizationRow,
    APNGUnoptimizationRow,
    StatusBar,
  },
  directives:{
    // ClickOutside,
    clickOutside: vClickOutside.directive,
  },
  data: function () {
    return {
      criteria: {
        // name: "",
        fps: "",
        delay: "",
        format: "gif",
        is_reversed: false,
        preserve_alpha: false,
        flip_x: false,
        flip_y: false,
        width: "",
        height: "",
        resize_method: "BICUBIC",
        loop_count: "",
        start_frame: "",
        rotation: 0,
      },
      gif_opt_criteria: {
        is_optimized: false,
        optimization_level: "1",
        is_lossy: false,
        lossy_value: "",
        is_reduced_color: false,
        color_space: "",
        is_unoptimized: false,
        dither_method: "FLOYD_STEINBERG",
        palletization_method: "ADAPTIVE",
        is_dither_alpha: false,
        dither_alpha_method: "SCREENDOOR",
        dither_alpha_threshold: 50,
      },
      apng_opt_criteria: {
        apng_is_optimized: false,
        apng_optimization_level: "1",
        apng_is_lossy: false,
        apng_lossy_value: "",
        apng_quantization_enabled: false,
        apng_quantization_quality: 70,
        apng_quantization_speed: 3,
        apng_is_unoptimized: false,
        apng_preconvert_rgba: false,
        apng_convert_color_mode: false,
        apng_new_color_mode: "RGBA",
      },
      fname: "",
      SUPPORTED_CREATE_EXTENSIONS: SUPPORTED_CREATE_EXTENSIONS,
      crt_menuselection: 0,
      image_paths: [],
      sequence_info: [],
      latest_load_count: 0,
      save_fstem: "",
      save_dir: "",
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
      statusBarId: "createPanelStatusBar",

      // statusBarBus: new Vue(),
    };
  },
  computed: {
    isButtonFrozen() {
      if (this.CRT_IS_LOADING || this.CRT_IS_PREVIEWING || this.CRT_IS_CREATING) return true;
      else return false;
    },
    sequenceCounter() {
      if (this.sequence_info.length > 0) {
        return `${this.sequence_info.length} images`;
      } else return "";
    },
    computeTotalSequenceSize() {
      console.log("computeTotalSequenceSize");
      console.log(this.sequence_info.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0));
      return formatBytes(this.sequence_info.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0), 3);
    },
    /*
    savePathInput: {
      get() {
        console.log(`getter obtain dir: ${this.save_dir}`)
        console.log(`getter obtain stem: ${this.save_fstem}`)
        console.log(`getter obtain format: ${this.criteria.format.toLowerCase()}`)
        if (this.save_dir && this.save_fstem){
          let p = join(data.save_dir, `${data.save_fstem}.${data.criteria.format.toLowerCase()}`);
          return p;
        }
        else
          return "";
      },
      set(value) {
        let dir = dirname(value);
        let fstem = stem(basename(value));
        console.log(`setter stem remove end: ${fstem.slice(-1)}`);
        if (fstem && fstem.slice(-1) == '.') {
          console.log('sliceddddd')
          fstem = fstem.slice(0, -1);
        }
        let ext = "";
        let frags = value.split('.');
        console.log(`setter frags: ${frags}`);
        if (frags.length >= 2)
          ext = frags.pop();
        console.log(`setter value: ${value}`);
        console.log(`setter dir: ${dir}`);
        console.log(`setter stem: ${fstem}`);
        console.log(`setter ext: ${ext}`);
        this.save_dir = dir;
        this.save_fstem = fstem;
        access(dir, constants.F_OK, (err) => {
          if (!err){
            this.save_dir = dir;
          }
          else {
            console.error(`${dir} does not exist`);
          }
        })
          console.log(`${ext} in ${SUPPORTED_CREATE_EXTENSIONS} is false`)
        if (ext && ext.toLowerCase() in SUPPORTED_CREATE_EXTENSIONS){
          console.log(`${ext} in ${SUPPORTED_CREATE_EXTENSIONS} is true`)
          data.criteria.format = ext.toLowerCase();
        }
      }
    },*/
  },
  created() {
    window.addEventListener("resize", this.closeLoadPopper);
  },
  unmounted() {
    window.removeEventListener("resize", this.closeLoadPopper);
  },
  methods: {
    toggleLoadButtonAnim(ops, state = false) {
      if (ops == "insert") {
        this.CRT_INSERT_LOAD = state;
      } else if (ops == "smart_insert") {
        this.CRT_SMARTINSERT_LOAD = state;
      } else if (ops == "replace") {
        this.CRT_REPLACE_LOAD = state;
      }
    },
    btnToggleLoadPopper() {
      if (!this.popperIsVisible) {
      let popper = document.querySelector("#crtLoadPopper");
      let button = document.querySelector("#addPopperBtn");
      this.popper = createPopper(button, popper, {
        placement: 'top-start',
      });
      console.log("btnToggleLoadPopper");
      this.popperIsVisible = true;
      }
      else {
        this.popperIsVisible = false;
      }
    },
    closeLoadPopper(event) {
      console.log(`closeLoadPopper ${this.popperIsVisible}, ${this.popper}`);
      console.log(event);
      if (this.popperIsVisible) {
        this.popperIsVisible = false;
      }
    },
    btnLoadImages(ops) {
      console.log("crt load image with ops:", ops);
      let props = ops == "insert" ? imgs_dialog_props : img_dialog_props;
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

      ipcRenderer.invoke('open-dialog', options).then((result) => {
        let img_paths = result.filePaths;
        console.log(img_paths);
        if (img_paths === undefined || img_paths.length == 0) {
          return;
        }

        this.CRT_IS_LOADING = true;
        this.toggleLoadButtonAnim(ops, true);

        cmd_args.push(img_paths)

        tridentEngine(cmd_args, (error, res) => {
          if (error) {
            try {
              this._logError(error);
            }
            catch (e) {
              this._logError(error);
            }
            this.CRT_IS_LOADING = false;
            this.toggleLoadButtonAnim(ops, false);
          } else if (res) {
            if (res && res.msg) {
              this._logProcessing(res.msg);
            } else if (res && res.data) {
              let info = res.data;
              console.log("sequence info");
              console.log(info.sequence_info);
              console.log(info);
              this._renderSequence(info, { operation: ops });
              this.total_size = `Total size: ${info.total_size}`;
              // data.save_fstem = stem(data.save_fstem || info.name);
              this.fname = this.fname || info.name
              this.criteria.width = this.criteria.width || info.width;
              this.criteria.height = this.criteria.height || info.height;
              this.criteria.fps = this.criteria.fps || 50;
              this.criteria.delay = this.criteria.delay || 0.02;
              this.orig_width = info.width;
              this.orig_height = info.height;
              this.latest_load_count = info.total;
              this._logSuccess(`Loaded ${this.latest_load_count} images`);
              this._updateAspectRatio(this.criteria.width, this.criteria.height);
              this.CRT_IS_LOADING = false;
              this.toggleLoadButtonAnim(ops, false);
              this.lock_aspect_ratio = true;
            }
          }
        });
      });
    },
    _renderSequence(pyinfo, options) {
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
        if (this.insert_index) {
          this.image_paths.splice(this.insert_index, 0, ...pyinfo.sequence);
          this.sequence_info.splice(this.insert_index, 0, ...pyinfo.sequence_info);
        } else {
          this.image_paths.push(...pyinfo.sequence);
          this.sequence_info.push(...pyinfo.sequence_info);
        }
      // }
    },
    _setMinimalDimensions() {
      if (this.criteria.width == 0)
        this.criteria.width = 1;
      if (this.criteria.height == 0)
        this.criteria.height = 1;
    },
    previewAIMG() {
      console.log("preview called");
      this._logClear();
      if (this.sequence_info.length < 2) {
        this._logError("Please load at least 2 images!");
        return;
      }
      this._setMinimalDimensions();
      this.CRT_IS_PREVIEWING = true;
      let criteria_pack = {
        "criteria": this.criteria,
        "gif_opt_criteria": this.gif_opt_criteria,
        "apng_opt_criteria": this.apng_opt_criteria,
      };
      let preview_filename = `createPanel_preview_${Date.now()}_${randString(7)}.${this.criteria.format.toLowerCase()}`;
      let preview_savepath = join(PREVIEWS_PATH, preview_filename);
      console.log(preview_savepath);
      tridentEngine(["combine_image", this.image_paths, preview_savepath, criteria_pack], (error, res) => {
        if (error) {
          this._logError(error)
          this.CRT_IS_PREVIEWING = false;
        } else if (res) {
          if (res.msg) {
            this._logProcessing(res.msg);
          }
          if (res.preview_path) {
            this.preview_path = res.preview_path;
            this._previewPathCacheBreaker();
          }
        }},
        () => tridentEngine(["inspect_one", this.preview_path], (error, info) => {
          if (error) {
            console.error(error);
            this.CRT_IS_PREVIEWING = false;
          } else if (info) {
            let inspectionData = info.data;
            console.log("preview inspect");
            console.log(inspectionData);
            this.preview_info = inspectionData;
            this._logSuccess("Previewed!");
            this.CRT_IS_PREVIEWING = false;
          }
        })
      );
    },
    _previewPathCacheBreaker() {
      let cb_url = `${this.preview_path}`;
      console.log("Cache breaker url", cb_url);
      this.preview_path_cb = cb_url;
    },
    removeFrame(index) {
      this.image_paths.splice(index, 1);
      this.sequence_info.splice(index, 1);
    },
    btnClearAll() {
      console.log(this.emitter == emitter);
      this.clearSequence();
      this.clearPreviewAIMG();
      this.clearAuxInfo();
      this.clearFields();
      this.lock_aspect_ratio = false;
    },
    clearSequence() {
      this.image_paths = [];
      this.sequence_info = [];
      this.save_fstem = "";
    },
    clearPreviewAIMG() {
      this.preview_path = "";
      this.preview_path_cb = "";
      this.preview_info = "";
    },
    clearAuxInfo() {
      this.total_size = "";
      this.orig_width = "";
      this.old_width = "";
      this.orig_height = "";
      this.old_height = "";
      this._logClear();
      let empty_aspect_ratio = {
        w_ratio: "",
        h_ratio: "",
        text: "",
      };
      this.aspect_ratio = empty_aspect_ratio;
    },
    clearFields() {
      this.criteria.name = "";
      this.criteria.delay = "";
      this.criteria.fps = "";
      this.criteria.loop_count = "";
      this.criteria.width = "";
      this.criteria.height = "";
    },
    btnPreviewAIMG() {
      this.previewAIMG();
    },
    btnSetSavePath() {
      this.setSaveDirFromDialogAsync();
    },
    async setSaveDirFromDialogAsync() {
      let options = { properties: dir_dialog_props };
      let dirPath;
      const result = await ipcRenderer.invoke('open-dialog', options);
      if (result.canceled) {
        return {canceled: true, result: dirPath};
      }
      let out_dirs = result.filePaths;
      console.log(out_dirs);
      if (out_dirs && out_dirs.length > 0) { 
        this.save_dir = out_dirs[0];
        dirPath = this.save_dir;
      }
      this._logClear();
      return {canceled: false, result: dirPath};
    },
    async validateFilenameAsync() {
      if (validateFilename(this.fname))
        return true;
      else
        return false;
    },
    btnCreateAIMG() {
      if (this.sequence_info.length < 2) {
        this._logError("Please load at least 2 messages!");
        // this.create_msgbox = "Please load at least 2 images!";
        return;
      }
      this.validateFilenameAsync().then(async (isValid) => {
        if (isValid) {
          if (!this.save_dir) {
            const result = await this.setSaveDirFromDialogAsync()
            if (result.canceled)
              return Promise.reject("Directory selection cancelled");
            else
              return this._checkFileOverwriteAsync();
          }
          else 
            return this._checkFileOverwriteAsync();
        }
        else {
          let errMsg = "File name contains characters that are not allowed";
          this._logError(errMsg);
          return Promise.reject(errMsg);
        }
      }).then((proceed) => {
        console.log(`proceed create ${proceed}`);
        if (proceed)
          this.createAnimatedImage();
        else
          return;
      }).catch((error) => {
        console.error(error);
      });

      // if (this.save_dir) {
      //   if (!validateFilename(this.fname)) {
      //     this._logError("File name contains characters that are not allowed");
      //     return;
      //   }
      //   this._checkFileOverwriteAsync().then((proceed_create) => {
      //     if (proceed_create)
      //       this.createAnimatedImage();
      //     else
      //       return;
      //   })
      // }
      // else {
      //   this.setSaveDirFromDialogAsync().then((result) => {
      //     if (result.canceled)
      //       return Promise.reject("Directory selection cancelled");
      //     else
      //       return this._checkFileOverwriteAsync()
      //   }).then((proceed_create) => {
      //     console.log(`proceed_create ${proceed_create}`);
      //     if (proceed_create)
      //       this.createAnimatedImage();
      //     else
      //       return Promise.reject("Cancelled creation");
        // }).catch((error) => {
        //   console.error(error);
        // });
      // }
    },
    async _checkFileOverwriteAsync() {
      let proceed = true;
      if (existsSync(this._getSavePath())) {
        let options = {
          title: "TridentFrame",
          buttons: ["Yes", "No"],
          message:
            "A file with the same name already exists in the output folder and it will get overwritten. Do you want to proceed?",
        };
        const promptResult = await ipcRenderer.invoke("show-msg-box", options);
        console.log(`msgbox promptResult:`);
        console.log(promptResult);
        if (promptResult.response == 1) proceed = false;
      }
      return proceed;
    },
    createAnimatedImage() {
      // let proceed_create = true;
      this._logClear();
      // this.create_msgbox = "";
      this._setMinimalDimensions();

      this.CRT_IS_CREATING = true;
      let criteria_pack = {
        "criteria": this.criteria,
        "gif_opt_criteria": this.gif_opt_criteria,
        "apng_opt_criteria": this.apng_opt_criteria,
      };
      tridentEngine(["combine_image", this.image_paths, this._getSavePath(), criteria_pack], (error, res) => {
        if (error) {
          try {
            this._logError(error);
            // this.create_msgbox = error;
            this.CRT_IS_CREATING = false;
          }
          catch (e) {
            this._logError(e);
            // this.create_msgbox = error;
          }
        } else if (res) {
          console.log(`res -> ${res}`);
          if (res) {
            console.log(res);
            if (res.msg) {
              this._logProcessing(res.msg);
              // this.create_msgbox = res.msg;
            }
          }
        }
      },
      () => {
        this._logSuccess(`${this.criteria.format.toUpperCase()} created!`);
        // this.create_msgbox = `${this.criteria.format.toUpperCase()} created!`;
        this.CRT_IS_CREATING = false;
      });
    },
    btnToggleCheckerBG() {
      this.checkerbg_active = !this.checkerbg_active;
      console.log("now checkerbg is", this.checkerbg_active);
    },
    _getFullFilename() {
      return `${this.fname}.${this.criteria.format}`;
    },
    _getSavePath() {
      let file_name = this._getFullFilename();
      let save_path = join(this.save_dir, file_name);
      console.log(`getSavePath ${save_path}`);
      return save_path;
    },
    numConstrain: numConstrain,
    widthHandler(width, event) {
      this.old_width = parseInt(width);
      let newWidth = event.target.value;
      this.criteria.width = parseInt(newWidth);
      if (this.lock_aspect_ratio && this.aspect_ratio.h_ratio > 0) {
        // Change height if lock_aspect_ratio is true and height is not 0
        let raHeight = Math.round(
          (newWidth / this.aspect_ratio.w_ratio) * this.aspect_ratio.h_ratio
        );
        this.criteria.height = raHeight > 0 ? parseInt(raHeight) : "";
      } else {
        this._updateAspectRatio(this.criteria.width, this.criteria.height);
      }
    },
    heightHandler(height, event) {
      this.old_height = parseInt(height);
      let newHeight = event.target.value;
      this.criteria.height = parseInt(newHeight);
      if (this.lock_aspect_ratio && this.aspect_ratio.w_ratio > 0) {
        let raWidth = Math.round(
          (newHeight / this.aspect_ratio.h_ratio) * this.aspect_ratio.w_ratio
        );
        console.log(raWidth);
        this.criteria.width = raWidth > 0 ? parseInt(raWidth) : "";
      } else {
        this._updateAspectRatio(this.criteria.width, this.criteria.height);
      }
    },
    _updateAspectRatio(width, height) {
      if (this.criteria.width && this.criteria.height) {
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
        this.aspect_ratio = ARData;
      }
    },
    delayConstrain(event) {
      console.log("delay event", event);
      let value = event.target.value;
      if (value && value.includes(".")) {
        let numdec = value.split(".");
        console.log("numdec", numdec);
        let precision = 2;
        if (this.criteria.format.toUpperCase() == "GIF") {
          precision = GIF_DELAY_DECIMAL_PRECISION;
        } else if (this.criteria.format.toUpperCase() == "PNG") {
          precision = APNG_DELAY_DECIMAL_PRECISION;
        }
        if (numdec[1].length > precision) {
          let decs = numdec[1].substring(0, precision);
          console.log("decs limit triggered", decs);
          this.criteria.delay = `${numdec[0]}.${decs}`;
        }
      }
      this.criteria.fps = Math.round(1000 / this.criteria.delay) / 1000;
    },
    fpsConstrain(event) {
      console.log("fps event", event);
      let value = event.target.value;
      if (value) {
        let mult = 100;
        if (this.criteria.format.toUpperCase() == "GIF") {
          mult = 100;
        } else if (this.criteria.format.toUpperCase() == "PNG") {
          mult = 1000;
        }
        this.criteria.delay = Math.round(mult / this.criteria.fps) / mult;
      }
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
    escapeLocalPath: escapeLocalPath,
  },
};
</script>
