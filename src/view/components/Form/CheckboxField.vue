<template>
  <label class="checkbox" :title="hint">
    <input 
      type="checkbox"
      :checked="modelValue" 
      :disabled="isReadonly"
      @change="$emit('update:modelValue', $event.target.checked)"
      @mouseover="handleMouseDownOver"
      @mousedown="handleMouseDownOver"
    />
    {{ label }}
  </label>
</template>

<script>
import { type } from 'os'

export default {
  name: "CheckboxField",
  props: {
    label: {
      type: String,
      default: "",
      required: false,
    },
    hint: {
      type: String,
      default: null,
      required: false
    },
    modelValue: {
      type: Boolean,
    },
    isReadonly: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue', 'mouse-over-down'],
  methods: {
    handleMouseDownOver(event) {
      // console.log(event);
      // If mouse hovers over the element while the left button is held down (key 1), emit the custom event
      if (event.type == "mouseover" && event.which == 1) {
        this.$emit('mouse-over-down', event);
      }
      // if (event.type == "mousedown" && event.which == 1) {
      //   this.$emit('mouse-over-down', event);
      // }
    }
  }
};
</script>