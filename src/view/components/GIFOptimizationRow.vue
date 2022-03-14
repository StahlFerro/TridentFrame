<template>
  <tr>
    <td class="force-vcenter" width="25%">
      <label class="checkbox" title="Optimize GIFs to reduce output filesize">
        <input
          v-model="is_optimized" :disabled="isUnoptimized"
          type="checkbox" @change="$emit('update:is_optimized', is_optimized)"
        />
        Optimize
      </label>
    </td>
    <td class="force-vcenter" width="25%">
      <div class="field">
        <!-- <label class="label">Optimization Level</label> -->
        <div class="control">
          <div class="select is-neon-cyan" :class="{'non-interactive': !is_optimized}">
            <select v-model="optimization_level" @change="$emit('update:optimization_level', optimization_level)">
              <option value="1" :class="{'is-selected': optimization_level == '1'}">
                Lv. 1: Store changed portion only
              </option>
              <option value="2" :class="{'is-selected': optimization_level == '2'}">
                Lv. 2: Also uses transparency
              </option>
              <option value="3" :class="{'is-selected': optimization_level == '3'}">
                Lv. 3: All optimization methods
              </option>
            </select>
          </div>
        </div>
      </div>
    </td>
    <td class="force-vcenter" width="25%" />
    <td class="force-vcenter" width="25%" />
  </tr>
  <tr>
    <td class="force-vcenter">
      <label
        class="checkbox"
        title="Performs significant file size reduction at the cost of quality (artifacts and noise)"
      >
        <input
          v-model="is_lossy" type="checkbox" :disabled="isUnoptimized"
          @change="$emit('update:is_lossy', is_lossy)"
        />
        Lossy-compression
      </label>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <!-- <label class="label">Color space</label> -->
        <div class="control">
          <input
            v-model="lossy_value"
            class="input is-neon-white"
            type="number"
            min="30"
            max="200"
            placeholder="30 - 200"
            :disabled="!is_lossy"
            @change="$emit('update:lossy_value', lossy_value)"
            @keydown="numConstrain($event, true, true)"
          />
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td class="force-vcenter">
      <label
        class="checkbox"
        title="Limits the number for all frames of the GIF. Ranging from 2 colors (monochrome) to 256 (maximum for GIFs). Warning: this will also eliminate local/per-frame color tables, setting just one global color table for every frame."
      >
        <input
          v-model="is_reduced_color" type="checkbox" :disabled="is_unoptimized"
          @change="$emit('update:is_reduced_color', is_reduced_color)"
        />
        Color space
      </label>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <!-- <label class="label">Color space</label> -->
        <div class="control">
          <input
            v-model="color_space"
            :disabled="!is_reduced_color"
            class="input is-neon-white"
            type="number"
            min="2"
            max="256"
            placeholder="2 - 256"
            @change="$emit('update:color_space', color_space)"
            @keydown="numConstrain($event, true, true)"
          />
        </div>
      </div>
    </td>
  </tr>
  <tr>
    <td class="force-vcenter">
      <label
        class="checkbox"
        title="Perform dithering on translucent source pixels to either fully transparent or opaque depending on the chosen method"
      >
        <input
          v-model="is_dither_alpha" type="checkbox" :disabled="is_unoptimized"
          @change="$emit('update:is_dither_alpha', is_dither_alpha)"
        />
        Transparency Dither
      </label>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <!-- <label class="label">Color space</label> -->
        <div class="control">
          <div class="select is-neon-cyan" :class="{'non-interactive': !is_dither_alpha}">
            <select v-model="dither_alpha_method" @change="$emit('update:dither_alpha_method', dither_alpha_method)">
              <option value="SCREENDOOR" title="Screen door pattern">
                Screendoor
              </option>
            </select>
          </div>
        </div>
      </div>
    </td>
    <td class="force-vcenter">
      <label class="label" title="The width of the GIF/APNG">Threshold value</label>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <div class="control">
          <vue-slider
            v-model="dither_alpha_threshold" :class="[!is_dither_alpha? ['non-interactive', 'vue-slider-disabled']: '']"
            @change="$emit('update:dither_alpha_threshold', dither_alpha_threshold)"
          />
          <!-- <input id="ditherAlphaThresholdSlider" name="ditherAlphaThresholdSlider" class="has-output is-fullwidth" 
                min="0" max="100" v-model="dither_alpha_threshold" step="1" type="range"/>
              <output for="ditherAlphaThresholdSlider" @forminput="value = ditherAlphaThresholdSlider.valueAsNumber;">
                {{ dither_alpha_threshold }}</output> -->
        </div>
      </div>
    </td>
  </tr>
</template>

<script>
// import Vue from 'vue';
// import { Plugin } from 'vue'
// import { Fragment }  from 'vue-fragment';
import { numConstrain } from "../../modules/events/constraints";
// const bulmaSlider = require("../../node_modules/bulma-slider/dist/js/bulma-slider");
// bulmaSlider.attach();

export default {
  name: "GIFOptimizationRow",
  // components: { Fragment },
  props: {
    isUnoptimized: Boolean
  },
  emits: ['update:optimization_level', 'update:is_optimized', 'update:is_lossy', 'update:lossy_value', 'update:is_reduced_color', 'update:color_space', 
  'update:is_dither_alpha', 'update:dither_alpha_method', 'update:dither_alpha_threshold',],
  data: function() {
    return {
      preserve_alpha: false,
      is_optimized: false,
      optimization_level: "1",
      is_lossy: false,
      lossy_value: "",
      is_reduced_color: false,
      color_space: "",
      is_dither_alpha: false,
      dither_alpha_method: "SCREENDOOR",
      dither_alpha_threshold: 50,
    };
  },
  methods: {
    numConstrain: numConstrain,
  }
};
</script>
