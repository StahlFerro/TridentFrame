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
                  <span v-if="orig_attribute">{{ origAttributesTable.dimensions }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.dimensions') }}
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ previewAttributesTable.dimensions }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origAttributesTable.fileSize }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.fsize_hr') }}
                  <template v-if="preview_attribute">
                    <br />
                    {{ previewSizePercentage }}
                  </template>
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ previewAttributesTable.fileSize }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origAttributesTable.format }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.format') }}
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ previewAttributesTable.format }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origAttributesTable.frameCount }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.frame_count') }}
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_info">{{ previewAttributesTable.frameCount }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origAttributesTable.fps }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.fps') }}
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_info">{{ previewAttributesTable.fps }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origAttributesTable.averageDelay }}</span>
                  <!-- <span v-else>-</span> -->
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.average_delay') }}
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ previewAttributesTable.averageDelay }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  <span v-if="orig_attribute">{{ origAttributesTable.loopDuration }}</span>
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.loop_duration') }}
                </td>
                <td class="mod-info-data">
                  <span v-if="preview_attribute">{{ previewAttributesTable.loopDuration }}</span>
                </td>
              </tr>
              <tr>
                <td class="mod-info-data">
                  {{ origAttributesTable.loopCount }}
                </td>
                <td class="mod-info-label is-cyan">
                  {{ $t('image_metadata.loop_count') }}
                </td>
                <td class="mod-info-data">
                  {{ previewAttributesTable.loopCount }}
                  <!-- <span v-if="preview_attribute.loop_count == 0">Infinite</span>
                  <span v-else>{{ preview_attribute.loop_count }}</span> -->
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
          <img :src="escapeLocalPath(previewPathCB)" />
        </div>
      </div>
      <div class="modify-panel-middlebar">
        <div class="mpb-load-buttons">
          <a class="button is-neon-emerald" :class="{'is-loading': MOD_IS_LOADING, 'non-interactive': isButtonFrozen}" @click="loadImage">
            <span class="icon is-small">
              <font-awesome-icon icon="plus" />
            </span>
            <span>Load Image</span>
          </a>
          <a class="button is-neon-crimson" :class="{'non-interactive': isButtonFrozen}" @click="clearImage">
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
        <div class="mpb-center-buttons">
          <p class="is-white-d">
            <!-- {{ hasModification }} -->
          </p>
        </div>
        <div class="mpb-preview-buttons">
          <a class="button is-neon-cyan" :class="{'is-loading': MOD_IS_PREVIEWING, 'non-interactive': isButtonFrozen}" @click="btnPreviewModImg">
            <span class="icon is-small">
              <font-awesome-icon :icon="['far', 'eye']" />
            </span>
            <span>Preview</span>
          </a>
          <a class="button is-neon-cyan" :class="{'non-interactive': isButtonFrozen}" @click="btnPreviewSaveAIMG">
            <span class="icon is-medium">
              <font-awesome-icon icon="save" />
            </span>
          </a>
          <a class="button is-neon-crimson" :class="{'non-interactive': isButtonFrozen}" @click="clearPreviewImage">
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
                :class="{'is-selected': modSubMenuSelection == 0}"
              >
                <a id="MOD_menu_general" @click="modSubMenuSelection = 0">
                  <span class="icon is-large">
                    <font-awesome-icon :icon="['far', 'image']" size="2x" inverse />
                    <!-- <i class="fas fa-image fa-2x fa-inverse"></i> -->
                  </span>
                  <p class="is-white-d">General</p>
                </a>
              </li>
              <li
                id="MOD_box_gif" class="subtab-menu-item is-cyan"
                :class="{'is-selected': modSubMenuSelection == 1}"
              >
                <a id="MOD_menu_gif" @click="modSubMenuSelection = 1">
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
        <div class="mpc-right-panel">
          <div class="mpc-right-top-panel">
            <div v-show="modSubMenuSelection == 0">
              <div class="general-form row-7">
                <div class="field-cell span-2">
                  <InputField v-model="fname" label="Name" type="text" hint="The name of the GIF/APNG" />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.width" label="Width" type="number" hint="The width of the animated image"
                              :constraint-option="ENFORCE_UNSIGNED_WHOLE" :min-number="0"
                              @input="widthHandler"
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.height" label="Height" type="number" hint="The height of the animated image"
                              :constraint-option="ENFORCE_UNSIGNED_WHOLE" :min-number="0"
                              @input="heightHandler"
                  />
                </div>
                <div class="field-cell">
                  <DropdownField v-model="criteria.resize_method" :options-list="RESIZE_METHODS" label="Resize method" :is-fullwidth="true" />
                </div>
                <div class="field-cell">
                  <CheckboxField v-model="criteria.flip_x" label="Flip X" hint="Flip the image horizontally" />
                  <br />
                  <CheckboxField v-model="criteria.flip_y" label="Flip Y" hint="Flip the image vertically" />
                </div>
                <div class="field-cell">
                  <CheckboxField v-model="lockAspectRatio" label="Lock aspect ratio" hint="Lock the width and height ratio" />
                  <br />
                  <template v-if="aspect_ratio && aspect_ratio.text">
                    <input v-model="aspect_ratio.text" class="input is-border-colorless is-paddingless" style="height: 1.5em;" readonly="readonly" />
                  </template>
                  <template v-else>
                    &nbsp;
                  </template>
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.delay" label="Delay (seconds)" type="number" hint="The time needed to move to the next frame"
                              :constraint-option="ENFORCE_UNSIGNED" :min-number="0"
                              @input="delayHandler" 
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.fps" label="Frame rate" type="number" hint="How many frames will be consecutively displayed per second"
                              :constraint-option="ENFORCE_UNSIGNED" :min-number="0"
                              @input="fpsHandler" 
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.loop_count" label="Run count" type="number" hint="How many times the GIF/APNG will run. Zero/blank to run forever"
                              :constraint-option="ENFORCE_UNSIGNED_WHOLE" :min-number="0"
                  />
                </div>
                <div class="field-cell">
                  <DropdownField v-model="criteria.delay_handling" :options-list="DELAY_HANDLING_OPTIONS" label="Delay handling" hint="How to modify the delay"
                                 :is-fullwidth="true" 
                  />
                </div>
                <div class="field-cell">
                  <InputField v-model="criteria.skip_frame" :label="$t('criterion.skip_frame')" type="number" 
                              hint="Amount of frames before the next frame is skipped. 0 or blank for no skipping"
                              :constraint-option="ENFORCE_UNSIGNED_WHOLE" :min-number="0"
                  />
                </div>
                <div class="field-cell">
                </div>
                <div class="field-cell">
                  <CheckboxField v-model="criteria.skip_frame_maintain_delay" :label="$t('criterion.skip_frame_maintain_delay')" 
                                 hint="(For GIFs) Preserve transparent pixels" 
                  />
                  <br />
                  <CheckboxField v-model="criteria.is_reversed" label="Reversed" hint="Reverse the animation" />
                </div>
                <div class="separator">
                  <div class="separator-space" />
                </div>
                <div class="field-cell span-4">
                  <ButtonInputField>
                    <template #buttonControl>
                      <ButtonField label="Save to" color="blue" :is-square="true" :icons="['fas', 'folder-open']"
                                   @click="btnSetSavePath"
                      />
                    </template>
                    <template #inputControl>
                      <InputField v-model="saveDir" type="text" />
                    </template>
                  </ButtonInputField>
                </div>
                <div class="field-cell">
                  <DropdownField v-model="criteria.format" :options-list="SUPPORTED_MODIFY_EXTENSIONS" label="" :is-non-interactive="isButtonFrozen" />
                </div>
                <div class="field-cell">
                  <ButtonField label="MODIFY" color="cyan"
                               :is-loading="MOD_IS_MODIFYING == true" :is-non-interactive="isButtonFrozen"
                               @click="btnModifyImage"
                  />
                </div>
              </div>
              <!--
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
                    <label class="checkbox">
                      <input v-model="lockAspectRatio" type="checkbox" />
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
                    <div class="field">
                      <label
                        class="label"
                        title="How to modify the delay"
                      >Delay Handling</label>
                      <div class="control">
                        <div class="select is-neon-cyan">
                          <select v-model="criteria.delay_handling">
                            <option
                              value="MULTIPLY_AVERAGE"
                              title="Multiply all frames based on the ratio between the current average and the value specified in the Delay field"
                            >
                              Multiply average
                            </option>
                            <option
                              value="EVEN_OUT"
                              title="Change all frame delay to the specified Delay field"
                            >
                              Even out
                            </option>
                            <option
                              value="DO_NOTHING"
                              title="Don't alter the current frames delays at all"
                            >
                              Do nothing
                            </option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td width="16.7%" />
                  <td width="16.7%" class="force-vcenter">
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
                  <td colspan="1">
                    <div class="field">
                      <div class="control">
                        <div class="select is-neon-cyan" :class="{'non-interactive': isButtonFrozen}">
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
                    <a class="button is-neon-cyan" :class="{'is-loading': MOD_IS_MODIFYING, 'non-interactive': isButtonFrozen}" @click="btnModifyImage">
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
              -->

            </div>
            <div v-show="modSubMenuSelection == 1 && criteria.format == 'gif'">
              <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
                <GIFOptimizationRow
                  v-model:hasOptimization="hasGIFOptimization"
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
            <div v-show="modSubMenuSelection == 1 && criteria.format == 'png'">
              <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%">
                <APNGOptimizationRow 
                  ref="apngOptimRow"
                  v-model:hasOptimizaton="hasAPNGOptimization"
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
                <APNGUnoptimizationRow
                  ref="apngUnoptimRow"
                  v-model:apng_is_optimized="apng_opt_criteria.apng_is_optimized"
                  v-model:apng_is_reduced_color="apng_opt_criteria.apng_is_reduced_color"
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
import { ConstraintOption } from '../models/componentProps';

