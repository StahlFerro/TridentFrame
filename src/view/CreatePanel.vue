<template>
  <div id="create_panel">
    <div class="create-panel-root">
      <div class="create-panel-display">
        <div class="create-panel-sequence silver-bordered">
          <div class="rtable rtable-5cols">
            <div
              v-for="(item, index) in imageSequenceInfo" :key="index" class="rtable-cell"
              :title="imageSequenceInfo?                    
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
          :title="computePreviewImageSummary"
          :class="{'has-checkerboard-bg': checkerBGIsActive }"
        >
          <!-- <div v-if="previewInfo" class="crt-aimg-container"> -->
          <img v-if="previewInfo" :src="escapeLocalPath(previewPathCB)" />
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
              v-model="insertIndex" class="input is-neon-white" type="number" min="0" style="width: 70px"
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
            <span v-if="imageSequenceInfo.length &gt; 0" class="is-white-d">Total: {{ computeTotalSequenceSize }} </span>
          </div>
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
          <a class="button is-neon-cyan" :class="{'non-interactive': isButtonFrozen}" @click="btnPreviewSaveAIMG">
            <span class="icon is-medium">
              <font-awesome-icon icon="save" />
            </span>
          </a>
          <a
            class="button is-neon-white" :class="{'is-active': checkerBGIsActive}"
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
              <li class="subtab-menu-item" :class="{ 'is-selected': crtSubMenuSelection == 0 }">
                <a @click="crtSubMenuSelection = 0">
                  <span class="icon is-large">
                    <font-awesome-icon :icon="['far', 'image']" size="2x" inverse />
                    <!-- <i class="fas fa-image fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d">General</p>
                </a>
              </li>
              <li
                class="subtab-menu-item is-cyan"
                :class="{ 'is-selected': crtSubMenuSelection == 1 }"
              >
                <a @click="crtSubMenuSelection = 1">
                  <span class="icon is-large">
                    <font-awesome-icon icon="sliders" size="2x" inverse />
                    <!-- <i class="far fa-images fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d">Advanced</p>
                </a>
              </li>
            </ul>
          </aside>
        </div>
        <div class="cpc-right-panel">
          <div class="cpc-right-top-panel">
            <div v-show="crtSubMenuSelection == 0">
              <div class="general-form row-6">
                <div class="field-cell">
                  <InputField v-model="fname" label="Name" type="text" hint="The name of the GIF/APNG" />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.width" label="Width" type="number" hint="The width of the animated image"
                              :constraint-option="{ handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true }}"
                              @field-input="widthHandler"
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.height" label="Height" type="number" 
                              hint="The height of the animated image"
                              :constraint-option="{handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true}}" 
                              @field-input="heightHandler"
                  />
                </div>
                <div class="field-cell">
                  <DropdownField v-model="criteria.resize_method" :options-list="RESIZE_METHODS" label="Resize method" />
                </div>
                <div class="field-cell">
                  <CheckboxField v-model="lockAspectRatio" label="Lock aspect ratio" hint="Lock the width and height ratio" />
                  <!-- <label class="checkbox">
                    <input v-model="lockAspectRatio" type="checkbox" />
                    Lock aspect ratio
                  </label> -->
                  <br />
                  <template v-if="aspectRatio && aspectRatio.text">
                    <input
                      v-model="aspectRatio.text"
                      class="input is-border-colorless is-paddingless"
                      style="height: 1.5em"
                      readonly="readonly"
                    />
                  </template>
                  <template v-else>
                    &nbsp;
                  </template>
                </div>
                <div class="field-cell">
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.delay" label="Delay (seconds)" type="number" hint="The time needed to move to the next frame"
                              :constraint-option="{ handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: false }}"
                              @field-input="delayHandler" 
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.fps" label="Frame rate" type="number" hint="How many frames will be consecutively displayed per second"
                              :constraint-option="{ handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: false }}"
                              @field-input="fpsHandler" 
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.loop_count" label="Run count" type="number" hint="How many times the GIF/APNG will run. Zero/blank to run forever"
                              :constraint-option="{handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true}}" 
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.start_frame" label="Start at frame" type="number" 
                              hint="Choose which frame to start the animation from. Default is 1 (is also 1 if left blank or typed 0)"
                              :constraint-option="{handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true}}" 
                  />
                </div>
                <div class="field-cell">
                  <CheckboxField v-model="criteria.flip_x" label="Flip X" hint="Flip the image horizontally" />
                  <br />
                  <CheckboxField v-model="criteria.flip_y" label="Flip Y" hint="Flip the image vertically" />
                </div>
                <div class="field-cell">
                  <CheckboxField v-model="criteria.preserve_alpha" label="Preserve Alpha" hint="(For GIFs) Preserve transparent pixels" />
                  <br />
                  <CheckboxField v-model="criteria.is_reversed" label="Reversed" hint="Reverse the animation" />
                </div>
                <div class="separator">
                  <div class="separator-space" />
                </div>
                <div class="field-cell span-4">
                  <ExtendedTextField v-model="saveDir" button-label="Save to" :use-icons="false" 
                                     @control-button-click="btnSetSavePath" 
                  />
                </div>
                <div class="field-cell">
                  <DropdownField v-model="criteria.format" :options-list="SUPPORTED_CREATE_EXTENSIONS" label="" :is-non-interactive="isButtonFrozen" />
                </div>
                <div class="field-cell">
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
                </div>
              </div>
             
