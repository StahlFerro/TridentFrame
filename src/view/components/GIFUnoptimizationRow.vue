<template>
  <div class="optimization-form row-3">
    <div class="field-cell-group">
      <div class="toggle-cell">
        <label
          class="checkbox"
          title="Unoptimize each frame of the GIF to fully define their original look. Allows editing of each frame on any other application at the cost of increased file size."
        >
          <input
            v-model="isUnoptimized" type="checkbox" :disabled="isDisabled"
            @change="$emit('update:isUnoptimized', isUnoptimized)"
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
    isDisabled: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {
      isUnoptimized: false,
    };
  },
  emits: ['update:isUnoptimized'],
};
</script>