import { dirname, join, basename } from "path";
import GIFOptimizationRow from "./components/GIFOptimizationRow.vue";
import GIFUnoptimizationRow from "./components/GIFUnoptimizationRow.vue";
import APNGOptimizationRow from "./components/APNGOptimizationRow.vue";
import APNGUnoptimizationRow from "./components/APNGUnoptimizationRow.vue";
import { existsSync } from 'fs';
import { copyFile }  from 'fs/promises';

import StatusBar from "./components/StatusBar.vue";
import InputField from "./components/Form/InputField.vue";
import CheckboxField from './components/Form/CheckboxField.vue';
import DropdownField from './components/Form/DropdownField.vue';
import ButtonField from './components/Form/ButtonField.vue';
import ButtonInputField from './components/Form/ButtonInputField.vue';

import { EnumStatusLogLevel } from "../modules/constants/loglevels";
import { logStatus } from "../modules/events/statusBarEmitter";

import { PreviewImageSaveNameBehaviour, PreviewImageSummary } from "../models/previewImage";
import { APNGOptimizationCriteria, GIFOptimizationCriteria, ModificationCriteria } from '../models/criterion';
// import Vue from 'vue';

const SUPPORTED_MODIFY_EXTENSIONS = [
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
];

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

const DELAY_HANDLING_OPTIONS = [
  {
    name: "MULTIPLY_AVERAGE",
    label: "Multiply average",
    description: "Multiply all frames based on the ratio between the current average and the value specified in the Delay field"
  },
  {
    name: "EVEN_OUT",
    label: "Even-out",
    description: "Change all frame delay to the specified Delay field"
  },
  {
    name: "DO_NOTHING",
    label: "Do nothing",
    description: "Don't alter the current frames delays at all"
  },
]
const ENFORCE_UNSIGNED = new ConstraintOption('numConstraint', {enforceUnsigned: true, enforceWhole: false });
const ENFORCE_UNSIGNED_WHOLE = new ConstraintOption('numConstraint', {enforceUnsigned: true, enforceWhole: true });
const ENFORCE_WHOLE = new ConstraintOption('numConstraint', {enforceUnsigned: false, enforceWhole: true });