<!--    
              <table class="" width="100%">
                <tr>
                  <td width="16.7%">
                  </td>
                  <td width="16.7%">
                  </td>
                  <td width="16.7%">
                  </td>
                  <td width="16.7%">
                  </td>
                  <td width="16.7%">
                  </td>
                  <td width="16.7%" style="vertical-align: bottom" />
                </tr>
                <tr>
                  <td>
                    <InputField v-model="criteria.delay" label="Delay (seconds)" type="number" hint="The time needed to move to the next frame"
                                :constraint-option="{ handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: false }}"
                                @field-input="delayHandler" 
                    />
                  </td>
                  <td>
                    <InputField v-model="criteria.fps" label="Frame rate" type="number" hint="How many frames will be consecutively displayed per second"
                                :constraint-option="{ handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: false }}"
                                @field-input="fpsHandler" 
                    />
                  </td>
                  <td>
                    <InputField v-model="criteria.loop_count" label="Run count" type="number" hint="How many times the GIF/APNG will run. Zero/blank to run forever"
                                :constraint-option="{handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true}}" 
                    />
                  </td>
                  <td>
                    <InputField v-model="criteria.start_frame" label="Start at frame" type="number" 
                                hint="Choose which frame to start the animation from. Default is 1 (is also 1 if left blank or typed 0)"
                                :constraint-option="{handlerName: 'numConstraint', options: {enforceUnsigned: true, enforceWhole: true}}" 
                    />
                  </td>
                  <td style="vertical-align: bottom">
                    <CheckboxField v-model="criteria.flip_x" label="Flip X" hint="Flip the image horizontally" />
                    <br />
                    <CheckboxField v-model="criteria.flip_y" label="Flip Y" hint="Flip the image vertically" />
                  </td>
                  <td style="vertical-align: bottom">
                    <CheckboxField v-model="criteria.preserve_alpha" label="Preserve Alpha" hint="(For GIFs) Preserve transparent pixels" />
                    <br />
                    <CheckboxField v-model="criteria.is_reversed" label="Reversed" hint="Reverse the animation" />
                  </td>
                </tr>
                <tr>
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
                          v-model="saveDir"
                          class="input is-neon-white"
                          type="text"
                          placeholder="Output folder"
                        />
                      </div>
                    </div>
                  </td>
                  <td colspan="1" style="padding-top: 15px">
                    <DropdownField v-model="criteria.format" :options-list="SUPPORTED_CREATE_EXTENSIONS" label="" :is-non-interactive="isButtonFrozen" />
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
              </table> -->
            </div>
            <div v-show="crtSubMenuSelection == 1 && criteria.format == 'gif'">
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
            <div v-show="crtSubMenuSelection == 1 && criteria.format == 'png'">
              <table
                class="mod-new-control-table is-hpaddingless medium-size-label"
                width="100%"
              >
                <APNGOptimizationRow
                  v-model:apng_is_optimized="apng_opt_criteria.apng_is_optimized"
                  v-model:apng_optimization_level="apng_opt_criteria.apng_optimization_level"
                  v-model:apng_is_reduced_color="apng_opt_criteria.apng_is_reduced_color"
                  v-model:apng_color_count="apng_opt_criteria.apng_color_count"
                  v-model:apng_quantization_enabled="apng_opt_criteria.apng_quantization_enabled"
                  v-model:apng_quantization_quality_min="apng_opt_criteria.apng_quantization_quality_min"
                  v-model:apng_quantization_quality_max="apng_opt_criteria.apng_quantization_quality_max"
                  v-model:apng_quantization_speed="apng_opt_criteria.apng_quantization_speed"
                  v-model:apng_convert_color_mode="apng_opt_criteria.apng_convert_color_mode"
                  v-model:apng_new_color_mode="apng_opt_criteria.apng_new_color_mode"
                  v-model:apng_is_unoptimized="apng_opt_criteria.apng_is_unoptimized"
                />
                <!-- <APNGUnoptimizationRow
                        :apng_is_optimized.sync="apng_is_optimized"
                        :apng_is_reduced_color.sync="apng_is_reduced_color"
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
import { access, accessSync, constants as fsConstants, existsSync } from "fs";
import { copyFile }  from 'fs/promises';
const SUPPORTED_CREATE_EXTENSIONS = [
  {
    name: "gif",
    label: "GIF",
    description: "", 
  },
  {
    name: "png",
    label: "APNG",
    description: "", 
  }
]
const RESIZE_METHODS = [
  {
    name: "BICUBIC",
    label: "Bicubic",
    description: "General-use resizing algorithm for most images"
  },
  {
    name: "NEAREST",
    label: "Nearest",
    description: "Preserve sharp edges. Ideal for pixel art"
  },
  {
    name: "BILINEAR",
    label: "Bilinear",
    description: "Similar to Bicubic, but not as smooth"
  },
  {
    name: "BOX",
    label: "Box",
    description: ""
  },
  {
    name: "HAMMING",
    label: "Hamming",
    description: ""
  },
  {
    name: "LANCZOS",
    label: "Lanczos",
    description: ""
  },
];

