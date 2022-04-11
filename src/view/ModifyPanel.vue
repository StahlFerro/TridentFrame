<template>
  <div id="modify_panel">
    <div class="modify-panel-root">
      <div class="modify-panel-displays">
        <div
          class="modify-old-container silver-bordered-no-right"
          :class="{'has-checkerboard-bg': orig_checkerbg_active }"
        >
          <img :src="escapeLocalPath(orig_attribute.path)" />
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
                <td class="mod-info-label is-cyan">
                  Dimensions
                </td>
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
                    <br />
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
                <td class="mod-info-label is-cyan">
                  Format
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ preview_attribute.format }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.frame_count }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  Total frames
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_info">{{ preview_attribute.frame_count }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.fps }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  Frame rate
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_info">{{ preview_attribute.fps }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ orig_attribute.delay_info }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  Avg. Delay
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ preview_attribute.delay_info }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute && orig_attribute.loop_duration">{{ roundPrecise(orig_attribute.loop_duration, 3) }} seconds</span>
                </td>
                <td class="mod-info-label is-cyan">
                  Loop duration
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute && preview_attribute.loop_duration">{{ roundPrecise(preview_attribute.loop_duration, 3) }} seconds</span>
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
                <td class="mod-info-label is-cyan">
                  Loop count
                </td>
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
        <div
          class="modify-new-container silver-bordered-no-left" 
          :title="preview_info?
            `Dimensions: ${preview_info.general_info.width.value} x ${preview_info.general_info.height.value}\n` +
            `File size: ${preview_info.general_info.fsize_hr.value}\n` +
            `Loop count: ${preview_info.animation_info.loop_count.value || 'Infinite'}\n` +
            `Format: ${preview_info.general_info.format.value}` : ''
          "
          :class="{'has-checkerboard-bg': new_checkerbg_active }"
        >
          <img :src="escapeLocalPath(preview_path_cb)" />
        </div>
      </div>
      <div class="modify-panel-middlebar">
        <div class="mpb-load-buttons">
          <a class="button is-neon-emerald" :class="{'is-loading': MOD_IS_LOADING, 'non-interactive': buttonIsFrozen}" @click="loadImage">
            <span class="icon is-small">
              <font-awesome-icon icon="plus" />
            </span>
            <span>Load Image</span>
          </a>
          <a class="button is-neon-crimson" :class="{'non-interactive': buttonIsFrozen}" @click="clearImage">
            <span class="icon is-small">
              <font-awesome-icon icon="times" />
            </span>
            <span>Clear</span>
          </a>
          <a
            class="button is-neon-white" :class="{'is-active': orig_checkerbg_active}"
            @click="toggleOrigCheckerBG"
          >
            <span class="icon is-medium">
              <font-awesome-icon icon="chess-board" />
            </span>
          </a>
        </div>
        <div class="mpb-center-buttons" />
        <div class="mpb-preview-buttons">
          <a class="button is-neon-cyan" :class="{'is-loading': MOD_IS_PREVIEWING, 'non-interactive': buttonIsFrozen}" @click="previewModImg">
            <span class="icon is-small">
              <font-awesome-icon :icon="['far', 'eye']" />
            </span>
            <span>Preview</span>
          </a>
          <a class="button is-neon-crimson" :class="{'non-interactive': buttonIsFrozen}" @click="clearPreviewImage">
            <span class="icon is-small">
              <font-awesome-icon icon="times" />
            </span>
            <span>Clear</span>
          </a>
          <a
            class="button is-neon-white" :class="{'is-active': new_checkerbg_active}"
            @click="toggleNewCheckerBG"
          >
            <span class="icon is-medium">
              <font-awesome-icon icon="chess-board" />
            </span>
          </a>
        </div>
      </div>
      <div class="modify-panel-controls">
        <div class="mpc-left-panel">
          <aside class="menu has-text-centered" style="margin: 0;">
            <ul class="menu-list">
              <li
                id="MOD_box_general" class="subtab-menu-item"
                :class="{'is-selected': mod_menuselection == 0}"
              >
                <a id="MOD_menu_general" @click="mod_menuselection = 0">
                  <span class="icon is-large">
                    <font-awesome-icon icon="image" size="2x" inverse />
                    <!-- <i class="fas fa-image fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d">General</p>
                </a>
              </li>
              <li
                id="MOD_box_gif" class="subtab-menu-item is-cyan"
                :class="{'is-selected': mod_menuselection == 1}"
              >
                <a
                  id="MOD_menu_gif" :class="{'is-disabled': criteria.format != 'gif'}"
                  @click="mod_menuselection = 1"
                >
                  <span class="icon is-large">
                    <font-awesome-icon icon="images" size="2x" inverse />
                    <!-- <i class="far fa-images fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d is-large">GIF</p>
                </a>
              </li>
              <li
                id="MOD_box_apng" class="subtab-menu-item"
                :class="{'is-selected': mod_menuselection == 2}"
              >
                <a
                  id="MOD_menu_apng" :class="{'is-disabled': criteria.format != 'png'}"
                  @click="mod_menuselection = 2"
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
        <div class="mpc-right-panel">
          <div class="mpc-right-top-panel">
            <div v-show="mod_menuselection == 0">
              <table class="" width="100%">
                <tr>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label">Name</label>
                      <div class="control">
                        <input v-model="fname" class="input is-neon-white" type="text" />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label">Width</label>
                      <div class="control">
                        <input
                          :value="criteria.width" class="input is-neon-white" type="number" 
                          min="1" step="1" @keydown="numConstrain($event, true, true)" @input="widthHandler(criteria.width, $event)"
                        />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label">Height</label>
                      <div class="control">
                        <input
                          :value="criteria.height" class="input is-neon-white" type="number"
                          min="1" step="1" @keydown="numConstrain($event, true, true)" @input="heightHandler(criteria.height, $event)"
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
                  <td width="16.7%" class="force-vcenter">
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
                  <td width="16.7%" class="force-vcenter">
                    <label class="checkbox" title="Reverse the animation">
                      <input v-model="criteria.is_reversed" type="checkbox" />
                      Reversed
                    </label>
                    <br />
                    <!-- <label class="checkbox" title="Preserve transparent pixels">
                      <input v-model="preserve_alpha" type="checkbox" />
                      Preserve Alpha
                    </label> -->
                    <label class="checkbox">
                      <input v-model="lock_aspect_ratio" type="checkbox" />
                      Lock aspect ratio
                    </label>
                  </td>
                </tr>
                <tr>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label">Frame rate</label>
                      <div class="control">
                        <input
                          v-model="criteria.fps" class="input is-neon-white" type="number" min="0"
                          @input="fpsConstrain" @keydown="numConstrain($event, true, false)"
                        />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label">Delay (seconds)</label>
                      <div class="control">
                        <input
                          v-model="criteria.delay" class="input is-neon-white" type="number" min="0"
                          @input="delayConstrain" @keydown="numConstrain($event, true, false)"
                        />
                      </div>
                    </div>
                  </td>
                  <td width="16.7%">
                    <div class="field">
                      <label class="label">Loop count</label>
                      <div class="control">
                        <input
                          v-model="criteria.loop_count" class="input is-neon-white" type="number" min="0"
                          @keydown="numConstrain($event, true, true)"
                        />
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
                  <td width="16.7%" />
                  <td width="16.7%" class="force-vcenter">
                    <!-- <label class="checkbox">
                      <input v-model="lock_aspect_ratio" type="checkbox"/>
                      Lock aspect ratio
                    </label> -->
                    <br />
                    <template v-if="aspect_ratio && aspect_ratio.text">
                      <input v-model="aspect_ratio.text" class="input is-border-colorless is-paddingless" style="height: 1.5em;" readonly="readonly" />
                    </template>
                    <template v-else>
                      &nbsp;
                    </template>
                  </td>
                </tr>
                <tr />
                <tr>
                  <td colspan="4">
                    <div class="field has-addons">
                      <div class="control">
                        <a class="button is-neon-cyan" @click="btnSetSavePath">
                          <span class="icon is-small">
                            <font-awesome-icon icon="save" />
                            <!-- <i class="fas fa-save"></i> -->
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
                  <td colspan="1">
                    <div class="field">
                      <div class="control">
                        <div class="select is-neon-cyan" :class="{'non-interactive': buttonIsFrozen}">
                          <select v-model="criteria.format">
                            <option v-for="(item, name, index) in SUPPORTED_MODIFY_EXTENSIONS" :key="index" :value="name">
                              {{ item }}
                            </option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td colspan="1">
                    <a class="button is-neon-cyan" :class="{'is-loading': MOD_IS_MODIFYING, 'non-interactive': buttonIsFrozen}" @click="btnModifyImage">
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
                <GIFUnoptimizationRow
                  v-model:is_optimized="gif_opt_criteria.is_optimized"
                  v-model:is_lossy="gif_opt_criteria.is_lossy"
                  v-model:is_reduced_color="gif_opt_criteria.is_reduced_color"
                  v-model:is_unoptimized="gif_opt_criteria.is_unoptimized"
                />
              </table>
            </div>
            <div v-show="mod_menuselection == 2">
              <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
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
                <APNGUnoptimizationRow
                  v-model:apng_is_optimized="apng_opt_criteria.apng_is_optimized"
                  v-model:apng_is_lossy="apng_opt_criteria.apng_is_lossy"
                  v-model:apng_is_unoptimized="apng_opt_criteria.apng_is_unoptimized"
                />
              </table>
            </div>
          </div>
          <div class="mpc-right-bottom-panel">
            <StatusBar :status-bar-id="statusBarId" />
          </div>
        </div>
      </div>
    </div>
    <!-- </div> -->
  </div>
