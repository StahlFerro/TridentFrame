<template>
  <Fragment>
    <tr>
      <td class="force-vcenter" width="35%">
        <label class="checkbox" title="Optimize APNG to decrease file size without affecting quality">
          <input v-model="apng_is_optimized" v-bind:disabled="apng_is_unoptimized"
           @change="$emit('update:apng_is_optimized', apng_is_optimized)" type="checkbox" />
          Optimize
        </label>
      </td>
      <td class="force-vcenter" width="65%">
        <div class="field">
          <div class="control">
            <div class="select is-neon-cyan">
              <select v-model="apng_optimization_level" @change="$emit('update:apng_optimization_level', apng_optimization_level)" v-bind:disabled="!apng_is_optimized">
                <option value="1" title="Default compression">Lv. 1: zlib compression</option>
                <option value="2" title="Heavier compression than zlib. Takes longer">Lv. 2: 7zip compression</option>
                <option value="3" title="Heaviest compression. Takes longest">Lv. 3: zopfli compression</option>
              </select>
            </div>
          </div>
        </div>
      </td>
    </tr>
    <tr>
      <td class="force-vcenter">
        <label
          class="checkbox"
          title="Performs significant file size reduction at a slight cost of quality (artifacts and noise).\n
          The smaller the value, the stronger the compression will be and the lower the quality will be."
        >
          <input v-model="apng_is_lossy" type="checkbox" v-bind:disabled="apng_is_unoptimized"
            @change="$emit('update:apng_is_lossy', apng_is_lossy)" />
          Lossy-compression
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
              min="10"
              max="100"
              placeholder="10 - 100"
              v-bind:disabled="!apng_is_lossy"
            />
          </div>
        </div>
      </td>
    </tr>
    
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

var data = {
  apng_is_optimized: false,
  apng_optimization_level: "1",
  apng_is_lossy: false,
  apng_lossy_value: "",
  // apng_is_unoptimized: false,
};

let props = ['apng_is_unoptimized'];

export default {
  name: "APNGOptimizationRow",
  props: props,
  components: { Fragment },
  data: function() {
    return data;
  }
};
</script>
