<template>
  <Fragment>
    <tr>
      <td class="force-vcenter" width="25%">
        <label class="checkbox" title="Optimize APNG to decrease file size without affecting quality">
          <input v-model="apng_is_optimized" v-bind:disabled="apng_is_unoptimized"
           @change="$emit('update:apng_is_optimized', apng_is_optimized)" type="checkbox" />
          Optimize
        </label>
      </td>
      <td class="force-vcenter" width="25%">
        <div class="field">
          <div class="control">
            <div class="select is-neon-cyan" v-bind:class="{'non-interactive': !apng_is_optimized}">
              <select v-model="apng_optimization_level" @change="$emit('update:apng_optimization_level', apng_optimization_level)">
                <option value="1" title="Default compression">Lv. 1: zlib compression</option>
                <option value="2" title="Heavier compression than zlib. Takes longer">Lv. 2: 7zip compression</option>
                <option value="3" title="Heaviest compression. Takes longest">Lv. 3: zopfli compression</option>
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
          title="Limits the number of colors for all frames of the APNG. Ranging from 2 colors (monochrome) to 256 (maximum for PNG palettes)."
        >
          <input v-model="apng_is_lossy" type="checkbox" v-bind:disabled="apng_is_unoptimized"
            @change="$emit('update:apng_is_lossy', apng_is_lossy)" />
          Color space
        </label>
      </td>
      <td class="force-vcenter">
        
        <div class="field">
          <!-- <label class="label">Color space</label> -->
          <div class="control">
            <input
              v-model="apng_lossy_value"
              @change="$emit('update:apng_lossy_value', apng_lossy_value)"
              class="input is-neon-white"
              type="number"
              min="2"
              max="256"
              placeholder="2 - 256"
              v-bind:disabled="!apng_is_lossy"
              v-on:keydown="numConstrain($event, true, true)"
            />
          </div>
        </div>
      </td>
    </tr>
<!--     
    <tr>
      <td class="force-vcenter">
        <label class="checkbox" title="Change color mode of image sequence before combinging them into APNG">
          <input v-model="apng_convert_color_mode" type="checkbox" 
              @change="$emit('update:apng_convert_color_mode', apng_convert_color_mode)"/>
          Change Color Mode
        </label>
      </td>
      <td class="force-vcenter">
        <div class="field">
          <div class="control">
            <div class="select is-neon-cyan">
              <select v-model="apng_new_color_mode" v-bind:disabled="!apng_convert_color_mode"
                @change="$emit('update:apng_new_color_mode', apng_new_color_mode)">
                <option value="RGBA" title="RGB + Alpha color mode">RGBA</option>
                <option value="RGB" title="RGB color mode">RGB</option>
                <option value="P" title="Palette color mode">Palette</option>
              </select>
            </div>
          </div>
        </div>
      </td>
    </tr> -->
    <!-- <tr>
      <td class="force-vcenter">
        <label class="checkbox" title="Unoptimizes the APNG">
          <input v-model="apng_is_unoptimized" type="checkbox" v-bind:disabled="apng_is_optimized || apng_is_lossy"
            @change="$emit('update:apng_is_unoptimized', apng_is_unoptimized)" />
          Unoptimize
        </label>
      </td>
    </tr> -->
  <!-- </table> -->
  </Fragment>
</template>

<script>
import { Fragment } from 'vue-fragment';
const { numConstrain } = require("../Utility.vue");

let props = ['apng_is_unoptimized'];

export default {
  name: "APNGOptimizationRow",
  props: props,
  components: { Fragment },
  data: function() {
    return {
      apng_is_optimized: false,
      apng_optimization_level: "1",
      apng_is_lossy: false,
      apng_lossy_value: "",
      apng_speed_value: "",
      apng_convert_color_mode: false,
      apng_new_color_mode: "RGBA",
      // apng_is_unoptimized: false,
    };
  },
  methods: {
    numConstrain: numConstrain,
  }
};
</script>