</template>

<script>

import { ipcRenderer } from 'electron';
import { tridentEngine } from "../modules/streams/trident_engine";
import { roundPrecise, gcd } from "../modules/utility/calculations";
import { floatConstrain, numConstrain } from "../modules/events/constraints";
import { GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION } from "../modules/constants/images";
import { randString } from "../modules/utility/stringutils";
import { escapeLocalPath, stem, validateFilename } from "../modules/utility/pathutils";
import { structuredClone } from "../modules/utility/objectutils";
import { PREVIEWS_PATH } from "../common/paths";

import { dirname, join, basename } from "path";
import GIFOptimizationRow from "./components/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./components/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./components/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./components/APNGUnoptimizationRow.vue";
import { existsSync } from 'fs';

import StatusBar from "./components/StatusBar.vue";
import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";
// import Vue from 'vue';

const SUPPORTED_MODIFY_EXTENSIONS = {
  'gif': 'GIF',
  'png': 'APNG',
}

let common_metadata = {
  fname: "",
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

let extension_filters = [
    { name: 'Images', extensions: Object.keys(SUPPORTED_MODIFY_EXTENSIONS) },
];
let file_dialog_props = ['openfile'];
let dir_dialog_props = ['openDirectory', 'createDirectory'];


export default {
  components: {
    GIFOptimizationRow,
    GIFUnoptimizationRow,
    APNGOptimizationRow,
    APNGUnoptimizationRow,
    StatusBar,
  },
  data: function() {
    return {
      orig_attribute: structuredClone(common_metadata),
      preview_attribute: structuredClone(common_metadata),
      criteria: {
        width: "",
        height: "",
        resize_method: "BICUBIC",
        rotation: "",
        fps: "",
        delay: "",
        loop_count: "",
        format: "gif",
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
        apng_convert_color_mode: false,
        apng_new_color_mode: "RGBA",
      },
      fname: "",
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
      SUPPORTED_MODIFY_EXTENSIONS: SUPPORTED_MODIFY_EXTENSIONS,
      statusBarId: "modifyPanelStatusBar",
      // statusBarBus: new Vue(),
    };
  },
  computed: {
    origDimensions() {
      if (this.orig_attribute.width && this.orig_attribute.height) {
        return `${this.orig_attribute.width} x ${this.orig_attribute.height}`;
      }
      else {
        return "";
      }
    },
    previewDimensions() {
      if (this.preview_attribute.width && this.preview_attribute.height) {
        return `${this.preview_attribute.width} x ${this.preview_attribute.height}`;
      }
      else {
        return "";
      }
    },
    buttonIsFrozen() {
      if (this.MOD_IS_LOADING || this.MOD_IS_MODIFYING || this.MOD_IS_PREVIEWING) return true;
      else return false;
    },
    previewSizePercentage() {
      if (this.orig_attribute.path && this.preview_attribute.path) {
        let oldSize = this.orig_attribute.file_size
        let previewSize = this.preview_attribute.file_size;
        console.log(oldSize, previewSize);
        let newSizePercentage = (previewSize / oldSize * 100).toFixed(2);
        let text = `${newSizePercentage}%`;
        return text;
      }
      else return "";
    },
  },
  methods: {
    loadOrigMetadata(res) {
      let geninfo = res.general_info;
      let ainfo = res.animation_info;
      this.orig_attribute.name = geninfo.name.value;
      this.save_fstem = stem(this.save_fstem || geninfo.name.value);
      this.orig_attribute.width = geninfo.width.value;
      this.orig_attribute.height = geninfo.height.value;
      this.orig_attribute.fps = `${ainfo.fps.value} FPS`;
      this.orig_attribute.frame_count= ainfo.frame_count.value;
      this.orig_attribute.format = geninfo.format.value;
      let delay_info = `${roundPrecise(ainfo.average_delay.value, 3)} ms`;
      if (ainfo.delays_are_even.value) {
        delay_info += ` (even)`;
      }
      else {
        delay_info += ` (uneven)`;
      }
      this.orig_attribute.delay = ainfo.average_delay.value;
      this.orig_attribute.delay_info = delay_info;
      this.orig_attribute.loop_duration = ainfo.loop_duration.value;
      if (ainfo.loop_count.value == 0) {
        this.orig_attribute.loop_count = "Infinite"
      }
      else {
        this.orig_attribute.loop_count = ainfo.loop_count.value;
      }
      this.orig_attribute.path = geninfo.absolute_url.value;
      this.orig_attribute.file_size = geninfo.fsize.value;
      this.orig_attribute.file_size_hr = geninfo.fsize_hr.value;
      this.orig_attribute.last_modified_dt = geninfo.modification_datetime.value;
      this.orig_attribute.hash_sha1 = geninfo.hash_sha1.value;
    },
    loadPreviewMetadata(res) {
      let geninfo = res.general_info;
      let ainfo = res.animation_info;
      this.preview_attribute.name = geninfo.name.value;
      this.preview_attribute.width = geninfo.width.value;
      this.preview_attribute.height = geninfo.height.value;
      this.preview_attribute.fps = `${ainfo.fps.value} FPS`;
      this.preview_attribute.frame_count= ainfo.frame_count.value;
      this.preview_attribute.format = geninfo.format.value;
      let delay_info = `${roundPrecise(ainfo.average_delay.value, 3)} ms`;
      if (ainfo.delays_are_even.value) {
        delay_info += ` (even)`;
      }
      else {
        delay_info += ` (not even)`;
      }
      this.preview_attribute.delay = ainfo.average_delay.value;
      this.preview_attribute.delay_info = delay_info;
      this.preview_attribute.loop_duration = ainfo.loop_duration.value;
      if (ainfo.loop_count.value == 0) {
        this.preview_attribute.loop_count = "Infinite"
      }
      else {
        this.preview_attribute.loop_count = ainfo.loop_count.value;
      }
      this.preview_attribute.path = geninfo.absolute_url.value;
      this.preview_attribute.file_size = geninfo.fsize.value;
      this.preview_attribute.file_size_hr = geninfo.fsize_hr.value;
      this.preview_attribute.last_modified_dt = geninfo.modification_datetime.value;
      this.preview_attribute.hash_sha1 = geninfo.hash_sha1.value;
    },
    populateForm(res) {
      var geninfo = res.general_info;
      var ainfo = res.animation_info;
      this.fname = geninfo.base_filename.value;
      this.criteria.format = geninfo.format.value.toLowerCase();
      this.criteria.width = geninfo.width.value;
      this.criteria.height = geninfo.height.value;
      this.criteria.delay = roundPrecise(ainfo.average_delay.value, 3) / 1000;
      this.criteria.fps = roundPrecise(ainfo.fps.value, 3);
      this.criteria.loop_count = ainfo.loop_count.value;
      this.updateAspectRatio(this.criteria.width, this.criteria.height);
    },
    updateAspectRatio(width, height) {
      if (this.criteria.width && this.criteria.height) {
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
        this.aspect_ratio = ARData;
      }
    },
    loadImage() {
      console.log("mod load image called");
      var options = {
        filters: extension_filters,
        properties: file_dialog_props
      };
      ipcRenderer.invoke('open-dialog', options).then((result) => {
        let chosen_path = result.filePaths;
        console.log(`chosen path: ${chosen_path}`);
        if (chosen_path === undefined || chosen_path.length == 0) {
          return;
        }
        this.MOD_IS_LOADING = true;
        this._logProcessing("Loading image...");
        tridentEngine(["inspect_one", chosen_path[0], "animated"], (error, res) => {
          if (error) {        
            try {
              this._logError(error);
              // this.modify_msgbox = error;
            }
            catch (e) {
              this._logError(e);
              // this.modify_msgbox = error;
            }
            // mboxError(split_msgbox, error);
            this.MOD_IS_LOADING = false;
          } else if (res) {
            if (res && res.msg) {
              this._logProcessing(res.msg);
            } else if (res && res.data) {
              this.loadOrigMetadata(res.data);
              this.populateForm(res.data);
              this._logSuccess("Image loaded.");
            }
            this.MOD_IS_LOADING = false;
            this.lock_aspect_ratio = true;
          }
        });
        console.log("registered!");
      });
    },
    clearOrigMetadata() {
      this.orig_attribute.name = "";
      this.orig_attribute.width = "";
      this.orig_attribute.height = "";
      this.orig_attribute.frame_count = "";
      this.orig_attribute.frame_count_ds = "";
      this.orig_attribute.fps = "";
      this.orig_attribute.delay = "";
      this.orig_attribute.delay_info = "";
      this.orig_attribute.loop_duration = "";
      this.orig_attribute.loop_count = "";
      this.orig_attribute.file_size = "";
      this.orig_attribute.file_size_hr = "";
      this.orig_attribute.format = "";
      this.orig_attribute.path = "";
      this.orig_attribute.hash_sha1 = "";
      this.orig_attribute.last_modified_dt = "";
      this._logClear();
    },
    clearPreiewMetadata() {
      this.preview_attribute.name = "";
      this.preview_attribute.width = "";
      this.preview_attribute.height = "";
      this.preview_attribute.frame_count = "";
      this.preview_attribute.frame_count_ds = "";
      this.preview_attribute.fps = "";
      this.preview_attribute.delay = "";
      this.preview_attribute.delay_info = "";
      this.preview_attribute.loop_duration = "";
      this.preview_attribute.loop_count = "";
      this.preview_attribute.file_size = "";
      this.preview_attribute.file_size_hr = "";
      this.preview_attribute.format = "";
      this.preview_attribute.path = "";
      this.preview_attribute.hash_sha1 = "";
      this.preview_attribute.last_modified_dt = "";
      this._logClear();
    },
    clearCriteriaFields() {
      this.criteria.old_width = "";
      this.criteria.width = "";
      this.criteria.old_height = "";
      this.criteria.height = "";
      this.criteria.rotation = "";
      this.criteria.fps = "";
      this.criteria.delay = "";
      this.criteria.loop_count = "";
      this.criteria.skip_frame = "";
      this._logClear();
      // this.criteria.modify_msgbox = "";
      let ARData = {
        "w_ratio": "",
        "h_ratio": "",
        "text": "",
      };
      this.aspect_ratio = ARData;
    },
    clearImage() {
      this.clearOrigMetadata();
      this.clearCriteriaFields();
      this.clearPreviewImage();
      this.lock_aspect_ratio = false;
    },
    clearPreviewImage() {
      this.preview_path = "";
      this.preview_path_cb = "";
      this.preview_size = "";
      this.preview_size_hr = "";
      this.clearPreiewMetadata();
    },
    btnSetSavePath() {
      // setSavePath();
      this.setSaveDirFromDialogAsync();
    },
    async setSaveDirFromDialogAsync() {
      let options = { properties: dir_dialog_props };
      let dirPath;
      const result = await ipcRenderer.invoke('open-dialog', options);
      if (result.canceled)
        return {canceled: true, result: dirPath};
      let out_dirs = result.filePaths;
      console.log(out_dirs);
      if (out_dirs && out_dirs.length > 0) { 
        this.save_dir = out_dirs[0];
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
    btnModifyImage() {
      if (!this.orig_attribute.path) {
        this._logError("Please load an image first!");
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
        console.log(`proceed modify ${proceed}`);
        if (proceed)
          this.modifyImage();
        else
          return;
      }).catch((error) => {
        console.error(error);
      });


      
    // if (this.save_dir)
    //   this.modifyImage();
    // else
    //   this.setSaveDirFromDialogAsync().then((result) => {
    //     if (result.canceled)
    //       return Promise.reject("Directory selection cancelled.");
    //     else
    //       return this._checkFileOverwriteAsync();
    //   }).then((proceed) => {
    //     console.log(`proceed_create ${proceed}`);
    //     if (proceed)
    //       this.modifyImage();
    //     else
    //       return Promise.reject("Cancelled modification");
    //   });
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
    // chooseOutDir: chooseOutDir,
    previewModImg() {
      if (this.orig_attribute.path == "") {
        this._logError("Please load an animated image first!");
        return;
      }
      this.MOD_IS_PREVIEWING = true;
      let criteria_pack = {
        "criteria": { ...this.criteria, "hash_sha1": this.orig_attribute.hash_sha1, "last_modified_dt": this.orig_attribute.last_modified_dt },
        "gif_opt_criteria": this.gif_opt_criteria,
        "apng_opt_criteria": this.apng_opt_criteria,
      };
      let preview_filename = `modifyPanel_preview_${Date.now()}_${randString(7)}.${this.criteria.format.toLowerCase()}`;
      let preview_savepath = join(PREVIEWS_PATH, preview_filename);
      // criteria_pack.criteria.name += `_preview_${Date.now()}_${randString(7)}`;
      tridentEngine(["modify_image", this.orig_attribute.path, preview_savepath, criteria_pack], (error, res) => {
        if (error) {
          console.error(error);
          this._logError(error);
          // this.modify_msgbox = error;
          this.MOD_IS_PREVIEWING = false;
        }
        else if (res) {
          if (res.msg) {
            this._logProcessing(res.msg);
          }
          if (res.preview_path) {
            this.preview_path = res.preview_path;
            this.previewPathCacheBreaker();
          }
        }
      },
      () => tridentEngine(["inspect_one", this.preview_path, "animated"], (error, res) => {
        if (error) {
          console.error(error);
          this._logError(error);
        } else if (res && res.data) {
          let preview_data = res.data;
          console.log(`res -> ${res}`);
          console.log("preview inspect");
          this.loadPreviewMetadata(preview_data);
          this.preview_info = preview_data;
          this.preview_size = preview_data.general_info.fsize.value;
          this.preview_size_hr = preview_data.general_info.fsize_hr.value;
          this._logSuccess("Previewed!")
          this.MOD_IS_PREVIEWING = false;
        }})
      );
    },
    previewPathCacheBreaker() {
      let cb_url = `${this.preview_path}`;
      console.log("Cache breaker url", cb_url);
      this.preview_path_cb = cb_url;
    },
    modifyImage() {
      let proceed_modify = true;
      this._logClear();
      
      if (proceed_modify) {
        this.MOD_IS_MODIFYING = true;
        let criteria_pack = {
          "criteria": { ...this.criteria, "hash_sha1": this.orig_attribute.hash_sha1, "last_modified_dt": this.orig_attribute.last_modified_dt },
          "gif_opt_criteria": this.gif_opt_criteria,
          "apng_opt_criteria": this.apng_opt_criteria,
        };
        // criteria_pack.criteria.name += `_preview_${Date.now()}_${randString(7)}`;
        tridentEngine(["modify_image", this.orig_attribute.path, this._getSavePath(), criteria_pack], (error, res) => {
          if (error) {
            console.error(error);
            this._logError(error);
            this.MOD_IS_MODIFYING = false;
          }
          else if (res) {
            console.log(res);
            if (res.msg) {
              this._logProcessing(res.msg);
            }
          }
        },
        () => {
          this._logSuccess("Modified and saved!");
          this.MOD_IS_MODIFYING = false;
        });
      }
    },
    widthHandler(width, event) {
      // data.orig_attribute.width = parseInt(width);
      console.log(event);
      let newWidth = event.target.value;
      this.criteria.width = newWidth;
      if (this.lock_aspect_ratio && this.aspect_ratio.h_ratio > 0) { // Change height if lock_aspect_ratio is true and height is not 0
        let raHeight = Math.round(newWidth / this.aspect_ratio.w_ratio * this.aspect_ratio.h_ratio);
        this.criteria.height = raHeight > 0? raHeight : "";
      }
      else {
        this.updateAspectRatio(this.criteria.width, this.criteria.height);
      }
    },
    heightHandler(height, event) {
      // data.orig_attribute.height = parseInt(height);
      let newHeight = event.target.value;
      this.criteria.height = newHeight;
      if (this.lock_aspect_ratio && this.aspect_ratio.w_ratio > 0) {
        let raWidth = Math.round(newHeight / this.aspect_ratio.h_ratio * this.aspect_ratio.w_ratio);
        console.log(raWidth);
        this.criteria.width = raWidth > 0? raWidth : "";
      }
      else {
        this.updateAspectRatio(this.criteria.width, this.criteria.height);
      }
    },
    toggleOrigCheckerBG() {
      this.orig_checkerbg_active = !this.orig_checkerbg_active;
      console.log("orig checkerbg is", this.orig_checkerbg_active);
    },
    toggleNewCheckerBG() {
      this.new_checkerbg_active = !this.new_checkerbg_active;
      console.log("new checkerbg is", this.new_checkerbg_active);
    },
    _getSavePath() {
      let file_name = `${this.fname}.${this.criteria.format}`;
      let save_path = join(this.save_dir, file_name);
      console.log(`getSavePath ${save_path}`);
      return save_path;
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
    floatConstrain: floatConstrain,
    numConstrain: numConstrain,
    roundPrecise: roundPrecise,
    escapeLocalPath: escapeLocalPath,
  }
};
</script>