let common_metadata = {
  fname: "",
  width: "",
  height: "",
  frame_count: "",
  frame_count_ds: "",
  fps: "",
  fps_info: "",
  delay: "",
  delay_info: "",
  loop_duration: "",
  loop_count: "",
  loop_count_info: "",
  file_size: "",
  file_size_hr: "",
  format: "",
  format_info: "",
  path: "",
  hash_sha1: "",
  last_modified_dt: "",
};

let extension_filters = [
    { name: 'Images', extensions: SUPPORTED_MODIFY_EXTENSIONS.map(ext => ext.name) },
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
    InputField,
    CheckboxField,
    DropdownField,
    ButtonField,
    ButtonInputField,
  },
  data() {
    return {
      orig_attribute: structuredClone(common_metadata),
      preview_attribute: structuredClone(common_metadata),
      criteria: new ModificationCriteria(),
      gif_opt_criteria: new GIFOptimizationCriteria(),
      hasGIFOptimization: false,
      apng_opt_criteria: new APNGOptimizationCriteria(),
      hasAPNGOptimization: false,
      fname: "",
      previewPath: "",
      previewPathCB: "",
      preview_info: "",
      // save_fstem: "",
      saveDir: "",
      preview_size: "",
      preview_size_hr: "",
      aspect_ratio: "",
      lockAspectRatio: false,
      modSubMenuSelection: 0,
      orig_checkerbg_active: false,
      new_checkerbg_active: false,
      MOD_IS_LOADING: false,
      MOD_IS_MODIFYING: false,
      MOD_IS_PREVIEWING: false,
      modify_msgbox: "",
      SUPPORTED_MODIFY_EXTENSIONS: SUPPORTED_MODIFY_EXTENSIONS,
      RESIZE_METHODS: RESIZE_METHODS,
      DELAY_HANDLING_OPTIONS: DELAY_HANDLING_OPTIONS,
      ENFORCE_UNSIGNED: ENFORCE_UNSIGNED,
      ENFORCE_UNSIGNED_WHOLE: ENFORCE_UNSIGNED_WHOLE,
      statusBarId: "modifyPanelStatusBar",
      // statusBarBus: new Vue(),
    };
  },
  computed: {
    origDimensionsText() {
      if (this.orig_attribute.width && this.orig_attribute.height) {
        return `${this.orig_attribute.width} x ${this.orig_attribute.height}`;
      }
      else {
        return "";
      }
    },
    previewDimensionsText() {
      if (this.preview_attribute.width && this.preview_attribute.height) {
        return `${this.preview_attribute.width} x ${this.preview_attribute.height}`;
      }
      else {
        return "";
      }
    },
    origAttributesTable() {
      let origAttributes = {
        dimensions: this.origDimensionsText,
        fileSize: this.orig_attribute.file_size_hr,
        format: this.orig_attribute.format.toUpperCase(),
        frameCount: this.orig_attribute.frame_count,
        fps: this.orig_attribute.fps? `${this.orig_attribute.fps} FPS` : '',
        averageDelay: this.orig_attribute.delay? `${roundPrecise(this.orig_attribute.delay, 3)} ms` : '',
        loopDuration: this.orig_attribute && this.orig_attribute.loop_duration? `${roundPrecise(this.orig_attribute.loop_duration, 3) } seconds` : '',
        loopCount: this.orig_attribute.loop_count && this.orig_attribute.loop_count == 0? "Infinite" : this.orig_attribute.loop_count,
      }
      console.table(origAttributes);
      return origAttributes;
    },
    previewAttributesTable() {
      let previewAttributes = {
        dimensions: this.previewDimensionsText,
        fileSize: this.preview_attribute.file_size_hr,
        format: this.preview_attribute.format.toUpperCase(),
        frameCount: this.preview_attribute.frame_count,
        fps: this.preview_attribute.fps? `${this.preview_attribute.fps} FPS` : '',
        averageDelay: this.preview_attribute.delay? `${roundPrecise(this.preview_attribute.delay, 3)} ms` : '',
        loopDuration: this.preview_attribute && this.preview_attribute.loop_duration? `${roundPrecise(this.preview_attribute.loop_duration, 3) } seconds` : '',
        loopCount: this.preview_attribute.loop_count && this.preview_attribute.loop_count == 0? "Infinite" : this.preview_attribute.loop_count,
      }
      console.table(previewAttributes);
      return previewAttributes;
    },
    isButtonFrozen() {
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
    hasGeneralModification() {
      // console.debug(`${this.orig_attribute.width != this.criteria.width}`);
      // console.debug(`${this.orig_attribute.width != this.criteria.height}`);
      // console.debug(`${this.orig_attribute.delay} ${this.criteria.delay} ${this.orig_attribute.delay != this.criteria.delay}`);
      // console.debug(`${this.orig_attribute.fps} ${this.criteria.fps} ${this.orig_attribute.fps != this.criteria.fps}`);
      // console.debug(`${this.orig_attribute.loop_count} ${this.criteria.loop_count} ${this.orig_attribute.loop_count != this.criteria.loop_count}`);
      // console.debug(`${this.orig_attribute.format} ${this.criteria.format} ${this.orig_attribute.format != this.criteria.format}`);
      if (this.orig_attribute.width != this.criteria.width || 
          this.orig_attribute.height != this.criteria.height || 
          this.orig_attribute.fps != this.criteria.fps || 
          this.orig_attribute.loop_count != this.criteria.loop_count || 
          this.orig_attribute.format != this.criteria.format ||
          this.criteria.flip_x || this.criteria.flip_y || this.criteria.is_reversed)
          return true;
      else return false;
    },
    hasFormatOptimization() {
      let hasOptim = false;
      let outFormat = this.criteria.format.toLowerCase();
      if (outFormat == 'gif') {
        let gifCriteria = this.gif_opt_criteria;
        hasOptim = gifCriteria.is_optimized || gifCriteria.is_lossy || gifCriteria.is_reduced_color || gifCriteria.is_dither_alpha;
      }
      else if (outFormat == 'png') {
        hasOptim = this.hasAPNGOptimization;
        let apngCriteria = this.apng_opt_criteria;
        hasOptim = apngCriteria.apng_is_optimized || apngCriteria.apng_is_reduced_color || apngCriteria.apng_quantization_enabled || apngCriteria.apng_is_unoptimized;
      }
      else {
        console.error(`Unknown format ${this.criteria.format.toLowerCase()}`);
      }
      /*
      switch (this.criteria.format.toLowerCase().valueOf()) {
        case 'gif':
          hasOptim = this.hasGIFOptimization;
          break;
        case 'png':
          hasOptim = this.hasAPNGOptimization;
        default:
          console.error(`Unknown format ${this.criteria.format.toLowerCase()}`)
          break;
      }
      */
      return hasOptim;
    },
    hasModification() {
      console.debug(`hasModification: ${this.hasGeneralModification} ${this.hasFormatOptimization}`)
      return this.orig_attribute.path !== "" && this.hasGeneralModification || this.hasFormatOptimization;
    },
  },
  beforeMount: function () {
    const SETTINGS = ipcRenderer.sendSync("IPC-GET-SETTINGS");
    try {
      const defaultOutDir = SETTINGS.directories.default_out_dir.modify_panel;
      if (defaultOutDir) {
        this.saveDir = defaultOutDir
      }
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    loadOrigMetadata(res) {
      let geninfo = res.general_info;
      let ainfo = res.animation_info;
      this.orig_attribute.name = geninfo.name.value;
      // this.save_fstem = stem(this.save_fstem || geninfo.name.value);
      this.orig_attribute.width = geninfo.width.value;
      this.orig_attribute.height = geninfo.height.value;
      this.orig_attribute.fps = ainfo.fps.value;
      this.orig_attribute.fps_info = `${ainfo.fps.value} FPS`;
      this.orig_attribute.frame_count= ainfo.frame_count.value;
      this.orig_attribute.format = geninfo.format.value.toLowerCase();
      this.orig_attribute.format_info = geninfo.format.value.toUpperCase();
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
      this.orig_attribute.loop_count = ainfo.loop_count.value;
      if (ainfo.loop_count.value == 0) {
        this.orig_attribute.loop_count_info = "Infinite"
      }
      else {
        this.orig_attribute.loop_count_info = ainfo.loop_count.value;
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
      this.preview_attribute.fps = ainfo.fps.value;
      this.preview_attribute.frame_count= ainfo.frame_count.value;
      this.preview_attribute.format = geninfo.format.value.toLowerCase();
      this.preview_attribute.format_info = geninfo.format.value.toUpperCase();
      let delay_info = `${roundPrecise(ainfo.average_delay.value, 3)} ms`;
      if (ainfo.delays_are_even.value) {
        delay_info += ` (even)`;
      }
      else {
        delay_info += ` (uneven)`;
      }
      this.preview_attribute.delay = ainfo.average_delay.value;
      this.preview_attribute.delay_info = delay_info;
      this.preview_attribute.loop_duration = ainfo.loop_duration.value;
      this.preview_attribute.loop_count = ainfo.loop_count.value;
      if (ainfo.loop_count.value == 0) {
        this.preview_attribute.loop_count_info = "Infinite"
      }
      else {
        this.preview_attribute.loop_count_info = ainfo.loop_count.value;
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
      this.fname = geninfo.sanitized_namestem.value;
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
        tridentEngine(["inspect_one", chosen_path[0], "animated"], (err, res) => {
          if (err) {
            if (err.error) {
              this._logError(err.error);
              this.MOD_IS_LOADING = false;
            }
            else if (err.warning) {
              this._logWarning(err.warning);
            }
            // mboxError(split_msgbox, error);
          } else if (res) {
            if (res && res.msg) {
              this._logProcessing(res.msg);
            } else if (res && res.data) {
              this.loadOrigMetadata(res.data);
              this.populateForm(res.data);
              this._logSuccess("Image loaded.");
            }
            this.MOD_IS_LOADING = false;
            this.lockAspectRatio = true;
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
      this.orig_attribute.fps_info = "";
      this.orig_attribute.delay = "";
      this.orig_attribute.delay_info = "";
      this.orig_attribute.loop_duration = "";
      this.orig_attribute.loop_count = "";
      this.orig_attribute.loop_count_info = "";
      this.orig_attribute.file_size = "";
      this.orig_attribute.file_size_hr = "";
      this.orig_attribute.format = "";
      this.orig_attribute.format_info = "";
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
      this.fname = "";
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
      this.lockAspectRatio = false;
    },
    clearPreviewImage() {
      this.previewPath = "";
      this.previewPathCB = "";
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
        this.saveDir = out_dirs[0];
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
        console.log(`proceed modify ${proceed}`);
        if (proceed)
          this.modifyImage();
        else
          return;
      }).catch((error) => {
        console.error(error);
      });


      
    // if (this.saveDir)
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
    // chooseOutDir: chooseOutDir,
    btnPreviewModImg() {
      this.previewModImg(); 
    },
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
      tridentEngine(["modify_image", this.orig_attribute.path, preview_savepath, criteria_pack], (err, res) => {
        if (err) {
          if (err.error) {
            this._logError(err.error);
            this.MOD_IS_PREVIEWING = false;
          }
          else if (err.warning) {
            this._logWarning(err.warning);
          }
        }
        else if (res) {
          if (res.msg) {
            this._logProcessing(res.msg);
          }
          if (res.preview_path) {
            this.previewPath = res.preview_path;
            this.previewPathCacheBreaker();
          }
        }
      },
      () => tridentEngine(["inspect_one", this.previewPath, "animated"], (err, res) => {
        if (err) {
          if (err.error) {
            this._logError(err.error);
          }
          else if (err.warning) {
            this._logWarning(err.warning);
          }
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
          console.log(fName);
          const result = await ipcRenderer.invoke('IPC-SHOW-SAVE-DIALOG', { 
            defaultPath: fName, 
            filters: [{ name: SUPPORTED_MODIFY_EXTENSIONS.find(ext => ext.name == previewFormat).label, extensions: [previewFormat]}],
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
            let options = { properties: dir_dialog_props };
            const result = await ipcRenderer.invoke('open-dialog', options);
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
            saveName = `modify_preview_${Date.now()}_${randString(7)}.${this.previewPath.split('.').pop().toLowerCase()}`;
          else if (nameSaveBehaviour.name == PreviewImageSaveNameBehaviour.FromNameField.name)
            saveName = `${this.fname}.${previewFormat}`;
          saveAbsolutePath = join(targetDir, saveName);
        }
        
        console.debug(`Skip existing check: ${skipManualExistingFileCheck}\nObtained saveAbsolutePath: ${saveAbsolutePath}`);
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
    previewPathCacheBreaker() {
      let cb_url = `${this.previewPath}`;
      console.log("Cache breaker url", cb_url);
      this.previewPathCB = cb_url;
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
        tridentEngine(["modify_image", this.orig_attribute.path, this._getSavePath(), criteria_pack], (err, res) => {
          if (err) {
            if (err.error) {
              console.error(err.error);
              this._logError(err.error);
              this.MOD_IS_MODIFYING = false;
            }
            else if (err.warning)
              this._logWarning(err.warning);
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
    widthHandler(event) {
      // data.orig_attribute.width = parseInt(width);
      console.log(event);
      let newWidth = event.target.value;
      this.criteria.width = newWidth;
      if (this.lockAspectRatio && this.aspect_ratio.h_ratio > 0) { // Change height if lockAspectRatio is true and height is not 0
        let raHeight = Math.round(newWidth / this.aspect_ratio.w_ratio * this.aspect_ratio.h_ratio);
        this.criteria.height = raHeight > 0? raHeight : "";
      }
      else {
        this.updateAspectRatio(this.criteria.width, this.criteria.height);
      }
    },
    heightHandler(event) {
      // data.orig_attribute.height = parseInt(height);
      let newHeight = event.target.value;
      this.criteria.height = newHeight;
      if (this.lockAspectRatio && this.aspect_ratio.w_ratio > 0) {
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
      let save_path = join(this.saveDir, file_name);
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
    floatConstrain: floatConstrain,
    numConstrain: numConstrain,
    roundPrecise: roundPrecise,
    escapeLocalPath: escapeLocalPath,
  }
};
</script>