import { tridentEngine } from "../modules/streams/trident_engine";
import { numConstrain } from "../modules/events/constraints";
import { escapeLocalPath, stem, validateFilename } from "../modules/utility/pathutils";
import { formatBytes, randString } from "../modules/utility/stringutils";
import { gcd } from "../modules/utility/calculations";
import { GIF_DELAY_DECIMAL_PRECISION, APNG_DELAY_DECIMAL_PRECISION } from "../modules/constants/images";
import { PREVIEWS_PATH } from "../common/paths";

import { ConstraintOption } from "../models/componentProps.js";

import GIFOptimizationRow from "./components/GIFOptimizationRow.vue";
// import GIFUnoptimizationRow from "./components/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./components/APNGOptimizationRow.vue";
// import APNGUnoptimizationRow from "./components/APNGUnoptimizationRow.vue";

import { CreationCriteria, GIFOptimizationCriteria, APNGOptimizationCriteria } from "../models/criterion";

import { createPopper } from '@popperjs/core';
import vClickOutside from 'click-outside-vue3'

import StatusBar from "./components/StatusBar.vue";
import InputField from "./components/Form/InputField.vue";
import CheckboxField from './components/Form/CheckboxField.vue';
import DropdownField from './components/Form/DropdownField.vue';
import ExtendedTextField from './components/Form/ExtendedTextField.vue';

import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";

import { PreviewImageSaveNameBehaviour, PreviewImageSummary } from "../models/previewImage";

let extension_filters = [{ name: "Images", extensions: SUPPORTED_CREATE_EXTENSIONS.map(ext => ext.name) }];
let img_dialog_props = ["openfile"];
let imgs_dialog_props = ["openfile", "multiSelections", "createDirectory"];
let dir_dialog_props = ["openDirectory", "createDirectory"];


