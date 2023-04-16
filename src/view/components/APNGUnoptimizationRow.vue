<template>
  <div class="optimization-form row-3">
    <div class="field-cell-group">
      <div class="toggle-cell">
        <label class="checkbox" title="Unoptimizes the APNG">
          <input
            v-model="isUnoptimized"
            type="checkbox"
            :disabled="isDisabled"
            @change="$emit('update:isUnoptimized', isUnoptimized)"
          />
          Unoptimize
        </label>
      </div>
      <div class="field-cell"></div>
    </div>
  </div>
</template>

<script>
// import { Fragment } from 'vue-fragment';

export default {
  name: "APNGUnoptimizationRow",
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
  // components: { Fragment },
};
</script>
