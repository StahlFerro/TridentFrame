<template>
  <table class="table mod-new-control-table is-hpaddingless" width="100%">
    <tr>
      <td class="force-vcenter" width="20%">
        <label class="checkbox" title="Optimize GIFs to reduce output filesize">
          <input v-model="is_optimized" @change="$emit('update:is_optimized', is_optimized)" type="checkbox" />
          Optimize
        </label>
      </td>
      <td class="force-vcenter" width="20%">
        <div class="field">
          <!-- <label class="label">Optimization Level</label> -->
          <div class="control">
            <div class="select is-neon-cyan">
              <select v-model="optimization_level" @change="$emit('update:optimization_level', optimization_level)" v-bind:disabled="!is_optimized">
                <option value="1">Low</option>
                <option value="2">Medium</option>
                <option value="3">High</option>
              </select>
            </div>
          </div>
        </div>
      </td>
    </tr>
    <tr>
      <td class="force-vcenter" width="20%">
        <label
          class="checkbox"
          title="Performs significant filesize reduction at the cost of quality"
        >
          <input v-model="is_lossy" type="checkbox" @change="$emit('update:is_lossy', is_lossy)" />
          Lossy-compress
        </label>
      </td>
      <td class="force-vcenter" width="20%">
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
            />
          </div>
        </div>
      </td>
    </tr>
    <tr>
      <td class="force-vcenter" width="20%">
        <label
          class="checkbox"
          title="Sets the number of colors for the GIF. Ranging from 2 colors (monochrome) to 256 (maximum for GIFs). Warning: this will also eliminate local/per-frame color tables, setting just one global color table for every frame.">
          <input  type="checkbox" v-model="is_reduced_color" @change="$emit('update:is_reduced_color', is_reduced_color)" />
          Color space
        </label>
      </td>
      <td class="force-vcenter" width="20%">
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
            />
          </div>
        </div>
      </td>
    </tr>
  </table>
</template>

<script>
var data = {
  is_reversed: false,
  preserve_alpha: false,
  is_optimized: false,
  optimization_level: "1",
  is_lossy: false,
  lossy_value: "",
  is_reduced_color: false,
  color_space: ""
};

export default {
  name: "GIFOptimizationTable",
  data: function() {
    return data;
  }
};
</script>