export default {
  components: {
    GIFOptimizationRow,
    // GIFUnoptimizationRow,
    APNGOptimizationRow,
    // APNGUnoptimizationRow,
    StatusBar,
    InputField,
    CheckboxField,
    DropdownField,
    ExtendedTextField,
  },
  directives:{
    clickOutside: vClickOutside.directive,
  },
  data() {
    return {
      criteria: new CreationCriteria(),
      gif_opt_criteria: new GIFOptimizationCriteria(),
      apng_opt_criteria: new APNGOptimizationCriteria(),
      fname: "",
      SUPPORTED_CREATE_EXTENSIONS: SUPPORTED_CREATE_EXTENSIONS,
      RESIZE_METHODS: RESIZE_METHODS,
      crtSubMenuSelection: 0,
      imagePaths: [],
      imageSequenceInfo: [],
      latestLoadCount: 0,
      // save_fstem: "",
      saveDir: "",
      insertIndex: "",
      totalSize: "",
      // orig_width: "",
      // old_width: "",
      // orig_height: "",
      // old_height: "",
      previewPath: "",
      previewPathCB: "",
      previewInfo: "",
      aspectRatio: "",
      lockAspectRatio: false,
      
      checkerBGIsActive: false,
      CRT_INSERT_LOAD: false,
      CRT_SMARTINSERT_LOAD: false,
      CRT_REPLACE_LOAD: false,
      CRT_IS_LOADING: false,
      CRT_IS_PREVIEWING: false,
      CRT_IS_CREATING: false,

      popperIsVisible: false,
      statusBarId: "createPanelStatusBar",
      ConstraintOption: ConstraintOption,
    };
  },
  computed: {
    isButtonFrozen() {
      if (this.CRT_IS_LOADING || this.CRT_IS_PREVIEWING || this.CRT_IS_CREATING) return true;
      else return false;
    },
    sequenceCounter() {
      if (this.imageSequenceInfo.length > 0) {
        return `${this.imageSequenceInfo.length} images`;
      } else return "";
    },
    computeTotalSequenceSize() {
      console.log("computeTotalSequenceSize");
      console.log(this.imageSequenceInfo.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0));
      return formatBytes(this.imageSequenceInfo.reduce((accumulator, currval) => accumulator + currval.fsize.value, 0), 3);
    },
    computePreviewImageSummary() {
      if (this.previewInfo) {
        let summary = new PreviewImageSummary(
          this.previewInfo.general_info.width.value,
          this.previewInfo.general_info.height.value,
          this.previewInfo.general_info.fsize_hr.value,
          this.previewInfo.animation_info != null,
          this.previewInfo.animation_info? this.previewInfo.animation_info.frame_count.value : 1,
          this.previewInfo.animation_info? this.previewInfo.animation_info.fps.value : null,
          this.previewInfo.animation_info? this.previewInfo.animation_info.loop_duration.value : null,
          this.previewInfo.animation_info? (this.previewInfo.animation_info.loop_count.value || 'Infinite') : null,
          this.previewInfo.general_info.format.value
        );
        return summary.toSummaryText();
      }
      else {
        return '';
      }
    }
  },
  watch: {
    // 'criteria.width': {
    //   handler(newValue, oldValue) {
    //     console.log(`width new ${newValue} old ${oldValue}`);
    //     this.criteria.height = oldValue;

        
    //     this.old_width = parseInt(oldValue);
    //     let newWidth = newValue;
    //     this.criteria.width = parseInt(newWidth);
    //     if (this.lockAspectRatio && this.aspectRatio.h_ratio > 0) {
    //       // Change height if lockAspectRatio is true and height is not 0
    //       let raHeight = Math.round(
    //         (newWidth / this.aspectRatio.w_ratio) * this.aspectRatio.h_ratio
    //       );
    //       this.criteria.height = raHeight > 0 ? parseInt(raHeight) : "";
    //     } else {
    //       this._updateAspectRatio(this.criteria.width, this.criteria.height);
    //     }
    //   },
    // },
    // 'criteria.height': {
    //   handler(newValue, oldValue) {
    //     this.old_height = parseInt(oldValue);
    //     let newHeight = newValue;
    //     this.criteria.height = parseInt(newHeight);
    //     if (this.lockAspectRatio && this.aspectRatio.w_ratio > 0) {
    //       let raWidth = Math.round(
    //         (newHeight / this.aspectRatio.h_ratio) * this.aspectRatio.w_ratio
    //       );
    //       console.log(raWidth);
    //       this.criteria.width = raWidth > 0 ? parseInt(raWidth) : "";
    //     } else {
    //       this._updateAspectRatio(this.criteria.width, this.criteria.height);
    //     }
    //   }
    // }
  },
  created() {
    window.addEventListener("resize", this.closeLoadPopper);
  },
  beforeMount: function () {
    const SETTINGS = ipcRenderer.sendSync("IPC-GET-SETTINGS");
    try {
      const defaultOutDir = SETTINGS.directories.default_out_dir.create_panel;
      if (defaultOutDir) {
        this.saveDir = defaultOutDir
      }
    } catch (error) {
      console.error(error);
    }
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
      console.log("obtained extension_filters", extension_filters);
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

        tridentEngine(cmd_args, (err, res) => {
          if (err) {
            if (err.error) {
              this._logError(err.error);
              this.toggleLoadButtonAnim(ops, false);
              this.CRT_IS_LOADING = false;
            }
            else if (err.warning) {
              this._logWarning(err.warning);
            }
          } else if (res) {
            if (res && res.msg) {
              this._logProcessing(res.msg);
            } else if (res && res.data) {
              let info = res.data;
              console.log("sequence info");
              console.log(info.sequence_info);
              console.log(info);
              this._renderSequence(info, { operation: ops });
              this.totalSize = `Total size: ${info.totalSize}`;
              // data.save_fstem = stem(data.save_fstem || info.name);
              this.fname = this.fname || info.name
              this.criteria.width = this.criteria.width || info.width;
              this.criteria.height = this.criteria.height || info.height;
              this.criteria.fps = this.criteria.fps || 50;
              this.criteria.delay = this.criteria.delay || 0.02;
              this.orig_width = info.width;
              this.orig_height = info.height;
              this.latestLoadCount = info.total;
              this._logSuccess(`Loaded ${this.latestLoadCount} images`);
              this._updateAspectRatio(this.criteria.width, this.criteria.height);
              this.CRT_IS_LOADING = false;
              this.toggleLoadButtonAnim(ops, false);
              console.log(`Set aspect ratio to true`);
              this.lockAspectRatio = true;
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
        if (this.insertIndex) {
          this.imagePaths.splice(this.insertIndex, 0, ...pyinfo.sequence);
          this.imageSequenceInfo.splice(this.insertIndex, 0, ...pyinfo.sequence_info);
        } else {
          this.imagePaths.push(...pyinfo.sequence);
          this.imageSequenceInfo.push(...pyinfo.sequence_info);
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
      if (this.imageSequenceInfo.length < 2) {
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
      tridentEngine(["combine_image", this.imagePaths, preview_savepath, criteria_pack], (err, res) => {
        if (err) {
          if (err.error) {
            this._logError(err.error);
            this.CRT_IS_PREVIEWING = false;
          }
          else if (err.warning) {
            this._logWarning(err.warning);
          }
        } else if (res) {
          if (res.msg) {
            this._logProcessing(res.msg);
          }
          if (res.preview_path) {
            this.previewPath = res.preview_path;
            this._previewPathCacheBreaker();
          }
        }},
        () => tridentEngine(["inspect_one", this.previewPath], (err, info) => {
          if (err) {
            if (err.error) {
              this._logError(err.error);
              this.CRT_IS_PREVIEWING = false;
            }
            else if (err.warning) {
              this._logWarning(err.warning);
            }
          } else if (info) {
            let inspectionData = info.data;
            console.log("preview inspect");
            console.log(inspectionData);
            this.previewInfo = inspectionData;
            this._logSuccess("Previewed!");
            this.CRT_IS_PREVIEWING = false;
          }
        })
      );
    },
    _previewPathCacheBreaker() {
      let cb_url = `${this.previewPath}`;
      console.log("Cache breaker url", cb_url);
      this.previewPathCB = cb_url;
    },
    removeFrame(index) {
      this.imagePaths.splice(index, 1);
      this.imageSequenceInfo.splice(index, 1);
    },
    btnClearAll() {
      this.clearSequence();
      this.clearPreviewAIMG();
      this.clearAuxInfo();
      this.clearFields();
      this.lockAspectRatio = false;
    },
    clearSequence() {
      this.imagePaths = [];
      this.imageSequenceInfo = [];
      // this.save_fstem = "";
    },
    clearPreviewAIMG() {
      this.previewPath = "";
      this.previewPathCB = "";
      this.previewInfo = "";
    },
    clearAuxInfo() {
      this.totalSize = "";
      // this.orig_width = "";
      // this.old_width = "";
      // this.orig_height = "";
      // this.old_height = "";
      this._logClear();
      let emptyAspectRatio = {
        w_ratio: "",
        h_ratio: "",
        text: "",
      };
      this.aspectRatio = emptyAspectRatio;
    },
    clearFields() {
      this.fname = "";
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
    btnPreviewSaveAIMG() {
      (async () => {
        let skipManualExistingFileCheck = false;

        if (!this.previewPath) {
          this._logError("No image in the preview to be saved!");
          return Promise.reject("No image in the preview to be saved!");
        }

        const SETTINGS = ipcRenderer.sendSync("IPC-GET-SETTINGS");
        let behaviourName = SETTINGS.preview_image.name_save_behaviour;
        const nameSaveBehaviour = PreviewImageSaveNameBehaviour.fromName(behaviourName);
        // console.error(`name save behaviour`);
        // console.error(nameSaveBehaviour);
        // console.error(nameSaveBehaviour.name == PreviewImageSaveNameBehaviour.AutoGenerated.name);

        if (!nameSaveBehaviour) {
          throw new Error(`Unknown preview name save behaviour: ${behaviourName}`);
        }

        let saveAbsolutePath = "";
        let previewFormat = this.previewPath.split('.').pop().toLowerCase();

        if (nameSaveBehaviour.name == PreviewImageSaveNameBehaviour.OpenWindowDialog.name) {
          let fName = `${this.fname}.${previewFormat}`;
          const result = await ipcRenderer.invoke('IPC-SHOW-SAVE-DIALOG', { 
            defaultPath: fName, 
            filters: [{ name: SUPPORTED_CREATE_EXTENSIONS.find(ext => ext.name == previewFormat).label, extensions: [previewFormat]}],
            properties: ["createDirectory"]});
          if (result.canceled)
            return Promise.reject("Image saving cancelled");
          else {
            let finalPath = result.filePath;
            console.log(finalPath);
            saveAbsolutePath = finalPath;
            skipManualExistingFileCheck = true;
          }
        }
        else {
          let targetDir = this.saveDir;
          if (!targetDir) {
            let dialogOptions = { properties: dir_dialog_props };
            const result = await ipcRenderer.invoke('open-dialog', dialogOptions);
            if (result.canceled)
              return Promise.reject("Directory selection cancelled");
            else{
              let out_dirs = result.filePaths;
              console.log(out_dirs);
              if (out_dirs && out_dirs.length > 0) { 
                targetDir = out_dirs[0];
              }
              else {
                return Promise.reject("No directories are selected")
              }
            }
          }
          let saveName = "";
          if (nameSaveBehaviour.name == PreviewImageSaveNameBehaviour.AutoGenerated.name)
            saveName = `create_preview_${Date.now()}_${randString(7)}.${previewFormat}`;
          else if (nameSaveBehaviour.name == PreviewImageSaveNameBehaviour.FromNameField.name)
            saveName = `${this.fname}.${previewFormat}`;
          // let targetName = basename(this.previewPath);
          saveAbsolutePath = join(targetDir, saveName);
        }

        console.debug(saveAbsolutePath);
        let proceed = true;
        if (!skipManualExistingFileCheck)
          proceed = await this._checkFileOverwriteAsync(saveAbsolutePath);
        console.log(`proceed? ${proceed}`)
        if (proceed){
          await copyFile(this.previewPath, saveAbsolutePath);
          this._logSuccess(`Saved preview image to ${saveAbsolutePath}`);
        }
        else {
        }
      })().catch((error) => {
        console.error(error);
      });
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
        this.saveDir = out_dirs[0];
        dirPath = this.saveDir;
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
      if (this.imageSequenceInfo.length < 2) {
        this._logError("Please load at least 2 messages!");
        // this.create_msgbox = "Please load at least 2 images!";
        return;
      }
      this.validateFilenameAsync().then(async (isValid) => {
        if (isValid) {
          if (!this.saveDir) {
            const result = await this.setSaveDirFromDialogAsync()
            if (result.canceled)
              return Promise.reject("Directory selection cancelled");
            else
              return this._checkFileOverwriteAsync(this._getSavePath());
          }
          else 
            return this._checkFileOverwriteAsync(this._getSavePath());
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

      // if (this.saveDir) {
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
    async _checkFileOverwriteAsync(fullPath) {
      let proceed = true;
      if (existsSync(fullPath)) {
        let options = {
          title: "TridentFrame",
          buttons: ["Yes", "No"],
          message:
            `A file with the same name (${this.fname}.${this.criteria.format}) already exists in the output folder and it will get overwritten. Do you want to proceed?`,
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
      tridentEngine(["combine_image", this.imagePaths, this._getSavePath(), criteria_pack], (err, res) => {
        if (err) {
          if (err.error) {
            this._logError(err.error);
            this.CRT_IS_CREATING = false;
          }
          else if (err.warning) {
            this._logWarning(err.warning);
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
      this.checkerBGIsActive = !this.checkerBGIsActive;
      console.log("now checkerbg is", this.checkerBGIsActive);
    },
    _getFullFilename() {
      return `${this.fname}.${this.criteria.format}`;
    },
    _getSavePath() {
      let file_name = this._getFullFilename();
      let save_path = join(this.saveDir, file_name);
      console.log(`getSavePath ${save_path}`);
      return save_path;
    },
    numConstrain: numConstrain,
    widthHandler(event) {
      console.log(event.target.value);
      let newWidth = event.target.value;
      this.criteria.width = parseInt(newWidth);
      if (this.lockAspectRatio && this.aspectRatio.h_ratio > 0) {
        // Change height if lockAspectRatio is true and height is not 0
        let raHeight = Math.round(
          (newWidth / this.aspectRatio.w_ratio) * this.aspectRatio.h_ratio
        );
        this.criteria.height = raHeight > 0 ? parseInt(raHeight) : "";
      } else {
        this._updateAspectRatio(this.criteria.width, this.criteria.height);
      }
    },
    heightHandler(event) {
      // this.old_height = parseInt(height);
      let newHeight = event.target.value;
      this.criteria.height = parseInt(newHeight);
      if (this.lockAspectRatio && this.aspectRatio.w_ratio > 0) {
        let raWidth = Math.round(
          (newHeight / this.aspectRatio.h_ratio) * this.aspectRatio.w_ratio
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
        this.aspectRatio = ARData;
      }
    },
    delayHandler(event) {
      console.log("delay event", event);
      let value = event.target.value;
      console.log("delay", value);
      if (value && value.includes(".")) {
        let numdec = value.split(".");
        console.log("numdec", numdec);
        let precision = GIF_DELAY_DECIMAL_PRECISION;
        if (this.criteria.format.toUpperCase() == "GIF") {
          precision = GIF_DELAY_DECIMAL_PRECISION;
        } else if (this.criteria.format.toUpperCase() == "PNG") {
          precision = APNG_DELAY_DECIMAL_PRECISION;
        }
        if (numdec[1].length > precision) {
          let decs = numdec[1].substring(0, precision);
          console.log("decs limit triggered", decs);
          value = `${numdec[0]}.${decs}`;
          this.criteria.delay = value;
        }
      }
      this.criteria.fps = Math.round(1000 / value) / 1000;
    },
    fpsHandler(event) {
      console.log("fps event", event);
      let value = event.target.value;
      console.log("fps", value);
      if (value) {
        let mult = 100;
        if (this.criteria.format.toUpperCase() == "GIF") {
          mult = 100;
        } else if (this.criteria.format.toUpperCase() == "PNG") {
          mult = 1000;
        }
        console.log("this.criteria.delay before", this.criteria.delay);
        this.criteria.delay = Math.round(mult / value) / mult;
        console.log("this.criteria.delay after", this.criteria.delay);
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
