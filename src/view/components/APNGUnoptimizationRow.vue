<template>
    <tr>
      <td class="force-vcenter">
        <label class="checkbox" title="Unoptimizes the APNG">
          <input v-model="apng_is_unoptimized" type="checkbox" v-bind:disabled="apng_is_optimized || apng_is_lossy"
            @change="$emit('update:apng_is_unoptimized', apng_is_unoptimized)" />
          Unoptimize
        </label>
      </td>
    </tr>
</template>

<script>
// import { Fragment } from 'vue-fragment';

export default {
  name: "APNGUnoptimizationRow",
  props: ['apng_is_optimized', 'apng_is_lossy'],
  // components: { Fragment },
  data: function() {
    return {
      // apng_is_optimized: false,
      // apng_optimization_level: "1",
      // apng_is_lossy: false,
      // apng_lossy_value: "",
      apng_is_unoptimized: false,
    };
  }
};
</script>
