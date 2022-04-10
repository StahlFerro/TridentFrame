<template>
  <tr>
    <td colspan="2" class="force-vcenter">
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
    </td>
  </tr>
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
      preserve_alpha: false,
    //   is_optimized: false,
    //   is_lossy: false,
    //   is_reduced_color: false,
      is_unoptimized: false,
    };
  }
};
</script>
