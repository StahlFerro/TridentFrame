<template>
    <tr>
      <td colspan="2" class="force-vcenter">
        <label
          class="checkbox"
          title="Unoptimize each frame of the GIF to fully define their original look. Allows editing of each frame on any other application at the cost of increased file size.">
          <input type="checkbox" v-model="is_unoptimized" v-bind:disabled="is_optimized || is_lossy || is_reduced_color"
          @change="$emit('update:is_unoptimized', is_unoptimized)" />
          Unoptimize
        </label>
      </td>
    </tr>
</template>

<script>

export default {
  props: ['is_optimized', 'is_lossy', 'is_reduced_color'],
  name: "GIFUnoptimizationRow",
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
