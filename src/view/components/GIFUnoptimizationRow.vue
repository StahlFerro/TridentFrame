<template>
  <div class="optimization-form row-3">
    <div class="field-cell-group">
      <div class="toggle-cell">
        <label
          class="checkbox"
          title="Unoptimize each frame of the GIF to fully define their original look. Allows editing of each frame on any other application at the cost of increased file size."
        >
          <input
            v-model="is_unoptimized" type="checkbox" :disabled="isOptimized || isLossy || isReducedColor"
            @change="$emit('update:is_unoptimized', is_unoptimized)"
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

export default {
  name: "GIFUnoptimizationRow",
  props: {
    isOptimized: Boolean,
    isLossy: Boolean,
    isReducedColor: Boolean
  },
  data() {
    return {
      is_unoptimized: false,
    };
  }
};
</script>
