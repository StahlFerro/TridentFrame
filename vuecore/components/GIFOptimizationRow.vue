<template>
  <!-- <table class="table mod-new-control-table is-hpaddingless medium-size-label" width="100%"> -->
    <Fragment>
      <tr>
        <td class="force-vcenter" width="25%">
          <label class="checkbox" title="Optimize GIFs to reduce output filesize">
            <input v-model="is_optimized" v-bind:disabled="is_unoptimized"
            @change="$emit('update:is_optimized', is_optimized)" type="checkbox" />
            Optimize
          </label>
        </td>
        <td class="force-vcenter" width="25%">
          <div class="field">
            <!-- <label class="label">Optimization Level</label> -->
            <div class="control">
              <div class="select is-neon-cyan" v-bind:class="{'non-interactive': !is_optimized}">
                <select v-model="optimization_level" @change="$emit('update:optimization_level', optimization_level)">
                  <option value="1">Lv. 1: Store changed portion only</option>
                  <option value="2">Lv. 2: Also uses transparency</option>
                  <option value="3">Lv. 3: All optimization methods</option>
                </select>
              </div>
            </div>
          </div>
        </td>
        <td class="force-vcenter" width="25%"></td>
        <td class="force-vcenter" width="25%"></td>
      </tr>
      <tr>
        <td class="force-vcenter">
          <label
            class="checkbox"
            title="Performs significant file size reduction at the cost of quality (artifacts and noise)"
          >
            <input v-model="is_lossy" type="checkbox" v-bind:disabled="is_unoptimized"
              @change="$emit('update:is_lossy', is_lossy)" />
            Lossy-compression
          </label>
        </td>
        <td class="force-vcenter">
          <div class="field">
            <!-- <label class="label">Color space</label> -->
            <div class="control">
              <input
                v-model="lossy_value"
                @change="$emit('update:lossy_value', lossy_value)"
                class="input is-neon-white"
                type="number"
                min="30"
                max="200"
                placeholder="30 - 200"
                v-bind:disabled="!is_lossy"
                v-on:keydown="numConstrain($event, true, true)"
              />
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td class="force-vcenter">
          <label
            class="checkbox"
            title="Limits the number for all frames of the GIF. Ranging from 2 colors (monochrome) to 256 (maximum for GIFs). Warning: this will also eliminate local/per-frame color tables, setting just one global color table for every frame.">
            <input type="checkbox" v-model="is_reduced_color" v-bind:disabled="is_unoptimized"
              @change="$emit('update:is_reduced_color', is_reduced_color)" />
            Color space
          </label>
        </td>
        <td class="force-vcenter">
          <div class="field">
            <!-- <label class="label">Color space</label> -->
            <div class="control">
              <input
                v-model="color_space"
                @change="$emit('update:color_space', color_space)"
                v-bind:disabled="!is_reduced_color"
                class="input is-neon-white"
                type="number"
                min="2"
                max="256"
                placeholder="2 - 256"
                v-on:keydown="numConstrain($event, true, true)"
              />
            </div>
          </div>
        </td>
      </tr>
    <!-- <tr>
      <td colspan="2" class="force-vcenter" width="100%">
        <label
          class="checkbox"
          title="Unoptimize each frame of the GIF to fully define their original look. Allows editing of each frame on any other application at the cost of increased file size.">
          <input type="checkbox" v-model="is_unoptimized" v-bind:disabled="is_optimized || is_lossy || is_reduced_color"
          @change="$emit('update:is_unoptimized', is_unoptimized)" />
          Unoptimize
        </label>
      </td>
    </tr> -->
    </Fragment>
  <!-- </table> -->
</template>

<script>
// import Vue from 'vue';
// import { Plugin } from 'vue'
import { Fragment }  from 'vue-fragment';
const { numConstrain } = require("../Utility.vue");
const lodashClonedeep = require('lodash.clonedeep');

let props = ['is_unoptimized']

export default {
  components: { Fragment },
  props: props,
  name: "GIFOptimizationRow",
  data: function() {
    return {
      preserve_alpha: false,
      is_optimized: false,
      optimization_level: "1",
      is_lossy: false,
      lossy_value: "",
      is_reduced_color: false,
      color_space: "",
    };
  },
  methods: {
    numConstrain: numConstrain,
  }
};
</script>
