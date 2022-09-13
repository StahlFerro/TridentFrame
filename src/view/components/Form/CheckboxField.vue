<template>
  <label class="checkbox" :title="hint">
    <input 
      :checked="modelValue" 
      type="checkbox"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
    {{ label }}
  </label>
</template>

<script>
export default {
  name: "CheckboxField",
  props: {
    label: {
      type: String,
      required: true,
    },
    hint: {
      type: String,
      default: null,
      required: false
    },
    modelValue: {
      type: Boolean,
    },
  },
  emits: ['update:modelValue']
};
</script>