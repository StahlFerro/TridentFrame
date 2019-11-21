<template>
  <table class="table mod-new-control-table is-hpaddingless" width="100%">
    <tr>
      <td class="force-vcenter" width="20%">
        <label class="checkbox" title="Optimize GIFs to reduce output filesize">
          <input v-model="is_optimized" v-bind:disabled="is_unoptimized"
           @change="$emit('update:is_optimized', is_optimized)" type="checkbox" />
          Optimize
        </label>
      </td>
      <td class="force-vcenter" width="20%">
        <div class="field">
          <!-- <label class="label">Optimization Level</label> -->
          <div class="control">
            <div class="select is-neon-cyan">
              <select v-model="optimization_level" @change="$emit('update:optimization_level', optimization_level)" v-bind:disabled="!is_optimized">
                <option value="1">Lv. 1 Store changed portion only</option>
                <option value="2">Lv. 2 Also uses transparency</option>
                <option value="3">Lv. 3 All optimization methods</option>
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
          title="Performs significant file size reduction at a slight cost of quality (artifacts and noise).\n
          The smaller the value, the stronger the compression will be and the lower the quality will be."
        >
          <input v-model="is_lossy" type="checkbox"
            @change="$emit('update:is_lossy', is_lossy)" />
          Lossy-compression
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
              min="10"
              max="100"
              placeholder="10 - 100"
              v-bind:disabled="!is_lossy"
            />
          </div>
        </div>
      </td>
    </tr>
  </table>
</template>

<script>
var data = {
  is_optimized: false,
  optimization_level: "1",
  is_lossy: false,
  lossy_value: "",
  is_unoptimized: false,
};

export default {
  name: "APNGOptimizationTable",
  data: function() {
    return data;
  }
};
</script>
