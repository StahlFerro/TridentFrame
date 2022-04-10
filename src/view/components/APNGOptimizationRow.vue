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
      <div class="field">
        <label
          class="label"
          title="Quality to preserve. Ranging from 0 (worst quality but strongest compression) to 100 (best quality, weakest compression)"
        >Quality</label>
        <div class="control">
          <input
            v-model="apng_quantization_quality"
            class="input is-neon-white"
            type="number"
            min="0"
            max="100"
            placeholder="0 - 100"
            :disabled="!apng_quantization_enabled"
            @change="$emit('update:apng_quantization_quality', apng_quantization_quality)"
            @keydown="numConstrain($event, true, true)"
          />
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
        title="Use pngquant to lossy-compress each PNG images before combining them into a single APNG"
      >
        <input
          v-model="apng_is_lossy" type="checkbox" :disabled="apng_is_unoptimized"
          @change="$emit('update:apng_is_lossy', apng_is_lossy)"
        />
        Color space
      </label>
    </td>
    <td class="force-vcenter">
      <div class="field">
        <!-- <label class="label">Color space</label> -->
        <div class="control">
          <input
            v-model="apng_lossy_value"
            class="input is-neon-white"
            type="number"
            min="2"
            max="256"
            placeholder="2 - 256"
            :disabled="!apng_is_lossy"
            @change="$emit('update:apng_lossy_value', apng_lossy_value)"
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
import { numConstrain } from "../../modules/events/constraints";


export default {
  name: "APNGOptimizationRow",
  props: ['apng_is_unoptimized'],
  emits: ['update:apng_is_optimized', 'update:apng_optimization_level', 'update:apng_quantization_enabled', 'update:apng_quantization_quality', 
  'update:apng_quantization_speed', 'update:apng_is_lossy', 'update:apng_lossy_value'],
  // components: { Fragment },
  data: function() {
    return {
      apng_is_optimized: false,
      apng_optimization_level: "1",
      apng_is_lossy: false,
      apng_lossy_value: "",
      apng_quantization_enabled: false,
      apng_quantization_quality: 70,
      apng_quantization_speed: 3,
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
