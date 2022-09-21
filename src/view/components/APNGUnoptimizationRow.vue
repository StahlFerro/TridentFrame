<template>
  <div class="optimization-form row-3">
    <div class="field-cell-group">
      <div class="toggle-cell">
        <label class="checkbox" title="Unoptimizes the APNG">
          <input
            v-model="apng_is_unoptimized" type="checkbox" :disabled="apngIsOptimized || apngIsLossy"
            @change="$emit('update:apng_is_unoptimized', apng_is_unoptimized)"
          />
          Unoptimize
        </label>
      </div>
      <div class="field-cell">

      </div>
    </div>
  </div>
</template>

<script>
// import { Fragment } from 'vue-fragment';

export default {
  name: "APNGUnoptimizationRow",
  props: {
    apngIsOptimized: Boolean,
    apngIsLossy: Boolean,
  },
  emits: ['update:apng_is_unoptimized'],
  // components: { Fragment },
  data: function() {
    return {
      // apng_is_optimized: false,
      // apng_optimization_level: "1",
      // apng_is_reduced_color: false,
      // apng_color_count: "",
      apng_is_unoptimized: false,
    };
  }
};
</script>
