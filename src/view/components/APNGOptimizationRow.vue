<template>
  <tr>
    <td class="force-vcenter" width="25%">
      <label class="checkbox" title="Optimize APNG to decrease file size without affecting quality">
        <input
          v-model="apng_is_optimized" :disabled="apng_is_unoptimized"
          type="checkbox" @change="$emit('update:apng_is_optimized', apng_is_optimized)"
        />
        Optimize
      </label>
    </td>
    <td class="force-vcenter" width="25%">
      <div class="field">
        <div class="control">
          <div class="select is-neon-cyan" :class="{'non-interactive': !apng_is_optimized}">
            <select v-model="apng_optimization_level" @change="$emit('update:apng_optimization_level', apng_optimization_level)">
              <option value="1" title="Normal compression">
                Lv. 1: zlib compression
              </option>
              <option value="2" title="Heavier compression than zlib. Takes longer">
                Lv. 2: 7zip compression
              </option>
              <option value="3" title="Heaviest compression. Takes longest">
                Lv. 3: zopfli compression
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
        title="Use pngquant to lossy-compress PNG images."
      >
        <input
          v-model="apng_quantization_enabled" type="checkbox" :disabled="apng_is_unoptimized"
          @change="$emit('update:apng_quantization_enabled', apng_quantization_enabled)"
        />
        Quantize frames
      </label>
    </td>
    <td class="force-vcenter">
      <div class="field is-horizontal">
        <!-- <div class="field-label is-normal is-padding-middle">
          <label class="label">Quality</label>
        </div> -->
        <div class="field-body">
          <div class="field">
            <label
              class="label"
              title="Minimum quality. Ranging from 0 (worst quality but strongest compression) to 100 (best quality, weakest compression)"
            >Min Quality</label>
            <div class="control">
              <input
                v-model="apng_quantization_quality_min"
                class="input is-neon-white"
                type="number"
                min="0"
                max="100"
                placeholder="0 - 100"
                :disabled="!apng_quantization_enabled"
                @change="$emit('update:apng_quantization_quality_min', apng_quantization_quality_min)"
                @keydown="numConstrain($event, true, true)"
              />
            </div>
          </div>
          <div class="field">
            <label
              class="label"
              title="Maximum quality. Ranging from 0 (worst quality but strongest compression) to 100 (best quality, weakest compression)"
            >Max Quality</label>
            <div class="control">
              <input
                v-model="apng_quantization_quality_max"
                class="input is-neon-white"
                type="number"
                min="0"
                max="100"
                placeholder="0 - 100"
                :disabled="!apng_quantization_enabled"
                @change="$emit('update:apng_quantization_quality_max', apng_quantization_quality_max)"
                @keydown="numConstrain($event, true, true)"
              />
            </div>
          </div>
        </div>
      </div>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <label
          class="label"
          title="Speed/quality trade-off. Ranging from 1 (slowest but preserves quality as much as possible) to 10 (fastest, but results in 10% lower quality)"
        >Speed</label>
        <div class="control">
          <input
            v-model="apng_quantization_speed"
            class="input is-neon-white"
            type="number"
            min="1"
            max="10"
            placeholder="21- 10"
            :disabled="!apng_quantization_enabled"
            @change="$emit('update:apng_quantization_speed', apng_quantization_speed)"
            @keydown="numConstrain($event, true, true)"
          />
        </div>
      </div>
    </td>
    <td class="force-vcenter" width="25%" />
  </tr>
  <tr>
    <td class="force-vcenter">
      <label
        class="checkbox"
        title="When checked, reduce the amount of colors on each PNG image. Ranging from 2 colors (monochrome) to 256."
      >
        <input
          v-model="apng_is_reduced_color" type="checkbox" :disabled="apng_is_unoptimized"
          @change="$emit('update:apng_is_reduced_color', apng_is_reduced_color)"
        />
        Color space
      </label>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <!-- <label class="label">Color space</label> -->
        <div class="control">
          <input
            v-model="apng_color_count"
            class="input is-neon-white"
            type="number"
            min="2"
            max="256"
            placeholder="2 - 256"
            :disabled="!apng_is_reduced_color"
            @change="$emit('update:apng_color_count', apng_color_count)"
            @keydown="numConstrain($event, true, true)"
          />
        </div>
      </div>
    </td>
    <td class="force-vcenter" width="25%" />
    <td class="force-vcenter" width="25%" />
  </tr>
</template>

<script>
import { APNGOptimizationCriteria } from "../../models/criterion";
import { numConstrain } from "../../modules/events/constraints";


export default {
  name: "APNGOptimizationRow",
  props: ['apng_is_unoptimized'],
  emits: ['update:apng_is_optimized', 'update:apng_optimization_level', 'update:apng_quantization_enabled',
  'update:apng_quantization_quality_min', 'update:apng_quantization_quality_max', 
  'update:apng_quantization_speed', 'update:apng_is_reduced_color', 'update:apng_color_count'],
  // components: { Fragment },
  data: function() {
    return {
      ...new APNGOptimizationCriteria(),
      // hasOptimization: false,
      // apng_is_optimized: false,
      // apng_optimization_level: "1",
      // apng_is_reduced_color: false,
      // apng_color_count: 256,
      // apng_quantization_enabled: false,
      // apng_quantization_quality_min: 65,
      // apng_quantization_quality_max: 80,
      // apng_quantization_speed: 3,
      // apng_convert_color_mode: false,
      // apng_new_color_mode: "RGBA",
      // apng_is_unoptimized: false,
    };
  },
  computed: {
    // hasOptimizaton () {
    //   let hasOptim = this.apng_is_optimized || this.apng_quantization_enabled || this.apng_is_reduced_color;
    //   console.debug(`APNGOpt component hasOptim: ${hasOptim}`);
    //   this.$emit('update:hasOptimizaton', hasOptim);
    //   return hasOptim;
    // }
  },
  watch: {
    // hasOptimizatonWatcher () {
    //   let hasOptim = this.apng_is_optimized || this.apng_quantization_enabled || this.apng_is_reduced_color;
    //   console.debug(`APNGOpt component hasOptim: ${hasOptim}`);
    //   this.$emit('update:hasOptimizaton', hasOptim);
    //   // return hasOptim;
    // }
  },
  methods: {
    numConstrain: numConstrain,
    getOptimStatus() {
      let hasOptim = this.apng_is_optimized || this.apng_quantization_enabled || this.apng_is_reduced_color;
      return hasOptim
    }
  },
};
</script>
